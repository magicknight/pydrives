from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='pydrives',
    version='0.1',
    packages=find_packages(),
    # scripts=['scripts/remote_script.py'],
    # metadata for upload to PyPI
    author="Yi Sun",
    author_email="Yis@smu.edu",
    description="A light weight cloud drives program. Supports Google Drive, DropBox, and The Box",
    long_description=readme(),
    license="MIT",
    keywords="python google drive dropbox the box cloud drive",
    url="http://www.daxiv.com",   # project home page, if any
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
)
