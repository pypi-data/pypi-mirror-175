from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Jarvis Desktop Assitant In Just 2 LINES!'
LONG_DESCRIPTION = 'JarvisInOne is Module Developed, So that Anyone can Create Jarvis Program In Just Two Lines Of Code'

# Setting up
setup(
    name="JarvisInOne",
    version=VERSION,
    author="Tanma Sinha",
    author_email="tanmaysinhapatna@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['jarvis desktop assistant', 'jarvis ai', 'jarvis', 'jarvis pythoon', 'Mr Programmer','mrprogrammer'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)