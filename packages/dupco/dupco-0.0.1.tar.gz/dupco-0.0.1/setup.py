import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dupco",
    version="0.0.1",
    author="gaojian",
    author_email="gaojian@shuzilm.cn",
    description="A simple way to call DigitalUnion service",
    long_description=long_description,
    url="https://github.com/DigitalUnion/du-pco-py-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)