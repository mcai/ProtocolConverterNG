# shared_buffer.py
import threading

# Shared buffer
shared_buffer = {
    "UPS": [0] * 10,
    "Sensors": [0] * 10
}

# Lock for thread-safe access to the buffer
buffer_lock = threading.Lock()
