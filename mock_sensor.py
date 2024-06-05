# mock_sensor.py

import asyncio
import random
from datetime import datetime
from pymodbus.server.async_io import StartAsyncTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock, ModbusSparseDataBlock

# 定义一个协程来定期更新保持寄存器的值
async def update_holding_registers(sparse_block):
    while True:
        # 随机化保持寄存器中的值
        for address in range(100):
            value = random.randint(0, 100)  # 生成0到100之间的随机值
            sparse_block.setValues(address, [value])
        await asyncio.sleep(5)  # 每5秒更新一次

# 启动模拟传感器服务器
async def start_mock_sensor():
    # 创建一个稀疏数据块用于保持寄存器
    sparse_data = {i: 20 for i in range(100)}
    sparse_block = ModbusSparseDataBlock(sparse_data)

    # 配置Modbus数据存储
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [18]*100),  # 离散输入
        co=ModbusSequentialDataBlock(0, [18]*100),  # 线圈
        hr=sparse_block,  # 保持寄存器
        ir=ModbusSequentialDataBlock(0, [18]*100)   # 输入寄存器
    )
    context = ModbusServerContext(slaves=store, single=True)

    # 配置Modbus设备标识
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'mocksensor'  # 供应商名称
    identity.ProductCode = 'Sensor'  # 产品代码
    identity.VendorUrl = 'http://github.com/mocksensor/'  # 供应商网址
    identity.ProductName = 'Mock Sensor'  # 产品名称
    identity.ModelName = 'Mock Sensor Model'  # 型号名称
    identity.MajorMinorRevision = '1.0'  # 版本号

    # 打印欢迎信息
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{current_time} - 欢迎使用 Mock Sensor 服务器！服务器正在localhost:5021运行...")

    # 启动后台任务来更新保持寄存器
    asyncio.create_task(update_holding_registers(sparse_block))

    # 运行Modbus服务器
    await StartAsyncTcpServer(context, identity=identity, address=("localhost", 5021))

if __name__ == "__main__":
    asyncio.run(start_mock_sensor())