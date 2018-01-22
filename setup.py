from setuptools import setup

setup(
    name='devbox-cli',
    version='0.1',
    description='Command line tool to manage a development environment, including support for AWS resources',
    url='https://github.com/yevgenybulochnik/devbox-cli',
    author='Yevgeny Bulochnik',
    packages=['devbox'],
    entry_points={
        'console_scripts': [
            'devbox=devbox.cli:main'
        ]
    },
    install_requires=[
        'docopt',
        'boto3',
        'plumbum'
    ]
)
