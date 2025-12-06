"""
CLI interface for iOS Real Run
使用核心逻辑模块，保持CLI向后兼容
"""
import os
import asyncio
import logging

import config
from core_logic import RunnerCore


async def main():
    """CLI主函数"""
    debug = os.environ.get("DEBUG", False)
    
    # 创建核心运行器
    runner = RunnerCore(debug=debug)
    logger = logging.getLogger(__name__)
    
    try:
        # 初始化设备
        if not runner.initialize():
            logger.error("设备初始化失败")
            return
        
        # 启动隧道
        tunnel_info = runner.start_tunnel()
        if tunnel_info is None:
            logger.error("隧道启动失败")
            return
        
        process, address, port = tunnel_info
        
        try:
            logger.debug(f"tunnel address: {address}, port: {port}")
            
            # 加载路线
            loc = runner.get_route()
            if loc is None:
                logger.error("路线加载失败")
                return
            
            logger.info(f"已从 {config.config.routeConfig} 加载路线")
            
            try:
                print(f"已开始模拟跑步，速度大约为 {config.config.v} m/s")
                print("会无限循环，按 Ctrl+C 退出")
                print("请勿直接关闭窗口，否则无法还原正常定位")
                await runner.run_simulation(address, port, loc, config.config.v)
            except KeyboardInterrupt:
                logger.debug("收到中断信号 (inner)")
                logger.debug(f"进程是否存活? {process.is_alive()}")
            finally:
                logger.debug(f"进程是否存活? {process.is_alive()}")
                logger.debug("开始清理定位")
        
        except KeyboardInterrupt:
            logger.debug("收到中断信号 (outer)")
        finally:
            logger.debug(f"进程是否存活? {process.is_alive()}")
            runner.stop_tunnel()
            print("Bye")
    
    except Exception as e:
        logger.error(f"运行出错: {e}")
        runner.cleanup()
        raise


if __name__ == "__main__":
    asyncio.run(main())