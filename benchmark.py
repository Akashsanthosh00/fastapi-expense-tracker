import statistics
import requests
import os

URL = "http://127.0.0.1:8000/expenses"

TOKEN = os.getenv("EXPENSE_TOKEN")

HEADERS = {
    "Authorization": f"BEARER {TOKEN}"
}


times = []

for i in range(20):
    response = requests.get(
        URL,
        headers=HEADERS,
        params={
            "page": 1,
            "limit": 10,
            "sort_by": "id",
            "order": "asc"
        }
    )

    print(f"Run {i + 1}: {response.elapsed.total_seconds() * 1000:.2f} ms")

    times.append(response.elapsed.total_seconds() * 1000)

print("\n--- Results ---")
print(f"Average : {statistics.mean(times):.2f} ms")
print(f"Median  : {statistics.median(times):.2f} ms")
print(f"Minimum : {min(times):.2f} ms")
print(f"Maximum : {max(times):.2f} ms")