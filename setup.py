from setuptools import setup, find_packages

setup(
    name="genlayer-py",
    version="0.1.0",
    description="GenLayer Python SDK",
    author="GenLayer",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "web3>=7.10.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 