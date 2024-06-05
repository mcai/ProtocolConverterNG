# client.py
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('localhost', port=5020)
client.connect()

# Read holding registers for UPS data (addresses 0-9)
result = client.read_holding_registers(0, 10)
if not result.isError():
    print(f"UPS Data: {result.registers}")
else:
    print("Error reading UPS data")

# Read holding registers for Sensor data (addresses 10-19)
result = client.read_holding_registers(10, 10)
if not result.isError():
    print(f"Sensor Data: {result.registers}")
else:
    print("Error reading Sensor data")

client.close()
