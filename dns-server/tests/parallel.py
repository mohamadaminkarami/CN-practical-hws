import concurrent.futures
import subprocess
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5353


def run_dig_command():
    command = ["dig", f"@{SERVER_IP}", "-p", f"{SERVER_PORT}", "example.com"]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout


r = time.time()
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(run_dig_command) for _ in range(100)]

for result in concurrent.futures.as_completed(results):
    print(result.result())
print("Parallel Run time: ", time.time() - r)
