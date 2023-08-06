from pathlib import Path
from setuptools import setup, find_packages

setup(
    name='rcplus_alloy_common',
    version='0.0.3',
    description='RC+/Alloy helpers functions for Python',
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type='text/markdown',
    url='https://github.com/ringier-data/rcplus-alloy-lib-py-common',
    author='Ringier AG',
    author_email='info@rcplus.io',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    setup_requires=[
        'requests>=2.28.1',
        'jsonschema>=4.17.0',
        'python-json-logger>=2.0.4',
        'logzio-python-handler>=4.0.0',
        'pytest-runner>=6.0.0',
    ],
    tests_require=[
        'pytest>=7.2.0',
    ],
    python_requires='>=3.8',
)
