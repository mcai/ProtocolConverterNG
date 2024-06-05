# mock_devices/mock_sensor.py
import asyncio
from pymodbus.server.async_io import StartAsyncTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock

async def start_mock_sensor():
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [18]*100),
        co=ModbusSequentialDataBlock(0, [18]*100),
        hr=ModbusSequentialDataBlock(0, [20]*10),  # Mock data
        ir=ModbusSequentialDataBlock(0, [18]*100))
    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'mocksensor'
    identity.ProductCode = 'Sensor'
    identity.VendorUrl = 'http://github.com/mocksensor/'
    identity.ProductName = 'Mock Sensor'
    identity.ModelName = 'Mock Sensor Model'
    identity.MajorMinorRevision = '1.0'

    await StartAsyncTcpServer(context, identity=identity, address=("localhost", 5021))

if __name__ == "__main__":
    asyncio.run(start_mock_sensor())