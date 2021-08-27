import re
from setuptools import setup # type: ignore


# Get library version
VERSION_REGEX = re.compile(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', re.M)


version = ''
with open('qualitube/__init__.py') as f:
    version = VERSION_REGEX.search(f.read()).group(1) # type: ignore

if not version:
    raise RuntimeError('version is not set')


# Get README file
readme = ''
with open('README.md') as f:
    readme = f.read()


setup(
    name='qualitube',
    author='Vitor Mussa',
    version=version,
    packages=['qualitube'],
    license='MIT'
)
