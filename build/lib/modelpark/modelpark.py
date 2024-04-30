import json
import requests
import subprocess
import sys
import os
import platform

class CommandRunner:
    """Executes system commands related to ModelPark CLI operations."""

    @staticmethod
    def get_executable_path():
        """Returns the full path to the executable based on the operating system."""
        home_dir = os.path.expanduser('~')  # Gets the home directory
        if platform.system().lower() == 'windows':
            return os.path.join(home_dir, 'modelpark.exe')  # Windows executable path
        else:
            return os.path.join(home_dir, 'modelpark')  # Unix/Mac executable path

    @staticmethod
    def run_command(command):
        try:
            executable_path = CommandRunner.get_executable_path()
            command = f"{executable_path} {command}"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Started process {process.pid}")
            print (f"Command: {command}")
            if 'init' not in command:
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    print("Error:", stderr)
                    sys.exit(1)
                return stdout
        except subprocess.CalledProcessError as e:
            print("Error:", e.stderr)
            sys.exit(1)

class ModelPark:
    def __init__(self):
        pass

    def login(self, token=None, username=None, password=None):
        command = "login"
        if token:
            command += f" -t {token}"
        if username:
            command += f" -u {username}"
        if password:
            command += f" -p {password}"
        CommandRunner.run_command(command)

    def init(self, port=None, detach=True):
        command = "init"
        if port:
            command += f" -p {port}"
        if detach !=True:
            command += f" -d {str(detach).lower()}"
        print(f"Running command: {command}")  # Debug print
        output = CommandRunner.run_command(command)
        print("Initialization Output:", output)

    def stop(self):
        CommandRunner.run_command("stop")

    def logout(self):
        CommandRunner.run_command("logout")

    def register(self, port, name, file_path=None, access='private', password=None, framework=None):
        if framework:
            command = f"register -p {port} -n {name} -a {access} -f {framework}"
        else:
            command = f"register -p {port} -n {name} -a {access}"
        if file_path:
            command += f" {file_path}"
        if access == 'public' and password:
            command += f" -password {password}"
        CommandRunner.run_command(command)
    
    def register_port(self, name, port, access='private',password=None):
        command = f"register  -n {name} -a {access} -p {port}"
        if access == 'public' and password:
            command += f" -password {password}"
        CommandRunner.run_command(command)

    def run_with_streamlit_and_register(self, name, file_path, access='private', password=None, port=None):
        command = f"register {file_path} -n {name} -a {access} -f streamlit"
        if port:
            command += f" -p {port}"
        if access == 'public' and password:
            command += f" -password {password}"
        CommandRunner.run_command(command)

    def kill(self, name=None, all=False):
        command = "kill"
        if all:
            command += " -a"
        elif name:
            command += f" -n {name}"
        CommandRunner.run_command(command)

    def ls(self):
        result = CommandRunner.run_command("ls")
        print(result)

    def status(self):
        result = CommandRunner.run_command("status")
        print(result)

class APIManager:
    """Manages API interactions for ModelPark."""

    @staticmethod
    def get_auth_token(user_credentials):
        url = "https://modelpark.app/api/auth/login"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=user_credentials)
        return response.json()['authToken']

    @staticmethod
    def get_access_token(app_name, auth_token):
        url = f"https://modelpark.app/api/app-project/access/{app_name}"
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = requests.get(url, headers=headers)
        return response.json()['accessToken']

    @staticmethod
    def make_api_call(app_name, user_credentials, payload):
        auth_token = APIManager.get_auth_token(user_credentials)
        access_token = APIManager.get_access_token(app_name, auth_token)
        url = f"https://modelpark.app/api/app-project/access/{app_name}"
        headers = {'Authorization': f'Bearer {access_token}'}
        return requests.get(url, headers=headers, json=payload)


