from setuptools import setup, find_packages

NAME = "compile-minifier"
VERSION = "0.1.9"


def readme():
    """print long description"""
    with open("README.md") as f:
        return f.read()


setup(
    name=NAME,
    version=VERSION,
    description="Python compiler and minifier",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author_email="contact@bimdata.io",
    url="https://github.com/bimdata/compile-minifier",
    install_requires=["python-minifier==2.7.0", "fire==0.4.0"],
    extras_require={
        "ci": ["twine==4.0.1", "build==0.9.0"],
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.5, <4",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "compileminify=compileminify.main:entrypoint",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
