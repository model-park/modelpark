import json
import requests
import subprocess
import sys
import os
import platform
from packaging import version


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

class Install_ModelPark_CLI():
    def __init__(self, clear_cache=False):
        from . import __version__
        existing_cli_version = self.check_cli_version()
        new_package_cli_version = __version__['cli_version']
        # Parse the version strings
        existing_cli_version = version.parse(existing_cli_version)
        new_package_cli_version = version.parse(new_package_cli_version)
        # Compare the versions
        if new_package_cli_version > existing_cli_version:
            print(f"More recent ModelPark CLI version found in the new package and the CLI will be upgraded.")
            print(f"Existing CLI Version: {str(existing_cli_version)}")
            print(f"New CLI Version: {str(new_package_cli_version)}")
            clear_cache = True
        else:
            print(f"ModelPark CLI is up-to-date with the latest version.")
        if clear_cache:
            self.remove_existing_binary()
        if not self.is_existing_binary():
            #self.remove_existing_binary()  # Ensure any existing version is removed
            self.install_system_specific_dependencies()

    def check_cli_version(self):
        """Check the version of the installed ModelPark CLI."""
        command = "version"
        version = CommandRunner.run_command(command).strip("ModelPark CLI version: ")
        print(f"ModelPark CLI version: {version}")
        return version

    def remove_existing_binary(self):
        """Remove existing binary if it exists in the user's path."""
        os_type = platform.system().lower()
        if os_type in ["linux", "darwin"]:  # Unix-like systems including macOS
            home_dir = os.path.expanduser('~')
            binary_path = os.path.join(home_dir, "modelpark")
            if os.path.exists(binary_path):
                os.remove(binary_path)
                print(f"Removed existing binary at {binary_path}")
        elif os_type == "windows":
            home_dir = os.environ.get("USERPROFILE")
            executable_path = os.path.join(home_dir, "modelpark.exe")
            if os.path.exists(executable_path):
                os.remove(executable_path)
                print(f"Removed existing binary at {executable_path}")

    def is_existing_binary(self):
        """Remove existing binary if it exists in the user's path."""
        os_type = platform.system().lower()
        if os_type in ["linux", "darwin"]:  # Unix-like systems including macOS
            home_dir = os.path.expanduser('~')
            binary_path = os.path.join(home_dir, "modelpark")
            if os.path.exists(binary_path):
                return True
            else:
                return False
        elif os_type == "windows":
            home_dir = os.environ.get("USERPROFILE")
            executable_path = os.path.join(home_dir, "modelpark.exe")
            if os.path.exists(executable_path):
                return True
            else:
                return False
            
    def remove_existing_binary(self):
        """Remove existing binary if it exists in the user's path."""
        os_type = platform.system().lower()
        if os_type in ["linux", "darwin"]:  # Unix-like systems including macOS
            home_dir = os.path.expanduser('~')
            binary_path = os.path.join(home_dir, "modelpark")
            if os.path.exists(binary_path):
                os.remove(binary_path)
                print(f"Removed existing binary at {binary_path}")
        elif os_type == "windows":
            home_dir = os.environ.get("USERPROFILE")
            executable_path = os.path.join(home_dir, "modelpark.exe")
            if os.path.exists(executable_path):
                os.remove(executable_path)
                print(f"Removed existing binary at {executable_path}")

    def install_system_specific_dependencies(self):
        """Install system-specific dependencies based on the OS."""
        os_type = platform.system().lower()
        if os_type in ["linux", "darwin"]:  # Unix-like systems including macOS
            url = "https://modelpark.app/dist-folder/modelpark-cli-linux" if os_type == "linux" else "https://modelpark.app/dist-folder/modelpark-cli-macos"
            self.download_and_install(url)
        elif os_type == "windows":
            url = "https://modelpark.app/dist/mpinstaller.exe"
            self.download_and_install_windows(url)

    def download_and_install(self, url):
        """Download and install binary for Unix-like systems."""
        home_dir = os.path.expanduser('~')
        binary_path = os.path.join(home_dir, "modelpark")
        subprocess.check_call(['curl', url, '-o', binary_path])
        subprocess.check_call(['chmod', '+x', binary_path])
        #self.add_to_path(home_dir)

    def add_to_path(self, target_dir):
        """Add the installation directory to the user's PATH in .bashrc or .bash_profile."""
        path_update_script = f'\nexport PATH="$PATH:{target_dir}"\n'
        profile_path = os.path.join(os.path.expanduser('~'), '.bash_profile' if platform.system().lower() == 'darwin' else '.bashrc')
        with open(profile_path, 'a') as profile_file:
            profile_file.write(path_update_script)
        print(f"Added {target_dir} to PATH in {profile_path}")

    def download_and_install_windows(self, url):
        """Specific method to handle Windows installation."""
        home_dir = os.environ.get("USERPROFILE")
        executable_path = os.path.join(home_dir, "modelpark.exe")
        subprocess.check_call(['powershell', f'Invoke-WebRequest -Uri {url} -OutFile "{executable_path}"'])
        self.add_to_path_windows(home_dir)

    def add_to_path_windows(self, install_path):
        """Add the installation directory to the PATH for Windows."""
        command = f'[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User) + ";{install_path}", [EnvironmentVariableTarget]::User)'
        subprocess.check_call(['powershell', command], shell=True)
        print(f"Added {install_path} to PATH for Windows")

class ModelPark:
    def __init__(self, clear_cache=False):
        cli = Install_ModelPark_CLI(clear_cache)
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

    def version(self):
        # get version from __init__.py
        from . import __version__
        version_dict =  __version__
        print (f"modelpark python sdk version: {version_dict['app_version']}")
        print (f"modelpark CLI version: {version_dict['cli_version']}")
        return version_dict
    
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
    def get_access_token(app_name, auth_token, password=None, expire=None):
        url = f"https://modelpark.app/api/app-project/access/{app_name}"
        if password:
            url += f"?password={password}"
        if expire:
            url += f"&expire={expire}"
        
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = requests.get(url, headers=headers, data={})
        return response.json()['accessToken']

    @staticmethod
    def make_api_call(app_name, user_credentials, request_payload, password=None, expire=None, extension=None):
        auth_token = APIManager.get_auth_token(user_credentials)
        access_token = APIManager.get_access_token(app_name, auth_token, password=password, expire=expire)
        #url = f"https://modelpark.app/api/app-project/access/{app_name}"

        url = f"http://{app_name}-proxy.modelpark.app"

        if extension:
            url += f"/{extension}"   

        #headers = {'Authorization': f'Bearer {access_token}'}
        headers = {
            "x-access-token": access_token}

        return requests.get(url, headers=headers, params=request_payload)


