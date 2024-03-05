from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='sdr_utils',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=required,
)
