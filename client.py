# client.py

from pymodbus.client import ModbusTcpClient

# 创建Modbus TCP客户端并连接到服务器
client = ModbusTcpClient('localhost', port=5020)
client.connect()

# 读取UPS数据的保持寄存器（地址0-9）
result = client.read_holding_registers(0, 10)
if not result.isError():
    print(f"UPS数据: {result.registers}")  # 输出UPS数据
else:
    print("读取UPS数据出错")  # 输出读取错误信息

# 读取传感器数据的保持寄存器（地址10-19）
result = client.read_holding_registers(10, 10)
if not result.isError():
    print(f"传感器数据: {result.registers}")  # 输出传感器数据
else:
    print("读取传感器数据出错")  # 输出读取错误信息

# 关闭客户端连接
client.close()