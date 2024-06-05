# server.py

import threading
import asyncio
from pymodbus.server.async_io import StartAsyncTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from shared_buffer import shared_buffer, buffer_lock
from device_ups import read_ups_data
from device_sensor import read_sensor_data
from pymodbus.datastore import ModbusSparseDataBlock

class SharedBufferDataBlock(ModbusSparseDataBlock):
    def __init__(self):
        super().__init__()

    async def getValues(self, address, count=1):
        async with buffer_lock:  # 使用异步锁进行线程安全访问
            values = []
            if 0 <= address < 10:
                values = shared_buffer["UPS"][address:address+count]  # 读取UPS数据
            elif 10 <= address < 20:
                values = shared_buffer["Sensor"][address-10:address-10+count]  # 读取传感器数据
            return values

async def start_server():
    # 配置Modbus数据存储
    store = ModbusSlaveContext(
        di=None,
        co=None,
        hr=SharedBufferDataBlock(),  # 使用共享缓冲区数据块
        ir=None
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

    # 创建线程读取UPS和传感器数据
    ups_thread = threading.Thread(target=read_ups_data)
    sensor_thread = threading.Thread(target=read_sensor_data)

    ups_thread.start()
    sensor_thread.start()

    # 启动异步TCP服务器
    await StartAsyncTcpServer(context, identity=identity, address=("localhost", 5022))

if __name__ == "__main__":
    asyncio.run(start_server())