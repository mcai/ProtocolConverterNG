import asyncio
from pymodbus.server.async_io import StartAsyncTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock

async def start_mock_ups():
    # 配置Modbus数据存储
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17]*100),  # 离散输入
        co=ModbusSequentialDataBlock(0, [17]*100),  # 线圈
        hr=ModbusSequentialDataBlock(0, [10]*100),  # 保持寄存器
        ir=ModbusSequentialDataBlock(0, [17]*100))  # 输入寄存器
    context = ModbusServerContext(slaves=store, single=True)

    # 配置Modbus设备标识
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'mockups'  # 供应商名称
    identity.ProductCode = 'UPS'  # 产品代码
    identity.VendorUrl = 'http://github.com/mockups/'  # 供应商网址
    identity.ProductName = 'Mock UPS'  # 产品名称
    identity.ModelName = 'Mock UPS Model'  # 型号名称
    identity.MajorMinorRevision = '1.0'  # 版本号

    # 运行Modbus服务器
    await StartAsyncTcpServer(context, identity=identity, address=("localhost", 5020))

if __name__ == "__main__":
    asyncio.run(start_mock_ups())