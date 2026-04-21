from machine import UART
import time

uart = UART(2, baudrate=9600, tx=17, rx=16)

PREFIX = "AZ"
SUFFIX = "BY"

MY_ID = "1"          # <<< CHANGE TO YOUR ID
TEAM_IDS = {"2","3","4","5", "6"}

buffer = ""

# ---------------------------------------------------------
# SEND PACKETS (ASCII)
# ---------------------------------------------------------
def send_packet(msg_type, receiver, *data):
    packet = PREFIX + msg_type + MY_ID + receiver + "".join(data) + SUFFIX
    uart.write(packet)
    print("SENT:", packet)

# ---------------------------------------------------------
# PROCESS COMPLETE PACKET
# ---------------------------------------------------------
def process_packet(packet):
    print("\n=== PACKET RECEIVED ===")
    print(packet)

    payload = packet[len(PREFIX):-len(SUFFIX)]

    if len(payload) < 3:
        print("ERROR: Payload too short")
        return

    msg_type = payload[0]
    sender   = payload[1]
    receiver = payload[2]
    data     = payload[3:]

    # ---- ERROR HANDLING (choose one for checkoff) ----
    if sender == MY_ID:
        print("ERROR: Message from myself — dropping")
        return

    if sender not in TEAM_IDS:
        print("ERROR: Unknown sender — dropping")
        return

    # ---- ROUTING ----
    if receiver == MY_ID:
        print(">>> MESSAGE FOR ME <<<")
        print("Type:", msg_type, "Data:", data)
    else:
        print(">>> FORWARDING <<<")
        uart.write(packet)

# ---------------------------------------------------------
# STREAMING ASCII READER
# ---------------------------------------------------------
def read_uart_ascii():
    global buffer

    if not uart.any():
        return

    raw = uart.read()

    # SAFE DECODE — prevents UnicodeError crashes
    chunk = raw.decode("utf-8", "ignore")

    if not chunk:
        return

    buffer += chunk

    while True:
        start = buffer.find(PREFIX)
        if start == -1:
            buffer = buffer[-4:]
            return

        end = buffer.find(SUFFIX, start + len(PREFIX))
        if end == -1:
            return

        packet = buffer[start:end+len(SUFFIX)]
        buffer = buffer[end+len(SUFFIX):]

        process_packet(packet)


# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
print("HMI READY (ASCII MODE)")

while True:
    read_uart()
    time.sleep_ms(5)
