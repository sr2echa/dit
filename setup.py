from setuptools import setup, find_packages

with open("README.md", "r") as f:
    discription = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().split("\n")

setup(
    name='Dit',
    version='0.0.1',
    author='Sreecharan S, Harish Chandran, Harish Barathi, Nidish TS',
    description='Version control for Databases',
    url='https://github.com/sr2echa/dit', 
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    long_description=discription,
    long_description_content_type="text/markdown",
)