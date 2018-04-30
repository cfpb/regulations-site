from setuptools import find_packages, setup


setup(
    name="regulations",
    version_format='{tag}.dev{commitcount}+{gitsha}',
    packages=find_packages(),
    include_package_data=True,
    setup_requires=[
        'cfgov_setup==1.2',
        'setuptools-git-version==1.0.3',
    ],
    frontend_build_script='frontendbuild.sh',
    install_requires=[
        'Django>=1.8,<1.9',
        'lxml==4.1.0',
        'requests==2.18.4',
    ],
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'License :: Public Domain',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    extras_require={
        'testing': [
            'coverage>=3.7.0',
            'django-nose==1.4.5',
            'mock==2.0.0',
            'nose-exclude==0.5.0',
        ],
    }
)
