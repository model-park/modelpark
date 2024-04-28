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
        """Download and install the correct binary for the current OS."""
        system = platform.system().lower()
        if system == 'linux':
            url = "https://modelpark.app/dist-folder/modelpark-cli-linux"
            self.download_and_install(url)
        elif system == 'darwin':  # macOS is identified as 'Darwin'
            url = "https://modelpark.app/dist-folder/modelpark-cli-macos"
            self.download_and_install(url)
        else:
            raise Exception(f"Unsupported operating system: {system}")

    def download_and_install(self, url):
        """Download and install binary from a given URL."""
        target_dir = "/usr/local/bin/modelpark"
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        subprocess.check_call(['curl', url, '-o', target_dir])
        subprocess.check_call(['chmod', '+x', target_dir])
        print(f"Installed binary to {target_dir}")



setup(
    name='modelpark',
    version='0.1.1',
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
    ],
    keywords='modelpark, deployment, cloud, api',
    cmdclass={
        'install': CustomInstall,
    }
)

