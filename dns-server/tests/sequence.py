import subprocess
import time


SERVER_IP = "127.0.0.1"
SERVER_PORT = 5353

r = time.time()
for _ in range(100):
    command = ["dig", f"@{SERVER_IP}", "-p", f"{SERVER_PORT}", "example.com"]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
print("Sequence Run time: ", time.time() - r)
