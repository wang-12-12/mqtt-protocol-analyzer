# mqtt-protocol-analyzer
一款基于 Python 的 MQTT 协议深度分析自动化工具。利用 Wireshark/tshark 解析 .pcap 抓包文件，自动提取 MQTT 控制报文（CONNECT, PUBLISH, PUBACK），验证 QoS1 可靠性，检测异常断链，并生成结构化 CSV 报告。适用于物联网设备测试与车载 T-Box 通信故障诊断。
