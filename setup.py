from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

try:
    import pypandoc
    long_description = pypandoc.convert(path.join(here, 'README.md'), 'rst')
except(IOError, ImportError):
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()\

setup(
    name='vesync-outlet',
    version='0.1.1',
    description='vesync-outlet is a library to control Vesync wifi outlets',
    long_description=long_description,
    url='https://github.com/jeffleary00/vesync-outlet',
    author='Jeff Leary',
    author_email='sillymonkeysoftware@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
    ],
    keywords=['vesync', 'iot'],
    packages=['vesync_outlet'],
    zip_safe=False,
    install_requires=['requests>=2.6.0'],
)
