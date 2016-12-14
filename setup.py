try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('LICENSE') as f:
    license = f.read()

with open('README.rst') as f:
    readme = f.read()

requires = [
        'jinja2',
        'fabric',
        'unipath',
]

setup(
    name='easyfab',
    version='0.4.11',
    description='Simple deployments with fabric',
    long_description=readme,
    url='https://github.com/phonkee/easyfab/',
    author='phonkee',
    author_email='phonkee@phonkee.eu',
    license=license,
    packages=[
        'easyfab',
    ],
    scripts=[
        'bin/easyfab'
    ],
    install_requires=requires,
    include_package_data = True,
    package_data={
        '': [
            'LICENSE',
            'README.rst',
        ],
        'easyfab': [
            '*.conf',
            'templates/*.*',
            'templates/deployment/*.*',
            'templates/deployment/conf/*.*',
        ]
    },
    data_files=[
        ('', ['LICENSE', 'README.rst'])
    ],
    zip_safe=False,
    # classifiers=(
    #     'Development Status :: 3 - Alpha',
    #     'Intended Audience :: Developers',
    #     'Natural Language :: English',
    #     'License :: OSI Approved :: Apache Software License',
    #     'Programming Language :: Python',
    #     'Programming Language :: Python :: 2.6',
    #     'Programming Language :: Python :: 2.7',
    # ),
)
