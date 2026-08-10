import subprocess
import os
import csv
from collections import Counter

# ========== 配置区 ==========
PCAP_DIR = r"C:\Users\w1951\Desktop\项目2\mqtt_protocol_analyzer\captures"
PCAP_FILE = os.path.join(PCAP_DIR, "abnormal_disconnect.pcap")
TSHARK = r"C:\Program Files\Wireshark\tshark.exe"

MSG_TYPES = {
    1: "CONNECT", 2: "CONNACK", 3: "PUBLISH", 4: "PUBACK",
    5: "PUBREC", 6: "PUBREL", 7: "PUBCOMP", 8: "SUBSCRIBE",
    9: "SUBACK", 10: "UNSUBSCRIBE", 11: "UNSUBACK",
    12: "PINGREQ", 13: "PINGRESP", 14: "DISCONNECT"
}

CSV_FIELDS = [
    "time_epoch", "src", "dst",
    "msg_type", "msg_type_name",
    "qos", "topic", "length"
]
# =============================


def run_tshark():
    """
    调用 tshark，返回:
    - packets: 用于写 CSV 的 dict 列表
    - msg_types: 用于统计的消息类型名列表
    """
    cmd = [
        TSHARK,
        "-r", PCAP_FILE,
        "-Y", "tcp.port==1883",
        "-T", "fields",
        "-e", "frame.time_epoch",
        "-e", "ip.src",
        "-e", "ip.dst",
        "-e", "mqtt.msgtype",
        "-e", "mqtt.qos",
        "-e", "mqtt.topic",
        "-e", "mqtt.len"
    ]

    print(">>> 执行 tshark ...")
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    packets = []
    msg_types = []

    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue

        cols = line.split("\t")

        try:
            msg_type = int(cols[3]) if len(cols) > 3 and cols[3].strip() else 0
        except ValueError:
            msg_type = 0

        msg_type_name = MSG_TYPES.get(msg_type, f"UNKNOWN({msg_type})")
        msg_types.append(msg_type_name)

        packets.append({
            "time_epoch": cols[0] if len(cols) > 0 else "",
            "src": cols[1] if len(cols) > 1 else "",
            "dst": cols[2] if len(cols) > 2 else "",
            "msg_type": msg_type,
            "msg_type_name": msg_type_name,
            "qos": cols[4] if len(cols) > 4 else "",
            "topic": cols[5] if len(cols) > 5 else "",
            "length": cols[6] if len(cols) > 6 else ""
        })

    return packets, msg_types


def print_report(packets, msg_types):
    total = len(packets)
    counter = Counter(msg_types)

    print("\n" + "=" * 60)
    print("📊 MQTT 报文分析报告")
    print("=" * 60)
    print(f"📁 文件: {os.path.basename(PCAP_FILE)}")
    print(f"✅ MQTT 报文数: {total}\n")

    print("-" * 60)
    print("📋 消息类型分布")
    print("-" * 60)
    max_cnt = max(counter.values(), default=1)
    for name, cnt in counter.most_common():
        bar = "█" * int(cnt / max_cnt * 20)
        print(f"  {name:<14}: {cnt:>3}  {bar}")
    print()

    print("-" * 60)
    print("📋 发布主题 TOPIC 统计")
    print("-" * 60)
    topics = [p["topic"] for p in packets if p["topic"]]
    for t, c in Counter(topics).most_common():
        print(f"  {t:<40}: {c}")
    print()

    print("-" * 60)
    print("🔍 异常检测")
    print("-" * 60)

    pub = counter.get("PUBLISH", 0)
    puback = counter.get("PUBACK", 0)
    disc = counter.get("DISCONNECT", 0)
    ping = counter.get("PINGREQ", 0)

    if pub == puback:
        print("  ✅ PUBLISH 与 PUBACK 数量一致，QoS1 确认完整")
    else:
        print(f"  ⚠️  PUBLISH({pub}) ≠ PUBACK({puback})，存在未确认消息")

    if disc:
        print(f"  ✅ 存在 DISCONNECT 报文 ({disc} 条)")
    else:
        print("  ⚠️  未发现 DISCONNECT 报文")

    if ping:
        print(f"  ℹ️  检测到 {ping} 条 PINGREQ（心跳包）")

    print()

    print("-" * 60)
    print("📋 全部报文明细")
    print("-" * 60)
    for i, p in enumerate(packets, 1):
        print(f"  [{i:>3}] {p['msg_type_name']:<14} "
              f"QoS={p['qos']:<3} topic={p['topic']}")
    print()

    # ===== 写 CSV =====
    csv_path = os.path.join(PCAP_DIR, "analysis_result.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(packets)

    print(f"📁 详细结果已保存到: {csv_path}")
    print("=" * 60)
    print("✅ 分析完成")
    print("=" * 60)


def main():
    print("=" * 60)
    print("🔬 MQTT 协议分析器（基于 tshark 命令行 · 最终稳定版）")
    print("=" * 60)
    print(f"📁 pcap: {PCAP_FILE}")
    print(f"🔧 tshark: {TSHARK}\n")

    if not os.path.exists(TSHARK):
        print("❌ 找不到 tshark，请检查 Wireshark 安装路径")
        return
    if not os.path.exists(PCAP_FILE):
        print("❌ 找不到 pcap 文件")
        return

    packets, msg_types = run_tshark()
    print(f">>> 解析到 {len(packets)} 条 MQTT 报文\n")

    print_report(packets, msg_types)


if __name__ == "__main__":
    main()