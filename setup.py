# Dmitry Kisler © 2020
# www.dkisler.com

import pathlib
from setuptools import setup


DIR = pathlib.Path(__file__).parent
requirements = (DIR / "requirements.txt").read_text()
README = (DIR / "README.md").read_text()


setup(
    name='gbqschema_converter',
    version='1.1.0',
    description="Library to convert Google BigQuery Table Schema into Json Schema",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kislerdm/gbqschema_converter",
    author="Dmitry Kisler",
    author_email="admin@dkisler.com",
    license='MIT',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["gbqschema_converter"],
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "json2gbq = gbqschema_converter.__main__:json_to_gbq",
            "gbq2json = gbqschema_converter.__main__:gbq_to_json",
        ]
    },
)
