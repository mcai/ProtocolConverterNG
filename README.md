# Modbus Protocol Converter Project

This project demonstrates how to create a Modbus server that aggregates data from multiple devices, maps their data into a shared buffer, and exposes this buffer via Modbus to a remote console. Mock devices (UPS and Sensor) are also included for testing purposes.

## Project Structure

```
modbus_project/
├── server.py
├── client.py
├── devices/
│   ├── __init__.py
│   ├── ups.py
│   └── sensors.py
├── mock_devices/
│   ├── __init__.py
│   ├── mock_ups.py
│   └── mock_sensor.py
├── .gitignore
└── shared_buffer.py
```

## Prerequisites

- Python 3.6 or higher
- `pymodbus` library

You can install the `pymodbus` library using pip:

```bash
pip install pymodbus
```

## Setup Instructions

1. **Clone the repository** (if applicable) or download the project files.

2. **Install the required Python packages**:

   ```bash
   pip install pymodbus
   ```

3. **Run the Modbus Server**:

   Execute the `server.py` script to start the Modbus server, along with the mock UPS and sensor servers.

   ```bash
   python server.py
   ```

4. **Run the Modbus Client**:

   In a new terminal window, execute the `client.py` script to connect to the Modbus server and read data from the mock devices.

   ```bash
   python client.py
   ```

## Project Components

### `server.py`

- Starts the main Modbus server that aggregates data from mock UPS and sensor servers.
- Reads data from the mock devices and stores it in a shared buffer.
- Exposes the data in the shared buffer via Modbus.

### `client.py`

- Connects to the main Modbus server and reads data from the shared buffer.
- Demonstrates how to query the server for data from UPS and sensors.

### `devices/`

- `ups.py`: Contains the function to read data from the mock UPS server.
- `sensors.py`: Contains the function to read data from the mock sensor server.

### `mock_devices/`

- `mock_ups.py`: Starts a mock Modbus server simulating a UPS device.
- `mock_sensor.py`: Starts a mock Modbus server simulating a sensor device.

### `shared_buffer.py`

- Defines the shared buffer and a lock for thread-safe access.

### `.gitignore`

- Specifies files and directories to be ignored by Git.

## Testing the Setup

1. Start the Modbus server by running `server.py`.
2. In a separate terminal, run `client.py` to read and verify data from the Modbus server.

This setup allows you to simulate a Modbus communication system with multiple devices, providing a framework to develop and test Modbus applications without requiring physical devices.