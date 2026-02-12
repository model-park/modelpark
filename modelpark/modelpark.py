import shutil
import subprocess
import sys
import os
import platform
import requests


class CommandRunner:
    """Executes system commands using the ModelPark Go CLI."""

    @staticmethod
    def find_executable():
        """Find the modelpark CLI binary on the system."""
        # 1. Check PATH via shutil.which
        path = shutil.which('modelpark')
        if path:
            return path

        # 2. Check common install locations
        home = os.path.expanduser('~')
        candidates = [
            '/usr/local/bin/modelpark',
            os.path.join(home, '.local', 'bin', 'modelpark'),
            os.path.join(home, 'modelpark'),
        ]

        if platform.system().lower() == 'windows':
            candidates = [
                os.path.join(os.environ.get('PROGRAMFILES', ''), 'modelpark', 'modelpark.exe'),
                os.path.join(home, 'modelpark.exe'),
                os.path.join(home, '.local', 'bin', 'modelpark.exe'),
            ]

        for candidate in candidates:
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return candidate

        return None

    @staticmethod
    def run_command(command):
        """Run a CLI command and return stdout."""
        executable = CommandRunner.find_executable()
        if not executable:
            print(
                "Error: ModelPark CLI not found. "
                "Install it from https://github.com/model-park/cli/releases"
            )
            sys.exit(1)

        full_command = f"{executable} {command}"
        try:
            result = subprocess.run(
                full_command, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            if result.returncode != 0:
                print("Error:", result.stderr.strip())
            return result.stdout
        except Exception as e:
            print("Error running command:", e)
            sys.exit(1)


class ModelPark:
    """Python wrapper for the ModelPark Go CLI.

    The CLI must be installed separately — see
    https://github.com/model-park/cli/releases
    """

    def __init__(self):
        if CommandRunner.find_executable() is None:
            print(
                "Warning: ModelPark CLI not found on this system. "
                "Install it from https://github.com/model-park/cli/releases"
            )

    def login(self, token=None, email=None):
        """Authenticate with ModelPark.

        Args:
            token: API token for authentication.
            email: Email for interactive login.
        """
        command = "login"
        if token:
            command += f" --token {token}"
        elif email:
            command += f" --email {email}"
        return CommandRunner.run_command(command)

    def logout(self):
        """Log out of ModelPark."""
        return CommandRunner.run_command("logout")

    def run(self, name, command_args, port=None, access=None, framework=None):
        """Run a command and expose it via ModelPark tunnel (background).

        Args:
            name: App name (will be accessible at https://name.modelpark.app).
            command_args: Command and arguments to run (e.g. "streamlit run app.py").
            port: Port the app listens on (auto-detected if omitted).
            access: Access level — 'private' or 'public'.
            framework: Framework hint (e.g. 'streamlit', 'gradio').
        """
        command = f"run --name {name}"
        if port:
            command += f" --port {port}"
        if access:
            command += f" --access {access}"
        if framework:
            command += f" --framework {framework}"
        command += f" -- {command_args}"
        return CommandRunner.run_command(command)

    def serve(self, name, port, access=None, framework=None):
        """Tunnel an already-running local app via ModelPark (background).

        Args:
            name: App name (will be accessible at https://name.modelpark.app).
            port: Local port the app is running on.
            access: Access level — 'private' or 'public'.
            framework: Framework hint (e.g. 'streamlit', 'gradio').
        """
        command = f"serve --name {name} --port {port}"
        if access:
            command += f" --access {access}"
        if framework:
            command += f" --framework {framework}"
        return CommandRunner.run_command(command)

    def ls(self):
        """List running apps."""
        result = CommandRunner.run_command("ls")
        print(result)
        return result

    def logs(self, name, follow=False):
        """View logs for a running app.

        Args:
            name: App name.
            follow: If True, stream logs continuously (blocking).
        """
        command = f"logs {name}"
        if follow:
            command += " -f"
        result = CommandRunner.run_command(command)
        print(result)
        return result

    def stop(self, name):
        """Stop a running app by name.

        Args:
            name: App name to stop.
        """
        return CommandRunner.run_command(f"stop {name}")

    def kill(self, name):
        """Kill a running app by name.

        Args:
            name: App name to kill.
        """
        return CommandRunner.run_command(f"kill {name}")

    def status(self):
        """Show CLI status."""
        result = CommandRunner.run_command("status")
        print(result)
        return result

    def version(self):
        """Show version information."""
        from . import __version__
        version_dict = __version__
        print(f"modelpark python sdk version: {version_dict['app_version']}")
        cli_output = CommandRunner.run_command("version")
        if cli_output:
            print(f"modelpark CLI: {cli_output.strip()}")
        return version_dict


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
                url += f"&expiresIn={expire}"
        else:
            if expire:
                url += f"?expiresIn={expire}"

        headers = {'Authorization': f'Bearer {auth_token}'}
        response = requests.get(url, headers=headers, data={})
        return response.json()['accessToken']

    @staticmethod
    def make_api_call(app_name, user_credentials, request_payload=None, password=None,
                      expire=None, extension=None, files=None, audio_file_path=None):

        auth_token = APIManager.get_auth_token(user_credentials)
        access_token = APIManager.get_access_token(app_name, auth_token, password=password, expire=expire)

        url = f"https://{app_name}.modelpark.app"

        if extension:
            url += f"/{extension}"

        headers = {"x-access-token": access_token}

        if files:
            response = requests.post(url, headers=headers, files=files)
        elif audio_file_path:
            with open(audio_file_path, 'rb') as audio_file:
                audio_file_binary = {"audio": audio_file}
                response = requests.post(url, headers=headers, files=audio_file_binary)
        else:
            response = requests.get(url, headers=headers, params=request_payload)

        if response.status_code == 200:
            return response.json()
        else:
            return response.text

    @staticmethod
    def make_api_call_with_access_token(app_name, access_token, request_payload=None,
                                        extension=None, files=None, audio_file_path=None):

        url = f"https://{app_name}.modelpark.app"

        if extension:
            url += f"/{extension}"

        headers = {"x-access-token": access_token}

        if files:
            response = requests.post(url, headers=headers, files=files)
        elif audio_file_path:
            with open(audio_file_path, 'rb') as audio_file:
                audio_file_binary = {"audio": audio_file}
                response = requests.post(url, headers=headers, files=audio_file_binary)
        else:
            response = requests.get(url, headers=headers, params=request_payload)

        if response.status_code == 200:
            return response.json()
        else:
            return response.text
