# mock_devices/mock_ups.py
from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock

def start_mock_ups():
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

    StartTcpServer(context, identity=identity, address=("localhost", 5020))
