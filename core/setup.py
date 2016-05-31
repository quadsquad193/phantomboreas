from setuptools import setup, find_packages



setup(
    name='phantom-boreas',
    version='0.1.0',
    description='Backend services for the Quadcopter project',
    url='https://github.com/quadsquad193/Quadcopter',

    install_requires = [
        'flask',
        'flask-sqlalchemy',
        'redis',
        'MySQL-python',
        'wtforms',
        'flask-bcrypt',
        'flask-login'
    ],
    setup_requires=['pytest-runner'],
    test_requires=['pytest', 'pytest-dbfixtures'],

    packages=find_packages(),
    include_package_data=True,
)
