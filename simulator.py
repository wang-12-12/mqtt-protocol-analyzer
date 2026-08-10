import paho.mqtt.client as mqtt
import time
import random

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "vehicle/tbox/test"
CLIENT_ID = f"TBOX_{random.randint(1000,9999)}"

def on_connect(client, userdata, flags, rc):
    print(">>> on_connect 被调用，rc =", rc)
    if rc == 0:
        print("✅ MQTT 连接成功")
    else:
        print("❌ MQTT 连接失败")

def on_publish(client, userdata, mid):
    print("📤 PUBLISH 已发送，mid =", mid)

print("== MQTT 模拟器启动 ==")
print("CLIENT_ID =", CLIENT_ID)

client = mqtt.Client(client_id=CLIENT_ID)
client.on_connect = on_connect
client.on_publish = on_publish

print(f">>> 正在连接 {BROKER}:{PORT} ...")
client.connect(BROKER, PORT, keepalive=10)

client.loop_start()

for i in range(5):
    payload = f'{{"speed":{random.randint(0,120)}}}'
    print("发送:", payload)
    client.publish(TOPIC, payload, qos=1)
    time.sleep(2)

print(">>> 模拟结束")
client.loop_stop()
client.disconnect()