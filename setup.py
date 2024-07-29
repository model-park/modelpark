from setuptools import setup, find_packages

setup(
    name='modelpark',
    version='0.1.17',
    description='Versatile solution for sharing apps through secure URLs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/model-park/modelpark',
    author='Veysel Kocaman',
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

)