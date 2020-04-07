# Dmitry Kisler © 2020
# www.dkisler.com

import os
from setuptools import setup, find_namespace_packages


DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(DIR, 'requirements.txt')) as f:
    requirements = f.read()


setup(
    name='gbqschema_converter',
    version='1.0',
    description="Library to convert Google BigQuery Schema to Json Schema",
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    author="Dmitry Kisler",
    author_email=["admin@dkisler.com"],
    license='MIT',
    packages=("gbqschema_converter", 
              "gbqschema_converter.gbqschema_to_jsonschema",
              "gbqschema_converter.jsonschema_to_gbqschema"),
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False
)
