"""
Core logic for iOS Real Run - separated from UI concerns
"""
import logging
import signal
import asyncio
from typing import Tuple, Optional
import multiprocessing

from init import init
from init import tunnel
from init import route

import run
import config


class RunnerCore:
    """Core runner logic that can be used by both CLI and GUI"""
    
    def __init__(self, debug=False):
        self.debug = debug
        self.logger = logging.getLogger(__name__)
        self.process = None
        self.is_running = False
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        import coloredlogs
        level = logging.DEBUG if self.debug else logging.INFO
        coloredlogs.install(level=level)
        self.logger.setLevel(level)
        
        # Set log levels for various components
        log_level = logging.DEBUG if self.debug else logging.WARNING
        for logger_name in ['wintun', 'quic', 'asyncio', 'zeroconf', 
                           'parso.cache', 'parso.cache.pickle', 
                           'parso.python.diff', 'humanfriendly.prompts',
                           'blib2to3.pgen2.driver', 'urllib3.connectionpool']:
            logging.getLogger(logger_name).setLevel(log_level)
    
    def initialize(self) -> bool:
        """Initialize the device and check requirements"""
        try:
            init.init()
            self.logger.info("初始化完成")
            return True
        except Exception as e:
            self.logger.error(f"初始化失败: {e}")
            return False
    
    def start_tunnel(self) -> Optional[Tuple[multiprocessing.Process, str, int]]:
        """Start the tunnel and return process, address, port"""
        try:
            self.logger.info("正在启动隧道连接...")
            original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
            process, address, port = tunnel.tunnel()
            signal.signal(signal.SIGINT, original_sigint_handler)
            
            if process is None or address is None or port is None:
                self.logger.error("隧道启动失败")
                return None
            
            self.process = process
            self.logger.info(f"隧道已启动: {address}:{port}")
            return process, address, port
        except Exception as e:
            self.logger.error(f"启动隧道时发生错误: {e}")
            return None
    
    def stop_tunnel(self):
        """Stop the tunnel process"""
        if self.process and self.process.is_alive():
            self.logger.info("正在终止隧道进程...")
            self.process.terminate()
            self.process.join(timeout=5)
            if self.process.is_alive():
                self.logger.warning("隧道进程未正常终止，强制关闭")
                self.process.kill()
            self.logger.info("隧道进程已终止")
            self.process = None
    
    def get_route(self):
        """Get the route from config file"""
        try:
            loc = route.get_route()
            self.logger.info(f"从 {config.config.routeConfig} 加载路线成功")
            return loc
        except Exception as e:
            self.logger.error(f"加载路线失败: {e}")
            return None
    
    async def run_simulation(self, address: str, port: int, loc: list, speed: float):
        """Run the simulation with given parameters"""
        try:
            self.is_running = True
            self.logger.info(f"开始模拟跑步，速度: {speed} m/s")
            await run.run(address, port, loc, speed)
        except KeyboardInterrupt:
            self.logger.debug("收到中断信号")
        except Exception as e:
            self.logger.error(f"模拟运行时发生错误: {e}")
            raise
        finally:
            self.is_running = False
    
    def cleanup(self):
        """Cleanup resources"""
        self.logger.info("清理资源...")
        self.stop_tunnel()
        self.logger.info("清理完成")
