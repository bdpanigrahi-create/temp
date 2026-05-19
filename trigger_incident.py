import urllib.request
import time
import uuid

url = "http://localhost:8080/process?tx_id="

print("Starting to trigger incident...")
print("This will send requests to the billing processor to cause memory growth.")

try:
    for i in range(5000): # 5000 * 1MB = ~5GB if all held in memory, should trigger issues or at least high usage
        tx_id = str(uuid.uuid4())
        try:
            with urllib.request.urlopen(url + tx_id) as response:
                content = response.read()
                if i % 100 == 0:
                    print(f"Sent {i} requests. {content.decode()}")
        except Exception as e:
            print(f"Error sending request on iteration {i}: {e}")
            time.sleep(0.5)
except KeyboardInterrupt:
    print("\nStopped by user")
