import csv

data = [
    {"city_name": "New York City", "population": 8336000, "state": "New York"},
    {"city_name": "Los Angeles", "population": 3822000, "state": "California"},
    {"city_name": "Chicago", "population": 2665000, "state": "Illinois"},
    {"city_name": "Houston", "population": 2303000, "state": "Texas"},
    {"city_name": "Miami", "population": 449514, "state": "Florida"},
    {"city_name": "Seattle", "population": 749256, "state": "Washington"},
]

with open('city_stats.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["city_name", "population", "state"])
    writer.writeheader()
    writer.writerows(data)