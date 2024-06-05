# mock_sensor.py

import asyncio
from pymodbus.server.async_io import StartAsyncTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock

async def start_mock_sensor():
    # 配置Modbus数据存储
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [18]*100),  # 离散输入
        co=ModbusSequentialDataBlock(0, [18]*100),  # 线圈
        hr=ModbusSequentialDataBlock(0, [20]*100),  # 保持寄存器
        ir=ModbusSequentialDataBlock(0, [18]*100))  # 输入寄存器
    context = ModbusServerContext(slaves=store, single=True)

    # 配置Modbus设备标识
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'mocksensor'  # 供应商名称
    identity.ProductCode = 'Sensor'  # 产品代码
    identity.VendorUrl = 'http://github.com/mocksensor/'  # 供应商网址
    identity.ProductName = 'Mock Sensor'  # 产品名称
    identity.ModelName = 'Mock Sensor Model'  # 型号名称
    identity.MajorMinorRevision = '1.0'  # 版本号

    # 定义日志记录函数
    def log_request(request):
        print(f"Request received: {request}")

    # 异步请求处理器
    async def request_handler(context):
        while True:
            await asyncio.sleep(1)  # 设置睡眠间隔
            log_request(context[0].getValues(3, 0, count=10))  # 获取保持寄存器的值

    # 并发运行Modbus服务器和请求处理器
    await asyncio.gather(
        StartAsyncTcpServer(context, identity=identity, address=("localhost", 5021)),
        request_handler(context)
    )

if __name__ == "__main__":
    asyncio.run(start_mock_sensor())