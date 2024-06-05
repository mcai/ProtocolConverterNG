# mock_devices/mock_sensor.py
from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock

def start_mock_sensor():
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

    StartTcpServer(context, identity=identity, address=("localhost", 5021))
