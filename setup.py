from setuptools import setup, find_packages

setup(
    name="tpay",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "python-dotenv>=0.19.0",
    ],
    author="t54 labs",
    author_email="support@t54.ai",
    description="tPay SDK for Python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tledger/tpay-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 