import setuptools

with open("README.org", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="pwmg-fxia",
    version="0.0.1",
    author="Zeqing (Fred) Xia",
    author_email="fredxia2011@gmail.com",
    description="A command line tool to manage passwords",
    long_description=readme,
    long_description_content_Type="text/markdown",
    keywords="password passwords",
    url="https://github.com/fxia/pwmg",
    packages=setuptools.find_packages(),
    install_requires=["tabulate>=0.8.2", "pycrypto>=2.6.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "OperatingSystem :: OS Independent",
    ],
)

