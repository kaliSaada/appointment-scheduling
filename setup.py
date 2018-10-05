try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

from distutils.core import setup
import setuptools

requirements = parse_requirements('requirements.txt', session=False)
setup(name='api',
      version='1.0.0',
      author='khalil',
      email='khalil062010@gmail.com',
      packages=setuptools.find_packages(),
      install_requires=[str(requirement.req) for requirement in requirements])
