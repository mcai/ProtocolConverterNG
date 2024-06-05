# shared_buffer.py

import threading

# 共享缓冲区
shared_buffer = {
    "UPS": [0] * 10,  # UPS 数据
    "Sensors": [0] * 10  # 传感器数据
}

# 用于线程安全访问缓冲区的锁
buffer_lock = threading.Lock()