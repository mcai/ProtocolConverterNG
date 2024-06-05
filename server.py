# server.py
import threading
from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from shared_buffer import shared_buffer, buffer_lock
from devices.ups import read_ups_data
from devices.sensors import read_sensor_data
from pymodbus.datastore import ModbusSparseDataBlock
from mock_devices.mock_ups import start_mock_ups
from mock_devices.mock_sensor import start_mock_sensor

class SharedBufferDataBlock(ModbusSparseDataBlock):
    def __init__(self):
        super().__init__()

    def getValues(self, address, count=1):
        with buffer_lock:
            values = []
            if 0 <= address < 10:
                values = shared_buffer["UPS"][address:address+count]
            elif 10 <= address < 20:
                values = shared_buffer["Sensors"][address-10:address-10+count]
            return values

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

# Start threads for reading from devices
threading.Thread(target=read_ups_data, daemon=True).start()
threading.Thread(target=read_sensor_data, daemon=True).start()

# Start mock devices
threading.Thread(target=start_mock_ups, daemon=True).start()
threading.Thread(target=start_mock_sensor, daemon=True).start()

# Start the Modbus server
StartTcpServer(context, identity=identity, address=("localhost", 5022))
