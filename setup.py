import os
from setuptools import setup, find_packages


setup(
    name="regulations",
    version_format='{tag}.dev{commitcount}+{gitsha}',
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['cfgov_setup==1.2', 'setuptools-git-version==1.0.3'],
    frontend_build_script='frontendbuild.sh',
    install_requires=[
        'django>=1.8,<1.12',
        'lxml',
        'requests',
    ],
    classifiers=[
        'License :: Public Domain',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    ]
)
