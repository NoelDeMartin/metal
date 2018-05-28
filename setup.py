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

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='metal-cli',
    version='0.0.1',
    author='Noel De Martin',
    author_email='noeldemartin@gmail.com',
    description='Docker wrapper: Forget about your bare-metal and get started right away.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/noeldemartin/metal',
    license='MIT',
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
