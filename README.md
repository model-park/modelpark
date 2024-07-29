
# ModelPark

ModelPark provides a versatile platform to share and manage your ML models directly from your machine, offering a convenient Python API to manage these tasks programmatically, including controlling access and publishing applications.

This library provides a more Pythonic way of managing your applications with [ModelPark](https://modelpark.app/)  compared to using the CLI directly.

See [ModelPark](https://modelpark.app/) website and platform for more details.

![image](https://github.com/model-park/modelpark/assets/25637056/6eac80e7-91e9-477a-bcce-bd7d369d932e)

![image](https://github.com/model-park/modelpark/assets/25637056/be495106-915d-4989-818d-dad7bb5abc71)

## Features

- Share models directly from the Python API.
- Publish and manage applications using the ModelPark Python API.
- Configure access management according to your needs through Python methods.

## Installation

To install ModelPark, you can use pip:
```bash
pip install modelpark
```

## Configuration

Ensure Python and pip are installed on your machine. This API interfaces with the ModelPark CLI but manages interactions programmatically through Python.

## Usage

Here's how you can use the ModelPark Python package:

### Initialize and Login
```python
from modelpark import ModelPark

mp = ModelPark() # downloads the modelpark CLI binary/ executable to your home folder as "~/modelpark'
mp.login(username="your_username", password="your_password")
mp.init()
```

#### clear cache while init (remove existing modelpark CLI binaries from system)
```python
from modelpark import ModelPark

mp = ModelPark(clear_cache=True)
```

### Register an Application 

#### Register an app running on a certain port
```python
mp.register(port=3000, name="my-app", access="public") 
# access='private' if private (not visible/ accessible in modelpark dashboard)
```
#### Register a password protected app running on a certain port

```python
mp.register_port(port=3000, name="my-app", access="public", password='123')
```

#### Register an app running on a certain port

```python
mp.register_port(port=3000, name="my-app", access="public")
```

#### Register a streamlit app that is not run yet (this starts the app as well)
```python
mp.run_with_streamlit_and_register(port=3000, name="my-app", file_path="~/my-app/streamlit-app.py", access="public", framework="streamlit")
# generic registration also works >> 
# mp.register(port=3000, name="my-app", file_path="~/my-app/streamlit-app.py", access="public", framework="streamlit")

```

#### Register a streamlit app that is not run yet 
```python
mp.register(port=3000, name="my-app", file_path="~/my-app/streamlit-app.py", access="public", framework="streamlit")
```

#### Register a Fast API app while deploying 
add `register_port` within startup_event() function in FAST API app
```python
@app.on_event("startup")
async def startup_event():
    mp.register_port(port=5000, name="my-fast-api", access="public") 
```    

### List Registered Applications
```python
mp.ls()
# or mp.status()
```

### Stop and Logout
```python
mp.stop()
mp.logout()
```

### Kill an Application
```python
mp.kill(name="my-app")
```

### Kill all the registrations in this session
```python
mp.kill(all=True)
```


### Make an API Call to a Registered Application 
```python
from modelpark import APIManager
mp_api = APIManager()

user_credentials = {'username': 'your_username', 'password': 'your_password'}
app_name = 'my-app'
extension = 'api_extension' # or None
password = 'psw' # or None if no password protection
request_payload = {'key': 'value'}  # Payload required by the application

# Make the API call
response = mp_api.make_api_call(app_name, user_credentials, request_payload=request_payload, password=password, extension=extension)
print(response.json())  # Assuming the response is in JSON format

# get an access token to hit a modelpark api endpoint

import requests

expire ='7d' # x days or None
password = '1234' # or None if no password protection
auth_token = mp_api.get_auth_token(user_credentials)
access_token = mp_api.get_access_token(app_name, auth_token, password=password, expire=expire)

headers = {
    "x-access-token": access_token}

query = {'key': 'value'} 

requests.get(url, headers=headers, params=query).json()
```


