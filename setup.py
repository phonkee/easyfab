from setuptools import setup

setup(
    name='easyfab',
    version='0.3.6',
    description='simpler deployments with fabric',
    url='https://github.com/phonkee/easyfab/',
    author='phonkee',
    author_email='phonkee@phonkee.eu',
    license='MIT',
    packages=[
        'easyfab',
    ],
    scripts=[
        'bin/easyfab'
    ],
    install_requires=[
        'jinja2',
        'fabric',
        'unipath',
    ],
    package_data={
        'easyfab': [
            '*.conf',
            'templates/*.*',
            'templates/deployment/*.*',
            'templates/deployment/conf/*.*',
        ]
    },
    zip_safe=False
)
