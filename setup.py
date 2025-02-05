from setuptools import setup, find_packages

setup(
    name='documentation-capture',
    version='0.1.0',
    description='Setting up a python package',
    author='Elias Nimland',
    url='https://github.com/EliasNimlandLind/documentation-capture.git',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pygetwindow',
        'Pillow', 
        'pynput'
    ],
    entry_points={
        'console_scripts': ['entry-point=src.documentation_capture.__init__:main']  # Ensure this path is correct
    },
)
