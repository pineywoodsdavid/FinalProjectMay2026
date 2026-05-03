import paho.mqtt.client as mqtt
import xlwings as xw
import datetime

# MQTT settings
BROKER = "broker.hivemq.com"
PORT = 1883

TOPICS = [
    "cett14490001",
    "cett14490002"
]

# Map topics to columns (A=1, B=2, etc.)
TOPIC_COLUMNS = {
    topic: (i * 2) + 1 for i, topic in enumerate(TOPICS)
}

EXCEL_FILE = "mqtt_live_b.xlsx"

# Open Excel
try:
    wb = xw.Book(EXCEL_FILE)
except:
    wb = xw.Book()
    wb.save(EXCEL_FILE)

ws = wb.sheets[0]
ws.autofit()

# --- Setup headers (Row 1) ---
for i, topic in enumerate(TOPICS):
    col = (i * 2) + 1  # A=1, C=3, E=5, etc.
    
    ws.range((1, col)).value = topic
    ws.range((1, col + 1)).value = "Timestamp"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    for topic in TOPICS:
        client.subscribe(topic)

def get_next_row(sheet, col):
    # Start logging from row 3 (row 1 = header, row 2 = latest)
    last_row = sheet.range((sheet.cells.last_cell.row, col)).end("up").row
    return max(3, last_row + 1)

def on_message(client, userdata, msg):
    topic = msg.topic
    message = msg.payload.decode()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if topic not in TOPIC_COLUMNS:
        return

    col = TOPIC_COLUMNS[topic]

    # --- 1. Write to Row 2 (latest value snapshot) ---
    ws.range((2, col)).value = message
    ws.range((2, col + 1)).value = timestamp

    # --- 2. Append to history starting at Row 3 ---
    next_row = get_next_row(ws, col)
    ws.range((next_row, col)).value = message
    ws.range((next_row, col + 1)).value = timestamp

    print(f"{topic}: {message}")

# MQTT setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()