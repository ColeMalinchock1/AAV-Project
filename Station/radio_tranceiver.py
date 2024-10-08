# Use pyrf24 https://pypi.org/project/pyrf24/

import time
from RF24 import RF24, RPI_V2_GPIO, RF24_PA_LOW, RF24_1MBPS

radio = RF24(22, 0)

address = [b"1Node", b"2Node"]

def setup_radio():
    radio.begin()
    radio.setPALevel(RF24_PA_LOW)
    radio.setDataRate(RF24_1MBPS)
    radio.setChannel(76)
    radio.openWriingPipe(address[1])
    radio.openReadingPipe(1, address[0])
    radio.startListening()

def send_message(message):
    radio.stopListening()
    success = radio.write(message.encode('utf-8'))
    radio.startListening()
    if success:
        print(f"Sent: {message}")
    else:
        print("Send failed!")

def receive_message():
    if radio.available():
        received_payload = []
        radio.read(received_payload, radio.getDynamicPayloadSize())
        received_message = "".join(chr(i) for i in received_payload)
        print(f"Received: {received_message}")

if __name__ == "__main__":
    setup_radio()

    while True:
        send_message("Hello from Pi 1!")

        time.sleep(2)

        receive_message()

        time.sleep(2)
