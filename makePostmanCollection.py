import json
import os
from tqdm import tqdm

def clean_condition(condition):
    return condition.strip().replace('"', '').replace('(', '').replace(')', '')

def parse_paths_and_verb(conditions):
    pathsuffix = None
    verb = "Unknown"

    for condition in conditions:
        condition = clean_condition(condition)
        if 'MatchesPath' in condition:
            pathsuffix = condition.split('MatchesPath')[1].strip().strip('/').strip()

        if 'request.verb' in condition:
            verb = condition.split('=')[1].strip()

    return pathsuffix, verb

def extract_api_details(flow, http_proxy_connection):
    if 'Condition' in flow and flow['Condition']:
        name = flow.get('@name', '')
        description = flow.get('Description', '')
        request_details = flow.get('Request', {})
        response_details = flow.get('Response', {})
        conditions = clean_condition(flow['Condition']).split('and')

        pathsuffix, verb = parse_paths_and_verb(conditions)

        basepath = http_proxy_connection.get('BasePath', None)

        return {
            "name": name,
            "description": description,
            "verb": verb,
            "pathsuffix": "/" + pathsuffix,
            "basepath": basepath
        }

    return None

def process_flows(flows, http_proxy_connection):
    return [extract_api_details(flow, http_proxy_connection) for flow in flows if extract_api_details(flow, http_proxy_connection)]

def create_status_cure_json(input_json):
    flows = input_json.get("ProxyEndpoint", {}).get("Flows", {}).get("Flow", [])
    http_proxy_connection = input_json.get("ProxyEndpoint", {}).get("HTTPProxyConnection", {})

    return {"apis_details": process_flows(flows, http_proxy_connection)}

def create_postman_collection(endpoints, target_server, collection_name="Collection Name"):
    postman_collection = {
        "info": {
            "name": collection_name,
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": []
    }

    for endpoint in tqdm(endpoints, desc="Creating Postman Collection"):
        request = {
            "name": f"{endpoint['name']}",
            "request": {
                "method": endpoint["verb"],
                "header": [],
                "url": {
                    "raw": f"{target_server}{endpoint['basepath']}{endpoint['pathsuffix']}",
                    "protocol": "https",
                    "host": [target_server],
                    "path": [endpoint['basepath']] + endpoint['pathsuffix'].split("/")[1:],
                }
            },
            "response": [],
        }

        postman_collection["item"].append(request)

    return postman_collection

# Load input JSON
folder_path = './xml2jsonConvertedFile'
input_json_file_path = os.path.join(folder_path, 'default.json')

with open(input_json_file_path, 'r') as file:
    input_json = json.load(file)

# Validate input JSON format
flows = input_json.get("ProxyEndpoint", {}).get("Flows", {}).get("Flow", [])
http_proxy_connection = input_json.get("ProxyEndpoint", {}).get("HTTPProxyConnection", {})

if not flows or not http_proxy_connection:
    print("Invalid input JSON format. Exiting.")
    exit()

# Process and generate output
status_cure_json = create_status_cure_json(input_json)
endpoints = status_cure_json.get("apis_details", [])

# Update the target server as needed
target_server = "{{domaine}}"

# Create the Postman Collection
collection_name = input("Enter your collection name:")
postman_collection = create_postman_collection(endpoints, target_server, collection_name)

# Destination folder
destination_folder = 'PostmanCollections'
postman_collection_filename = collection_name + '.json'

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Save the Postman Collection
postman_collection_file_path = os.path.join(destination_folder, postman_collection_filename)
with open(postman_collection_file_path, 'w') as postman_collection_file:
    json.dump(postman_collection, postman_collection_file, indent=2)

print(f"Postman collection created and saved as '{postman_collection_filename}' in the {destination_folder} folder.")


