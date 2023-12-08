# Apigee To Postman

Apigee to Postman is a Python-based tool that connects to Apigee using your Google Auth token, downloads a specific API proxy based on your command, and efficiently converts it into a Postman collection. 
This tool is designed to save time and reduce manual effort by automating the conversion process, allowing you to convert  Apigee proxy to Postman collections within seconds.


## Key Features

- **Google Auth Token Integration**: Connect seamlessly to Apigee using your Google Auth token.
- **Proxy-Specific Conversion**: Download and convert a specific API proxy to a Postman collection with a single command.
- **Rapid Conversion**: Efficiently convert one Apigee API proxy to a Postman collection within seconds.


## Installation

Follow these steps to set up Apigee to Postman CLI:

### 1. **Google Cloud Authentication:**
   - Make sure you have the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed on your machine.
   - follow the steps in the documentation
   - Run the following command to make sure you have GAuth token:
```shell
gcloud auth print-access-token
```

   - Follow the next process once you receive confirmation that you have the GAuth token

### 2.Clone and Navigate to the Project:
   ```shell
git clone [https://github.com/nikhild28/apigee2postman-tool.git](https://github.com/Nikhil-d-963/Apigee2Postman-Tool.git)
```
```shell
cd apigee2postman-tool
```


### 3. Install Python and Dependencies:
   - Make sure you have Python 3.10.12 or a greater version installed. You can check your Python version with:

```shell
python3 --version
```

#### If Python is not installed, you can download it from [python.org](https://www.python.org/downloads/).
   - Make sure you have pip installed:
 ```shell
python3 -m pip --version
```

- If not, install pip using:

 ```shell
sudo apt install python3-pip
```

#### Install Required Python Packages:

  ```shell
pip install -r requirements.txt
```
****************************************************************************************************************************************************************************************************************************************************

# Usage
### 1. You can use downloadProxyFromApigee.py in two ways

#### A. Just run bellow command
```python
python3 downloadProxyFromApigee.py download
```
#### It will automatically prompt for all the details and carry out the process.

 ## OR

#### B. Download Proxy

##### To download an API proxy from Apigee, use the following command syntax:

```python
python3 script_name.py download --organization ABCD --api_name <API-NAME> --revision <revision>
```
##### Example command for downloading a proxy:

```python
python3 downloadProxyFromApigee.py download --organization abcd-apigee --api_name ABCD-API --revision 12
```


### 2.  **Make Postman Collection**

##### To convert the downloaded API proxy to a Postman collection, use the following command syntax:

   ```python
python3 script_name.py
```
##### Example command for making a Postman collection:

```python
python3 makePostmanCollection.py
```

  ### You will find postman collection in the **PostmanCollections** folder
