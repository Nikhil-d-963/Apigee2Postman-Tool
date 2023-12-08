import json
import os
from datetime import datetime
from tqdm import tqdm  # Import tqdm for the progress bar
import shutil

def extract_endpoints(json_data, base_path):
    endpoints = []

    if "Flows" in json_data["ProxyEndpoint"]:
        flows = json_data["ProxyEndpoint"]["Flows"]["Flow"]
        for flow in flows:
            if "Condition" in flow and "Request" in flow:
                condition = flow["Condition"]
                request = flow["Request"]
                if condition and request:
                    if isinstance(request["Step"], list):
                        method = request["Step"][0].get("Name", "")
                    else:
                        method = request.get("Step", {}).get("Name", "")
                    
                    path_suffix = condition.split("MatchesPath")[1].split("and")[0].strip()[1:-1].strip('"')
                    endpoint = f"{base_path}{path_suffix}"

                    verb = "GET" if "request.verb = \"GET\"" in condition else "POST"

                    # Extract API name from JSON
                    api_name = flow.get("@name", "")
                    
                    endpoints.append({"Endpoint": endpoint, "Verb": verb, "APIName": api_name})

    return endpoints

def extract_endpoints_from_json_file(file_path):
    with open(file_path, "r") as file:
        json_data = json.load(file)
    
    base_path = json_data["ProxyEndpoint"]["HTTPProxyConnection"]["BasePath"]
    return extract_endpoints(json_data, base_path)

def create_postman_collection(endpoints, target_server):
    postman_collection = {
        "info": {
            "name": "Collection Name",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": []
    }


    for endpoint in tqdm(endpoints, desc="Creating Postman Collection"):
        request = {
            "name": f"{endpoint['APIName']}",
            "request": {
                "method": endpoint["Verb"],
                "header": [],
                "url": {
                    "raw": f"{target_server}{endpoint['Endpoint']}",
                    "protocol": "https",
                    "host": [target_server],
                    "path": endpoint['Endpoint'].split("/")[1:],
                }
            },
            "response": [],
        }

        postman_collection["item"].append(request)

    return postman_collection

target_server = input("Enter the target server (e.g., google.com): ")

json_file_path = "./xml2jsonConvertedFile/default.json"
endpoints = extract_endpoints_from_json_file(json_file_path)

# Create Postman collection
postman_collection = create_postman_collection(endpoints, target_server)

timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
postman_collection_filename = f"PostmanCollection_{timestamp}.json"

# Destination folder
destination_folder = "PostmanCollections"
os.makedirs(destination_folder, exist_ok=True)

# Save the Postman collection
postman_collection_filepath = os.path.join(destination_folder, postman_collection_filename)
with open(postman_collection_filepath, "w") as file:
    json.dump(postman_collection, file, indent=2)

print(f"Postman collection created and saved as '{postman_collection_filename}' in the {destination_folder} folder.")
