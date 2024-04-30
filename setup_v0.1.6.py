import os
import platform
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstall(install):
    """Custom handler for the 'install' command."""

    def run(self):
        install.run(self)
        self.install_system_specific_binary()

    def install_system_specific_binary(self):
        """Install different binaries for different OS."""
        os_type = platform.system().lower()
        if os_type == "linux":
            url = "https://modelpark.app/dist-folder/modelpark-cli-linux"
            self.download_and_install(url)
        elif os_type == "darwin":  # macOS
            url = "https://modelpark.app/dist-folder/modelpark-cli-macos"
            self.download_and_install(url)
        elif os_type == "windows":
            url = "https://modelpark.app/dist/mpinstaller.exe"
            self.download_and_install_windows(url)
        else:
            raise Exception(f"Unsupported operating system: {os_type}")

    def download_and_install(self, url):
        """Download and install binary from a given URL."""
        target_dir = "/usr/local/bin/modelpark"
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        subprocess.check_call(['curl', url, '-o', target_dir])
        subprocess.check_call(['chmod', '+x', target_dir])
        print(f"Installed binary to {target_dir}")

    def download_and_install_windows(self, url):
        """Specific method to handle Windows installation."""
        install_path = os.environ.get("APPDATA") + "\\ModelPark"
        if not os.path.exists(install_path):
            os.makedirs(install_path)
        command = f"powershell Invoke-WebRequest -Uri {url} -OutFile \"{install_path}\\modelpark-cli.exe\""
        subprocess.check_call(command, shell=True)
        print(f"Installed modelpark-cli to {install_path}")

setup(
    name='modelpark',
    version='0.1.6',
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

