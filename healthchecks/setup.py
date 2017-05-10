import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_requirements_list(requirements):
    return read(requirements)


setup(
    name='devops_portal_tests',
    version=1.0,
    description='Unified function and integration tests for Devops Portal',

    url='http://www.openstack.org/',
    author='Mirantis',
    author_email='example@lists.openstack.org',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'devops-portal-tests = devops_portal_tests.cli:main'
        ]
    },
    include_package_data=True,
    classifiers=[
        'Environment :: Linux',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=get_requirements_list('./requirements.txt'),
)
