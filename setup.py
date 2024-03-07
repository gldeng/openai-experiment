from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='sdr_utils',
    version='0.1',
    packages=find_packages(),
    package_data={
        'sdr_utils': ['resource/*'],
    },
    entry_points={
        'console_scripts': [
            'sdr=sdr_utils.cli:main',  # Adjust the path according to your directory and file names
        ],
    },
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=required,
)
