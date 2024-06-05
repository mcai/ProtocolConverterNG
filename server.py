# server.py

import threading
import asyncio
from pymodbus.server.async_io import StartAsyncTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from device_ups import read_ups_data
from device_sensor import read_sensor_data
from pymodbus.datastore import ModbusSparseDataBlock

async def start_server():
    # 初始化共享缓冲区数据块
    initial_values = {}
    for i in range(10):
        initial_values[i] = 0  # 初始值为0
    for i in range(10, 20):
        initial_values[i] = 0  # 初始值为0

    # 配置Modbus数据存储
    shared_buffer_block = ModbusSparseDataBlock(initial_values)
    store = ModbusSlaveContext(
        di=None,
        co=None,
        hr=shared_buffer_block,  # 使用共享缓冲区数据块
        ir=None,
        zero_mode=True
    )
    context = ModbusServerContext(slaves=store, single=True)

    # 配置Modbus设备标识
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'pymodbus'  # 供应商名称
    identity.ProductCode = 'PM'  # 产品代码
    identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'  # 供应商网址
    identity.ProductName = 'pymodbus Server'  # 产品名称
    identity.ModelName = 'pymodbus Server'  # 型号名称
    identity.MajorMinorRevision = '1.0'  # 版本号

    # 创建线程读取UPS和传感器数据，并传递共享缓冲区数据块
    ups_thread = threading.Thread(target=read_ups_data, args=(shared_buffer_block,))
    sensor_thread = threading.Thread(target=read_sensor_data, args=(shared_buffer_block,))

    ups_thread.start()
    sensor_thread.start()

    # 启动异步TCP服务器
    await StartAsyncTcpServer(context, identity=identity, address=("localhost", 5022))

if __name__ == "__main__":
    asyncio.run(start_server())