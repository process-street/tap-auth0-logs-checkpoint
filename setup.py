#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-auth0-logs-checkpoint",
    version="0.1.0",
    description="Singer.io tap for extracting Auth0 logs by checkpoint method",
    author="Process Street",
    url="https://process.st",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_auth0_logs_checkpoint"],
    install_requires=[
        'auth0-python==3.9.1',
        "singer-python==5.8.0"
    ],
    entry_points="""
    [console_scripts]
    tap-auth0-logs-checkpoint=tap_auth0_logs_checkpoint:main
    """,
    packages=["tap_auth0_logs_checkpoint"],
    package_data={
        "schemas": ["tap_auth0_logs_checkpoint/schemas/*.json"]
    },
    include_package_data=True,
)
