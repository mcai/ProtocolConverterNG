import time
from pymodbus.client import ModbusTcpClient
from shared_buffer import shared_buffer, buffer_lock

def read_ups_data():
    client = ModbusTcpClient('localhost', port=5020)
    client.connect()
    while True:
        result = client.read_holding_registers(0, 10)
        if result.isError():
            print("Error reading UPS data")
            time.sleep(1)
            continue
        with buffer_lock:
            shared_buffer["UPS"] = result.registers
        time.sleep(1)