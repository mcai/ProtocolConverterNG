# mock_devices/mock_ups.py
import asyncio
from pymodbus.server.async_io import StartAsyncTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock

async def start_mock_ups():
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17]*100),
        co=ModbusSequentialDataBlock(0, [17]*100),
        hr=ModbusSequentialDataBlock(0, [10]*10),  # Mock data
        ir=ModbusSequentialDataBlock(0, [17]*100))
    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'mockups'
    identity.ProductCode = 'UPS'
    identity.VendorUrl = 'http://github.com/mockups/'
    identity.ProductName = 'Mock UPS'
    identity.ModelName = 'Mock UPS Model'
    identity.MajorMinorRevision = '1.0'

    await StartAsyncTcpServer(context, identity=identity, address=("localhost", 5020))

if __name__ == "__main__":
    asyncio.run(start_mock_ups())