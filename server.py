# server.py
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
        async with buffer_lock:
            values = []
            if 0 <= address < 10:
                values = shared_buffer["UPS"][address:address+count]
            elif 10 <= address < 20:
                values = shared_buffer["Sensors"][address-10:address-10+count]
            return values

async def start_server():
    # Configure the Modbus server
    store = ModbusSlaveContext(
        di=None,
        co=None,
        hr=SharedBufferDataBlock(),
        ir=None
    )
    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'
    identity.ProductName = 'pymodbus Server'
    identity.ModelName = 'pymodbus Server'
    identity.MajorMinorRevision = '1.0'

    # Start tasks for reading from devices
    asyncio.create_task(read_ups_data())
    asyncio.create_task(read_sensor_data())

    # Start the Modbus server
    await StartAsyncTcpServer(context, identity=identity, address=("localhost", 5022))

if __name__ == "__main__":
    asyncio.run(start_server())