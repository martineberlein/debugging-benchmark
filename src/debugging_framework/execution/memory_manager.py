import psutil
import os
import threading
import signal
import time


class ManageMemory:
    def __init__(self, max_memory: float):
        self.max_memory = max_memory
        self.memory_check_thread = threading.Thread(target=self.check_memory_usage)
        self.stop_event = threading.Event()

    def check_memory_usage(self):
        while not self.stop_event.is_set():
            process = psutil.Process(os.getpid())
            memory_usage = process.memory_info().rss / (1024 * 1024)  # Memory in MB
            if memory_usage > self.max_memory:
                os.kill(os.getpid(), signal.SIGTERM)  # Send SIGTERM to the process
            time.sleep(0.1)  # Sleep for a short time and then check again

    def __enter__(self):
        signal.signal(signal.SIGTERM, self.raise_memory_error)  # Set signal handler
        self.memory_check_thread.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_event.set()
        self.memory_check_thread.join()
        signal.signal(signal.SIGTERM, signal.SIG_DFL)  # Reset default signal handler

    @staticmethod
    def raise_memory_error(signum, frame):
        raise MemoryError("Memory limit exceeded")


def sieveOfEratosthenes(N):
    is_prime = [True] * (N + 1)
    for i in range(2, N):
        if is_prime[i]:
            for j in range(i * i, N + 1, i):
                is_prime[j] = False

    # Get the list of primes
    result = []
    for i in range(2, N + 1):
        if is_prime[i]:
            result.append(i)
    return result


if __name__ == "__main__":
    # Usage example
    try:
        with ManageMemory(max_memory=10):  # Set max memory usage to 100 MB
            print(sieveOfEratosthenes(4713133176770))
    except MemoryError as e:
        print("Memory Leak Detected")
