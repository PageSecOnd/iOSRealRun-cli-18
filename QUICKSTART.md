# 快速开始指南 / Quick Start Guide

## 🚀 快速开始

### 第一步：安装依赖

```bash
# 方法1：使用 uv (推荐，更快)
uv sync

# 方法2：使用 pip
pip install -r requirements.txt
```

### 第二步：准备工作

1. **连接设备**：将 iPhone/iPad 连接到电脑，解锁并信任此电脑
2. **检查iTunes**（仅Windows）：确保已安装 iTunes
3. **准备路线文件**：默认使用 `HNroute.txt`，或准备自己的路线文件

### 第三步：启动程序

#### 方式A：GUI图形界面（推荐新手）

**Windows**:
```bash
# 右键"命令提示符"或"PowerShell" -> "以管理员身份运行"
python gui_main.py
```

**macOS/Linux**:
```bash
sudo python3 gui_main.py
```

#### 方式B：命令行模式（熟悉CLI的用户）

**Windows**:
```bash
# 以管理员身份运行
python main.py
```

**macOS/Linux**:
```bash
sudo python3 main.py
```

#### 方式C：交互式启动器（最简单）

**Windows**:
```bash
# 以管理员身份运行
python launcher.py
# 然后输入 1 选择GUI，或输入 2 选择CLI
```

**macOS/Linux**:
```bash
sudo python3 launcher.py
# 然后输入 1 选择GUI，或输入 2 选择CLI
```

## 🖥️ GUI界面使用指南

1. **选择路线文件**
   - 点击"浏览"按钮选择路线文件
   - 或使用默认的 `HNroute.txt`

2. **调整速度**
   - 拖动滑块调整跑步速度 (0.5-10.0 m/s)
   - 建议速度：3-4 m/s（正常跑步速度）

3. **初始化设备**
   - 点击"初始化设备"按钮
   - 等待状态显示"已就绪"（绿色）

4. **开始模拟**
   - 点击"开始模拟"按钮
   - 观察日志窗口了解运行状态

5. **停止模拟**
   - 点击"停止模拟"按钮（按钮会变成红色）
   - 程序会自动恢复设备正常定位

## ⚠️ 常见问题

### 问：提示没有管理员权限怎么办？

**Windows**: 
- 右键程序图标 -> "以管理员身份运行"
- 或右键命令提示符/PowerShell -> "以管理员身份运行"

**macOS/Linux**: 
- 在命令前加上 `sudo`，例如：`sudo python3 gui_main.py`

### 问：找不到设备怎么办？

1. 检查设备是否已连接并解锁
2. 检查是否点击了"信任此电脑"
3. Windows用户：确保iTunes已安装并能识别设备
4. 重新插拔USB线
5. 重启程序

### 问：隧道启动失败怎么办？

1. 确认以管理员/root权限运行
2. 检查防火墙是否阻止了程序
3. 尝试重启程序
4. 查看日志了解具体错误信息

### 问：定位没有恢复怎么办？

1. **最简单方法**：重启iPhone/iPad
2. 或在设备上：设置 -> 隐私 -> 定位服务 -> 系统服务 -> 重置位置与隐私

### 问：GUI无法启动怎么办？

**Linux用户**可能需要安装tkinter：
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

## 📝 配置文件说明

### config.yaml

```yaml
v: 3.3                      # 跑步速度 (m/s)
routeConfig: "HNroute.txt"  # 路线文件路径
```

### 路线文件格式

路线文件是包含经纬度坐标的文本文件：

```
{"lat": 30.1234, "lng": 120.5678},
{"lat": 30.1235, "lng": 120.5679},
{"lat": 30.1236, "lng": 120.5680}
```

**获取坐标**：
- 在百度地图上获取坐标（程序会自动转换BD-09到WGS-84）
- 或使用高德地图、谷歌地图等

## 💡 使用建议

1. **首次使用**：建议先用GUI模式，更直观
2. **速度设置**：3-4 m/s 比较接近真实跑步速度
3. **路线选择**：选择合理的跑步路线，避免异常轨迹
4. **正确退出**：
   - GUI模式：点击"停止模拟"按钮
   - CLI模式：使用 Ctrl+C
   - 不要直接关闭窗口！

## 🔗 相关链接

- [完整文档](README.md)
- [更新日志](CHANGELOG.md)
- [问题反馈](https://github.com/PageSecOnd/iOSRealRun-cli-18/issues)

## ⚖️ 免责声明

本工具仅供学习和研究使用，请勿用于任何违反服务条款或法律法规的行为。使用本工具造成的任何后果由使用者自行承担。
