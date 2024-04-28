
# ModelPark

ModelPark provides a versatile platform to share and manage your ML models directly from your machine, offering a convenient Python API to manage these tasks programmatically, including controlling access and publishing applications.

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

mp = ModelPark()
mp.login(username="your_username", password="your_password")
mp.init()
```

### Register an Application
```python
mp.register(port=3000, name="my-app", file_path="~/my-app/streamlit-app.py", access="public", framework="streamlit")
```

### List Registered Applications
```python
mp.ls()
```

### Make an API Call to a Registered Application
```python
user_credentials = {'username': 'your_username', 'password': 'your_password'}
app_name = 'my-app'
payload = {'key': 'value'}  # Payload required by the application

# Make the API call
response = mp.make_api_call(app_name, user_credentials, payload)
print(response.json())  # Assuming the response is in JSON format
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

This API provides a more Pythonic way of managing your applications with ModelPark compared to using the CLI directly.
