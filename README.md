# Modbus协议转换器项目

该项目演示了如何创建一个Modbus服务器，该服务器从多个设备汇总数据，将它们的数据映射到共享缓冲区，并通过Modbus将此缓冲区暴露给远程控制台。还包括用于测试的模拟设备（UPS和传感器）。

## 项目结构

```
ProtocolConverterNG/
├── server.py
├── client.py
├── device_sensor.py
├── device_ups.py
├── mock_sensor.py
├── mock_ups.py
├── shared_buffer.py
└── README.md
```

## 前提条件

- Python 3.6或更高版本
- `pymodbus`库

你可以使用pip安装`pymodbus`库：

```bash
pip install pymodbus
```

## 设置说明

1. **克隆存储库**（如果适用）或下载项目文件。

2. **安装所需的Python包**：

   ```bash
   pip install pymodbus
   ```

3. **启动模拟UPS和传感器服务器**：

   分别执行`mock_ups.py`和`mock_sensor.py`脚本以启动模拟服务器。

   在一个终端窗口中，运行：

   ```bash
   python mock_ups.py
   ```

   在另一个终端窗口中，运行：

   ```bash
   python mock_sensor.py
   ```

4. **运行Modbus服务器**：

   在新的终端窗口中，执行`server.py`脚本以启动Modbus服务器。

   ```bash
   python server.py
   ```

5. **运行Modbus客户端**：

   在新的终端窗口中，执行`client.py`脚本以连接到Modbus服务器并从模拟设备读取数据。

   ```bash
   python client.py
   ```

## 项目组件

### `server.py`

- 启动汇总来自模拟UPS和传感器服务器数据的主要Modbus服务器。
- 从模拟设备读取数据并将其存储在共享缓冲区中。
- 通过Modbus暴露共享缓冲区中的数据。

### `client.py`

- 连接到主要Modbus服务器并从共享缓冲区读取数据。
- 演示如何从UPS和传感器查询服务器数据。

### `device_sensor.py`

- 包含从模拟传感器服务器读取数据的函数。

### `device_ups.py`

- 包含从模拟UPS服务器读取数据的函数。

### `mock_sensor.py`

- 启动模拟Modbus服务器，模拟传感器设备。

### `mock_ups.py`

- 启动模拟Modbus服务器，模拟UPS设备。

### `shared_buffer.py`

- 定义共享缓冲区和用于线程安全访问的锁。

## 测试设置

1. 分别运行`mock_ups.py`和`mock_sensor.py`以启动模拟服务器。
2. 运行`server.py`启动Modbus服务器。
3. 在单独的终端中运行`client.py`以读取并验证来自Modbus服务器的数据。

此设置允许你模拟具有多个设备的Modbus通信系统，提供一个框架来开发和测试Modbus应用程序，而无需物理设备。