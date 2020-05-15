from setuptools import setup, find_namespace_packages

with open('VERSION') as f:
    version = f.read()

setup(
    name="account",
    version=version,
    packages=find_namespace_packages(),
    scripts=['account/app.py'],

    package_data={
        'account': ['account', 'VERSION'],
    },

    # metadata to display on PyPI
    author="Chris Antenesse",
    author_email="chris@huntfindr.com",
    description="The service that provides the backend REST API for account actions"

)
