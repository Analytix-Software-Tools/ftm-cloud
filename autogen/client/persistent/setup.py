"""
    FtmCloud

    Search engine and analytics API.  # noqa: E501

    The version of the OpenAPI document: v0
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "ftmcloud-api-client"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
  "urllib3 >= 1.25.3",
  "python-dateutil",
]

setup(
    name=NAME,
    version=VERSION,
    description="FtmCloud",
    author="Chris Rinaldi",
    author_email="crinaldi44@gmail.com",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "FtmCloud"],
    python_requires=">=3.6",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="GNU General Public License v3.0",
    long_description="""\
    Search engine and analytics API.  # noqa: E501
    """
)
