from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "readme.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.2.1'
DESCRIPTION = 'Tool to ace coding practicals.'
LONG_DESCRIPTION = "It is a tool created by Aditya jha to help students in their school coding practicals or any other thing(even cheating) so that they can use this to get help in finding any data problem's answer. Check out more about this project and its code on https://github.com/Notanyon/STUHELP"

# Setting up
setup(
    name="STUHELP",
    version=0.2,
    author="Aditya jha",
    author_email="ajha75862@gmail.com",
    url = "https://github.com/Notanyon/STUHELP",
    description="It is a tool created by Aditya jha to help students in their school coding practicals or any other thing(even cheating) so that they can use this to get help in finding any data problem's answer. Check out more about this project and its code on https://github.com/Notanyon/STUHELP",
    long_description_content_type="text/markdown",
    long_description="It can be used for coding practicals, cheating and much more as it provides you feature to find mean, mode, median, average and sort any array. We all have seen students suffering to learn things like numpy and using it so why don't I help? I present you my creation STUHELP, you can find any answer of any data question in seconds. So forget numpy and say hello to STUHELP. Check out more about this project and its code on https://github.com/Notanyon/STUHELP",
    packages=find_packages(),
    install_requires=['numpy', 'time', 'os', ],
    keywords=['python', 'data', 'mean', 'mode', 'median', 'average', 'sort', 'data all-in-one', 'school help', 'school', 'coding'], 
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
    )