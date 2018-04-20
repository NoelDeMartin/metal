import os

from setuptools import setup

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__)) + '/metal/'

def get_files(*paths):
    files = []

    for path in paths:
        for (absolute_path, _, filenames) in os.walk(PROJECT_ROOT + path):
            for filename in filenames:
                files.append(absolute_path + '/' + filename)

    return files

setup(
    name='metal',
    version='0.1.0',
    packages=['metal', 'metal.commands', 'metal.lib'],
    package_data={
        'metal': get_files('docker', 'nginx')
    },
    include_package_data=True,
    install_requires=[
        'Click',
        'docker',
        'docker-compose'
    ],
    entry_points='''
        [console_scripts]
        metal=metal.cli:cli
    ''',
)
