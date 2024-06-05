# shared_buffer.py

import threading

# 用于线程安全访问缓冲区的锁
buffer_lock = threading.Lock()