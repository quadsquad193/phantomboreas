from setuptools import setup

setup(
    name='Quadcopter/backend',
    version='0.0.0',
    description='Backend services for the Quadcopter project',
    url='https://github.com/quadsquad193/Quadcopter',

    setup_requires=['pytest-runner'],
    test_requires=['pytest', 'pytest-dbfixtures'],

    packages=['droneservice', 'openalprservice', 'parkinglogservice', 'webservice'],
    package_dir={
        'droneservice': 'droneservice',
        'openalprservice': 'openalprservice',
        'parkinglogservice': 'parkinglogservice',
        'webservice': 'webservice'
    }
)
