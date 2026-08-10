# MQTT 协议自动化分析器  
*(基于 Python + Wireshark/tshark)*
# mqtt-protocol-analyzer
##  项目简介
一款基于 Python 的 MQTT 协议深度分析自动化工具。利用 Wireshark/tshark 解析 .pcap 抓包文件，自动提取 MQTT 控制报文（CONNECT, PUBLISH, PUBACK），验证 QoS1 可靠性，检测异常断链，并生成结构化 CSV 报告。适用于物联网设备测试与车载 T-Box 通信故障诊断。
无需手工翻看 Wireshark  
自动检测 QoS1 可靠性问题  
可用于 车载 / 工业物联网 / 通信协议测试
##  核心功能
| 功能 | 说明 |
|---|---|
| **MQTT 报文解析** | CONNECT / CONNACK / PUBLISH / PUBACK / PINGREQ / DISCONNECT |
| **消息类型统计** | 自动统计各类 MQTT 控制报文数量 |
| **QoS1 一致性检测** | 校验 PUBLISH 与 PUBACK 数量是否匹配 |
| **TOPIC 分析** | 统计发布主题及频次 |
| **异常断链检测** | 识别是否存在 DISCONNECT 报文 |
| **CSV 导出** | 生成结构化分析结果，便于二次处理 |
| **终端可视化报告** | 直观展示协议交互概况 |
### 协议与工具
- **MQTT 3.1.1**
- **Wireshark / tshark**
- **TCP/IP**

### 开发语言
- **Python 3.8+**
- `subprocess`（调用 tshark）
- `csv`（结果导出）
- `collections.Counter`（统计分析）
---

##  项目结构
- mqtt_protocol_analyzer/
- ├── .venv/ # Python 虚拟环境
- ├── captures/
- │ ├── abnormal_disconnect.pcap # 示例抓包文件
- │ └── analysis_result.csv # 分析输出
- ├── src/
- │ ├── simulator.py # MQTT 模拟器（异常/正常模式）
- │ └── analyzer.py # MQTT 协议分析器（核心）
- ├── requirements.txt
- └── README.md
---
### 快速开始
- 1. 创建虚拟环境
**python -m venv .venv**
**.\.venv\Scripts\Activate.ps1**
- 2. 安装依赖
**pip install -r requirements.txt**
- 3. 准备抓包文件
模拟器运行后用WIRESHARK对其抓包
**python src/simulator.py abnormal**
**python src/simulator.py normal**
- 4. 运行分析器
**python src/analyzer.py**
- 5. 示例输出
- 📊 MQTT 报文分析报告
- 📁 文件: abnormal_disconnect.pcap
- ✅ MQTT 报文数: 25
- 📋 消息类型分布
- UNKNOWN(0) : 11 ████████████████████
- PUBLISH : 5 █████████
- PUBACK : 5 █████████
- CONNECT : 1 █
- CONNACK : 1 █
- PINGREQ : 1 █
- DISCONNECT : 1 █
- 🔍 异常检测
- ✅ PUBLISH(5) = PUBACK(5)，QoS1 确认完整
- ✅ 存在 DISCONNECT 报文 (1 条)
- ℹ️ 检测到 1 条 PINGREQ（心跳包）
- 📁 详细结果已保存到: captures/analysis_result.csv
-  6.调试阶段可使用 src/debug_analyzer.py 直接查看 tshark 原始输出，用于验证抓包文件与过滤条件是否匹配


