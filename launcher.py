#!/usr/bin/env python3
"""
便捷启动器 - 可以选择CLI或GUI模式
"""
import sys
import os


def main():
    print("=" * 50)
    print("iOS Real Run - 启动器")
    print("=" * 50)
    print()
    print("请选择运行模式:")
    print("1. GUI 模式 (图形界面)")
    print("2. CLI 模式 (命令行)")
    print("3. 退出")
    print()
    
    while True:
        choice = input("请输入选项 (1/2/3): ").strip()
        
        if choice == "1":
            print("\n正在启动 GUI 模式...")
            import gui_main
            gui_main.main()
            break
        elif choice == "2":
            print("\n正在启动 CLI 模式...")
            import asyncio
            import main
            asyncio.run(main.main())
            break
        elif choice == "3":
            print("再见!")
            sys.exit(0)
        else:
            print("无效选项，请重新输入")


if __name__ == "__main__":
    main()
