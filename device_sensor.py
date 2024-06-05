# device_sensor.py

import time
from datetime import datetime
from pymodbus.client import ModbusTcpClient
from shared_buffer import shared_buffer, buffer_lock

def read_sensor_data():
    # 创建Modbus TCP客户端并连接到服务器
    client = ModbusTcpClient('localhost', port=5021)
    client.connect()
    while True:
        try:
            print(f"{datetime.now()} - 传感器: 发送读取请求...")  # 发送读取请求
            result = client.read_holding_registers(0, 10)  # 请求前10个保持寄存器
            print(f"{datetime.now()} - 传感器: 收到响应: {result}")  # 输出响应结果
            if result.isError():
                raise Exception("读取传感器数据出错: " + str(result))  # 抛出读取错误异常
            with buffer_lock:  # 使用锁进行线程安全访问
                shared_buffer["Sensor"] = result.registers  # 更新共享缓冲区中的传感器数据
        except Exception as e:
            print(f"{datetime.now()} - 传感器: {e}")  # 输出异常信息
        time.sleep(1)  # 休眠1秒钟后再次读取