import os
import platform
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstall(install):
    def run(self):
        install.run(self)
        self.remove_existing_binary()  # Ensure any existing version is removed
        self.install_system_specific_dependencies()

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

setup(
    name='modelpark',
    version='0.1.7',
    description='Versatile solution for sharing apps through secure URLs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/model-park/modelpark',
    author='Your Name',
    author_email='info@modelpark.app',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
],
    keywords='modelpark, deployment, cloud, api',
    cmdclass={
        'install': CustomInstall,
    }
)

