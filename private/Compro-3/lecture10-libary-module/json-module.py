import json

data = {"name": "Alice", "age": 25}
json_str = json.dumps(data)
print(json_str)

parsed_data = json.loads(json_str)
print(parsed_data)
print(parsed_data["name"])
print(parsed_data["age"])