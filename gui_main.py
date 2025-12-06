"""
Modern GUI for iOS Real Run using CustomTkinter
"""
import os
import sys
import asyncio
import threading
import logging
from pathlib import Path
from typing import Optional

import customtkinter as ctk
from tkinter import filedialog, scrolledtext
import tkinter as tk

import config
from core_logic import RunnerCore


# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"


class TextHandler(logging.Handler):
    """Custom logging handler to redirect logs to GUI text widget"""
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        
    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.see(tk.END)
        self.text_widget.after(0, append)


class iOSRealRunGUI(ctk.CTk):
    """Main GUI Application Window"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("iOS Real Run - GUI")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Initialize variables
        self.runner_core: Optional[RunnerCore] = None
        self.running = False
        self.tunnel_info = None
        self.route_data = None
        self.loop = None
        self.runner_thread = None
        
        # Load initial config
        try:
            self.config = config.config
            self.route_file = self.config.routeConfig
            self.speed = self.config.v
        except:
            self.route_file = "HNroute.txt"
            self.speed = 3.3
        
        # Setup UI
        self.setup_ui()
        
        # Setup logging
        self.setup_logging()
        
        # Protocol for closing window
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_ui(self):
        """Setup the UI components"""
        # Configure grid layout (2 columns)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        
        # Left panel - Controls
        self.left_frame = ctk.CTkFrame(self, corner_radius=10)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Right panel - Logs
        self.right_frame = ctk.CTkFrame(self, corner_radius=10)
        self.right_frame.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")
        
        self.setup_left_panel()
        self.setup_right_panel()
        
    def setup_left_panel(self):
        """Setup left control panel"""
        # Title
        title = ctk.CTkLabel(self.left_frame, text="iOS Real Run", 
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))
        
        # Status indicator
        self.status_frame = ctk.CTkFrame(self.left_frame, corner_radius=5)
        self.status_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="● 未连接", 
                                         font=ctk.CTkFont(size=14),
                                         text_color="gray")
        self.status_label.pack(pady=5)
        
        # Route file selection
        route_label = ctk.CTkLabel(self.left_frame, text="路线配置文件:", 
                                   font=ctk.CTkFont(size=13))
        route_label.grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 5), sticky="w")
        
        self.route_entry = ctk.CTkEntry(self.left_frame, placeholder_text="选择路线文件...")
        self.route_entry.grid(row=3, column=0, padx=(20, 5), pady=5, sticky="ew")
        self.route_entry.insert(0, self.route_file)
        
        self.browse_btn = ctk.CTkButton(self.left_frame, text="浏览", width=70,
                                       command=self.browse_route_file)
        self.browse_btn.grid(row=3, column=1, padx=(5, 20), pady=5)
        
        # Speed configuration
        speed_label = ctk.CTkLabel(self.left_frame, text="跑步速度 (m/s):", 
                                   font=ctk.CTkFont(size=13))
        speed_label.grid(row=4, column=0, columnspan=2, padx=20, pady=(15, 5), sticky="w")
        
        self.speed_var = tk.DoubleVar(value=self.speed)
        self.speed_slider = ctk.CTkSlider(self.left_frame, from_=0.5, to=10.0, 
                                         variable=self.speed_var,
                                         command=self.update_speed_label)
        self.speed_slider.grid(row=5, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        
        self.speed_value_label = ctk.CTkLabel(self.left_frame, 
                                             text=f"{self.speed:.1f} m/s",
                                             font=ctk.CTkFont(size=12))
        self.speed_value_label.grid(row=6, column=0, columnspan=2, padx=20, pady=5)
        
        # Debug mode
        self.debug_var = tk.BooleanVar(value=False)
        self.debug_checkbox = ctk.CTkCheckBox(self.left_frame, text="调试模式", 
                                             variable=self.debug_var)
        self.debug_checkbox.grid(row=7, column=0, columnspan=2, padx=20, pady=(15, 5))
        
        # Initialize button
        self.init_btn = ctk.CTkButton(self.left_frame, text="初始化设备",
                                     command=self.initialize_device,
                                     font=ctk.CTkFont(size=14))
        self.init_btn.grid(row=8, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")
        
        # Start/Stop button
        self.start_btn = ctk.CTkButton(self.left_frame, text="开始模拟",
                                      command=self.toggle_simulation,
                                      font=ctk.CTkFont(size=14, weight="bold"),
                                      fg_color="green",
                                      hover_color="darkgreen",
                                      state="disabled")
        self.start_btn.grid(row=9, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        
        # Info text
        info_text = ("提示:\n"
                    "1. 确保设备已连接并解锁\n"
                    "2. Windows需要iTunes\n"
                    "3. 需要管理员/root权限\n"
                    "4. 结束后会自动恢复定位")
        info_label = ctk.CTkLabel(self.left_frame, text=info_text, 
                                 font=ctk.CTkFont(size=11),
                                 justify="left",
                                 text_color="gray")
        info_label.grid(row=10, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")
        
        # Configure column weights for left frame
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(1, weight=0)
        
    def setup_right_panel(self):
        """Setup right log panel"""
        # Title
        log_title = ctk.CTkLabel(self.right_frame, text="运行日志", 
                                font=ctk.CTkFont(size=16, weight="bold"))
        log_title.pack(padx=20, pady=(20, 10), anchor="w")
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(self.right_frame, 
                                                  wrap=tk.WORD,
                                                  width=60,
                                                  height=35,
                                                  font=("Courier", 9),
                                                  bg="#2b2b2b",
                                                  fg="#ffffff",
                                                  state='disabled')
        self.log_text.pack(padx=20, pady=(0, 10), fill="both", expand=True)
        
        # Clear log button
        self.clear_log_btn = ctk.CTkButton(self.right_frame, text="清空日志",
                                          command=self.clear_logs)
        self.clear_log_btn.pack(padx=20, pady=(0, 20))
        
    def setup_logging(self):
        """Setup logging to redirect to GUI"""
        # Create text handler
        text_handler = TextHandler(self.log_text)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                     datefmt='%H:%M:%S')
        text_handler.setFormatter(formatter)
        
        # Add handler to root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(text_handler)
        root_logger.setLevel(logging.INFO)
        
    def update_speed_label(self, value):
        """Update speed label when slider changes"""
        self.speed_value_label.configure(text=f"{float(value):.1f} m/s")
        
    def browse_route_file(self):
        """Open file dialog to select route file"""
        filename = filedialog.askopenfilename(
            title="选择路线文件",
            initialdir=".",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filename:
            self.route_entry.delete(0, tk.END)
            self.route_entry.insert(0, filename)
            
    def update_status(self, status_text, color):
        """Update status indicator"""
        self.status_label.configure(text=f"● {status_text}", text_color=color)
        
    def initialize_device(self):
        """Initialize device and setup tunnel"""
        def init_thread():
            self.update_status("正在初始化...", "yellow")
            self.init_btn.configure(state="disabled")
            
            try:
                # Create runner core
                debug = self.debug_var.get()
                self.runner_core = RunnerCore(debug=debug)
                
                # Initialize device
                if not self.runner_core.initialize():
                    self.update_status("初始化失败", "red")
                    logging.error("设备初始化失败，请检查连接")
                    return
                
                # Start tunnel
                self.tunnel_info = self.runner_core.start_tunnel()
                if self.tunnel_info is None:
                    self.update_status("隧道启动失败", "red")
                    logging.error("隧道启动失败，请重试")
                    return
                
                # Load route
                route_file = self.route_entry.get()
                if route_file:
                    # Update config with selected route file
                    config.config.routeConfig = route_file
                
                self.route_data = self.runner_core.get_route()
                if self.route_data is None:
                    self.update_status("路线加载失败", "red")
                    logging.error("路线文件加载失败，请检查文件")
                    self.runner_core.cleanup()
                    return
                
                self.update_status("已就绪", "green")
                logging.info("设备初始化成功，可以开始模拟")
                self.start_btn.configure(state="normal")
                
            except Exception as e:
                self.update_status("初始化错误", "red")
                logging.error(f"初始化过程出错: {e}")
            finally:
                self.init_btn.configure(state="normal")
        
        # Run in separate thread to avoid blocking GUI
        threading.Thread(target=init_thread, daemon=True).start()
        
    def toggle_simulation(self):
        """Toggle simulation start/stop"""
        if not self.running:
            self.start_simulation()
        else:
            self.stop_simulation()
            
    def start_simulation(self):
        """Start the simulation"""
        if self.tunnel_info is None or self.route_data is None:
            logging.error("请先初始化设备")
            return
        
        self.running = True
        self.start_btn.configure(text="停止模拟", fg_color="red", hover_color="darkred")
        self.init_btn.configure(state="disabled")
        self.update_status("运行中", "green")
        
        # Get current speed
        speed = self.speed_var.get()
        
        # Run simulation in separate thread
        def run_thread():
            try:
                process, address, port = self.tunnel_info
                
                # Create event loop for this thread
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
                
                logging.info(f"开始模拟跑步，速度: {speed:.1f} m/s")
                logging.info("按'停止模拟'按钮退出")
                
                # Run the simulation
                self.loop.run_until_complete(
                    self.runner_core.run_simulation(address, port, self.route_data, speed)
                )
            except Exception as e:
                logging.error(f"模拟运行出错: {e}")
            finally:
                if self.loop:
                    self.loop.close()
                self.loop = None
        
        self.runner_thread = threading.Thread(target=run_thread, daemon=True)
        self.runner_thread.start()
        
    def stop_simulation(self):
        """Stop the simulation"""
        self.running = False
        self.start_btn.configure(text="开始模拟", fg_color="green", hover_color="darkgreen")
        self.update_status("已停止", "yellow")
        logging.info("正在停止模拟...")
        
        # Stop the event loop
        if self.loop and self.loop.is_running():
            self.loop.call_soon_threadsafe(self.loop.stop)
        
        # Cleanup
        if self.runner_core:
            self.runner_core.cleanup()
        
        self.init_btn.configure(state="normal")
        self.start_btn.configure(state="disabled")
        self.tunnel_info = None
        self.route_data = None
        
        logging.info("模拟已停止")
        
    def clear_logs(self):
        """Clear log text area"""
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')
        
    def on_closing(self):
        """Handle window closing"""
        if self.running:
            logging.info("正在停止模拟并清理资源...")
            self.stop_simulation()
        
        if self.runner_core:
            self.runner_core.cleanup()
        
        self.destroy()


def main():
    """Main entry point for GUI application"""
    # Check for admin/root privileges
    import ctypes
    if sys.platform == "win32":
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("错误: 请以管理员权限运行此程序")
            print("右键程序图标 -> '以管理员身份运行'")
            input("按回车键退出...")
            sys.exit(1)
    elif os.geteuid() != 0:
        print("错误: 请以root权限运行此程序")
        print("使用: sudo python gui_main.py")
        input("按回车键退出...")
        sys.exit(1)
    
    # Create and run GUI
    app = iOSRealRunGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
