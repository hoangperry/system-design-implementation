from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'Unique ID Generator'
LONG_DESCRIPTION = 'An implementation for System Design Interview books'

setup(
    name="unique_id_generator",
    version=VERSION,
    author="Hoang N. Truong",
    author_email="hoang@hoang.tech",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    url="https://github.com/hoangperry/system-design-implementation/tree/master/unique-id-generator",
    install_requires=[],
    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
    ]
)
