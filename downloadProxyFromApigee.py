import argparse
import subprocess
import requests
import os
from datetime import datetime
import zipfile
import shutil
import xmltodict
import json
import sys
from tqdm import tqdm
import subprocess
from tqdm import tqdm
import sys

DOWNLOAD_FOLDER = 'downloadedXmlFiles'
CONVERTED_FOLDER = 'xml2jsonConvertedFile'



def get_access_token():
    try:
        # Use tqdm to create a progress bar
        with tqdm(total=100, desc="Retrieving access token", unit="%", bar_format="{desc}: {percentage:3.0f}%|{bar}|") as pbar:
            result = subprocess.run(['gcloud', 'auth', 'print-access-token'], stdout=subprocess.PIPE, check=True, text=True)
            # Update the progress bar to 100% when the subprocess completes
            pbar.update(100)

        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f'Error retrieving access token: {e}')
        sys.exit(1)

def download_proxy(organization, api_key, api_name, revision):
    if not api_key:
        api_key = get_access_token()

    url = f'https://apigee.googleapis.com/v1/organizations/{organization}/apis/{api_name}/revisions/{revision}?format=bundle'
    headers = {'Authorization': f'Bearer {api_key}'}

    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        zip_filename = f'api_bundle_{timestamp}.zip'
        zip_file_path = os.path.join(DOWNLOAD_FOLDER, zip_filename)

        os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

        total_size = int(response.headers.get('content-length', 0))

        try:
            with open(zip_file_path, 'wb') as file, tqdm(
                    desc=f"Downloading {zip_filename}",
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    bar.update(len(data))

            print(f'Download complete. File saved as {zip_filename} in the {DOWNLOAD_FOLDER} folder.')

            extract_and_convert(zip_file_path)

        except KeyboardInterrupt:
            print("\nDownload interrupted. Cleaning up...")
            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)
            sys.exit(1)
    else:
        print(f'Error: {response.status_code} - {response.text}')

def extract_and_convert(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        os.makedirs(CONVERTED_FOLDER, exist_ok=True)

        total_size = sum(file.file_size for file in zip_ref.infolist())

        with tqdm(
                desc=f"Unzipping {zip_file_path}",
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for file in zip_ref.infolist():
                zip_ref.extract(file, DOWNLOAD_FOLDER)
                bar.update(file.file_size)

    default_xml_path = os.path.join(DOWNLOAD_FOLDER, 'apiproxy', 'proxies', 'default.xml')
    destination_json_path = os.path.join(CONVERTED_FOLDER, 'default.json')

    if os.path.exists(default_xml_path):
        with open(default_xml_path, 'r') as xml_file:
            xml_dict = xmltodict.parse(xml_file.read(), force_list=('key',))
            json_data = json.dumps(xml_dict, indent=2)

        with open(destination_json_path, 'w') as json_file:
            json_file.write(json_data)

        print(f'Converted to JSON and moved to {CONVERTED_FOLDER} directory successfully.')
    else:
        print('Error: default.xml not found in the extracted folder.')

def main():
    parser = argparse.ArgumentParser(description='Download and convert Apigee proxy to JSON.')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Command: download
    parser_download = subparsers.add_parser('download', help='Download Apigee proxy')
    parser_download.add_argument('--organization', type=str, help='Apigee organization name')
    parser_download.add_argument('--api_name', type=str, help='Apigee API name')
    parser_download.add_argument('--revision', type=str, help='Apigee API revision')

    # Command: help
    parser_help = subparsers.add_parser('help', help='Show help message for a command')
    parser_help.add_argument('command_name', type=str, nargs='?', help='Name of the command to show help for')

    args = parser.parse_args()

    if args.command == 'download':
        if args.organization is None:
            args.organization = input('Enter Apigee organization name: ')
        if args.api_name is None:
            args.api_name = input('Enter Apigee API name: ')
        if args.revision is None:
            args.revision = input('Enter Apigee API revision: ')

        download_proxy(args.organization, None, args.api_name, args.revision)
    elif args.command == 'help':
        if args.command_name:
            subparsers.choices[args.command_name].print_help()
        else:
            parser.print_help()
            # A. Command syntax for Download proxy
            print("\n" + "-" * 50 + "\n")
            print("\nUsage: python3 script_name.py download --organization <ORG_NAME> --api_name <API-NAME> --revision <REVISION>")
            
            print("\nExample:")
            print("python3 downloadProxyFromApigee.py download --organization abcd-apigee --api_name abcd-API --revision 12")
            print("\n" + "-" * 50 + "\n")
            print("\nSimplified Command:")
            print("python3 downloadProxyFromApigee.py download")
            print("\n" + "-" * 50 + "\n")

    else:
        print(f'Error: Unknown command - {args.command}')

if __name__ == "__main__":
    main()
