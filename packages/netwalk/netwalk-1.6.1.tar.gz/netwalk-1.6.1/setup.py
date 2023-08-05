# -*- coding: UTF-8 -*-
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "netwalk",
    version = "1.6.1",
    author = "Federico Tabbò (Europe)",
    author_email = "federico.tabbo@global.ntt",
    description = "Network discovery and analysis tool",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/icovada/netwalk",
    project_urls = {
        "Bug Tracker": "https://github.com/icovada/netwalk/issues"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    packages = setuptools.find_packages(),
    python_requires = ">=3.10",
    install_requires=[
        "ciscoconfparse==1.6.50",
        "napalm==4.0.0"
    ],
    include_package_data=True
)
