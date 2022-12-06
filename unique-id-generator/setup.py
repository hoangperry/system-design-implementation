from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Unique ID Generator'
LONG_DESCRIPTION = 'An implementation for System Design Interview books'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="unique_id_generator",
    version=VERSION,
    author="Hoang N. Truong",
    author_email="hoang@hoang.tech",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
    ]
)
