# iOSRealRun-cli-18

## ✨ 最新更新

### v0.2.0 - GUI 图形界面版本 🎉

- ✅ **现代化 GUI 界面**: 使用 CustomTkinter 构建的美观易用的图形界面
- ✅ **依赖优化**: 更新到最新稳定版本的 pymobiledevice3 (6.1.6+)
- ✅ **完全可控**: GUI 界面提供完整的程序控制，包括:
  - 设备初始化和连接状态监控
  - 路线文件选择（可视化文件浏览器）
  - 跑步速度调节（滑块控制，0.5-10.0 m/s）
  - 实时日志显示
  - 一键启动/停止模拟
  - 调试模式开关
- ✅ **向后兼容**: 保留原有 CLI 命令行模式
- ✅ **双模式运行**: 可以选择 GUI 或 CLI 模式运行

### 截图预览
<img width="800" alt="GUI Preview" src="https://github.com/user-attachments/assets/89554033-0357-4873-9a21-a647a3ee581a" />

---

本项目基于 [iOSRealRun-cli-17](https://github.com/iOSRealRun/iOSRealRun-cli-17) 修改而来，并更新了依赖的 [pymobiledevice3](https://github.com/doronz88/pymobiledevice3)。

如果使用时出现了无法解决的报错可以考虑使用[这个仓库手动启动](https://github.com/BiancoChiu/iOSEasyRun)。

测试环境：
- 操作系统：MacOS，Windows11，Linux
- Python 版本：3.12+
- iOS 版本：17+ / 18+
- pymobiledevice3 版本：6.1.6+

## 📋 功能特性

- 🎯 iOS 设备位置模拟
- 🏃 自动循环跑步路线
- 📍 支持 BD-09 到 WGS-84 坐标转换
- 🎚️ 可调节跑步速度
- 🖥️ 现代化 GUI 图形界面
- 💻 传统 CLI 命令行模式
- 📊 实时日志输出
- 🔒 安全的设备连接管理

## 🚀 用法简介

### 前置条件

1. 系统是 `Windows`，`macOS`，`Linux` 均可（Linux 请参考[此 issue](https://github.com/BiancoChiu/iOSRealRun-cli-18/issues/4)）
2. iPhone 或 iPad 系统版本大于等于 17（17 / 18 均可运行）
3. Windows 需要安装 iTunes
4. 已安装 `Python 3.12+` 和 `uv` / `pip3` (选择一种方式即可）
5. **重要**: 只能有一台 iPhone 或 iPad 连接到电脑，否则会出问题

### 安装步骤

1. 克隆本项目到本地并进入项目目录
2. 安装依赖  
    ```shell
    # 使用 uv (推荐)
    uv sync
    
    # 或使用 pip
    pip3 install -r requirements.txt
    ```
    
3. 修改配置和路线文件
   - 编辑 `config.yaml` 设置速度等参数
   - 准备路线文件（默认为 `HNroute.txt`）
   - 路线文件格式参考 [这里](https://github.com/iOSRealRun/iOSRealRun-cli/blob/main/README.md#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95) 的 4、5、7 步

### 🖥️ 方式一：使用 GUI 图形界面（推荐）

GUI 界面提供了更直观、更易用的操作方式，适合所有用户。

1. 将设备连接到电脑，解锁，如果请求信任的提示框，请点击信任

2. **Windows** - 以管理员身份运行
   ```shell
   # 使用 uv
   uv run python gui_main.py
   
   # 或使用 pip
   python gui_main.py
   ```

3. **macOS / Linux** - 使用 sudo 运行
   ```shell
   # 使用 uv
   sudo uv run python gui_main.py
   
   # 或使用 pip
   sudo python3 gui_main.py
   ```

4. 在 GUI 界面中：
   - 📁 点击"浏览"选择路线文件（或使用默认路线）
   - 🎚️ 拖动滑块调整跑步速度（0.5-10.0 m/s）
   - ⚙️ 如需调试，勾选"调试模式"
   - 🔄 点击"初始化设备"按钮连接设备
   - ▶️ 等待状态变为"已就绪"后，点击"开始模拟"
   - ⏹️ 需要停止时，点击"停止模拟"按钮
   - 📋 右侧日志窗口实时显示运行状态

> **注意**: GUI 模式会在停止模拟时自动恢复定位

### 💻 方式二：使用 CLI 命令行模式（传统方式）

CLI 模式适合熟悉命令行的高级用户。

1. 将设备连接到电脑，解锁，如果请求信任的提示框，请点击信任

2. **Windows** - 以管理员身份打开终端
    ```shell
    # 使用 uv
    uv run main.py
    
    # 或使用 pip
    python main.py
    ```

3. **macOS / Linux** - 使用 sudo 运行
    ```shell
    # 使用 uv
    sudo uv run main.py
    
    # 或使用 pip
    sudo python main.py
    ```

4. 按照提示操作
   - 如果一直显示没有设备连接，Windows 平台请确保 iTunes 已安装
   - 重新运行程序时请确保设备已连接、解锁并信任

5. **结束请务必使用 `Ctrl + C` 终止程序，否则无法恢复定位**

6. 如果定位未恢复，可以重启手机解决

### 🎯 方式三：使用启动器（推荐新手）

使用便捷启动器可以在 GUI 和 CLI 之间快速切换：

```shell
# Windows (管理员权限)
python launcher.py

# macOS / Linux
sudo python3 launcher.py
```

然后根据提示选择：
- 输入 `1` - 启动 GUI 图形界面模式
- 输入 `2` - 启动 CLI 命令行模式  
- 输入 `3` - 退出

## 📝 配置说明

### config.yaml

```yaml
v: 3.3                          # 跑步速度 (m/s)
routeConfig: "HNroute.txt"      # 路线文件路径
libimobiledeviceDir: "libimobiledevice"  # (已弃用)
imageDir: "DeveloperDiskImage"  # (已弃用)
```

### 路线文件格式

路线文件是一个包含经纬度坐标的文本文件，格式示例：
```
{"lat": 30.1234, "lng": 120.5678},
{"lat": 30.1235, "lng": 120.5679},
{"lat": 30.1236, "lng": 120.5680}
```

## 🔧 依赖更新说明

本版本对依赖进行了重大优化：

| 依赖包 | 旧版本 | 新版本 | 说明 |
|--------|--------|--------|------|
| pymobiledevice3 | 4.26.3 | 6.1.6+ | 大版本升级，支持最新 iOS |
| PyYAML | 6.0.1 | 6.0.3+ | 安全性修复 |
| geopy | 2.4.1 | 2.4.1+ | 保持稳定 |
| coloredlogs | - | 15.0.1+ | 新增：彩色日志输出 |
| customtkinter | - | 5.2.2+ | 新增：现代化 GUI 界面 |

所有依赖均已通过 GitHub Advisory Database 安全检查，无已知漏洞。

## ⚠️ 注意事项

1. **需要管理员/root权限**: 因为需要创建 TUN 设备
2. **只能连接一台设备**: 多台设备会导致连接混乱
3. **正确退出很重要**: 
   - GUI 模式：点击"停止模拟"按钮
   - CLI 模式：使用 `Ctrl+C` 而不是直接关闭窗口
   - 否则可能无法恢复正常定位，需要重启设备
4. **Windows 用户**: 确保已安装 iTunes 并可以识别设备
5. **开发者模式**: 首次使用需要在设备上启用开发者模式

## 🐛 故障排除

### 设备连接不上
- 检查设备是否解锁
- 检查是否点击了"信任此电脑"
- Windows 用户检查 iTunes 是否已安装
- 尝试重新插拔设备

### 隧道启动失败
- 确保以管理员/root权限运行
- 检查防火墙设置
- 尝试重启程序

### 定位未恢复
- 重启 iPhone/iPad 设备
- 或在设备上：设置 -> 隐私 -> 定位服务 -> 系统服务 -> 重置位置与隐私

### GUI 界面无法启动
- 确保已安装所有依赖：`pip install -r requirements.txt`
- Linux 用户可能需要安装 tkinter：`sudo apt-get install python3-tk`

## 📄 许可证

见 [LICENSE](LICENSE) 文件

## 🙏 致谢
