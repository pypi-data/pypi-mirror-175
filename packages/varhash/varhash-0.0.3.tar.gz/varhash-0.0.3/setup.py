from setuptools import setup, find_packages
from setuptools import setup, Extension

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='varhash',
  version='0.0.3',
  description='Implementation of VAR Hash in Python',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/rishabhc9',  
  author='Rishabh Chopda',
  author_email='aaditchopda2@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['varhash','hash','hashing','cryptography'], 
  packages=find_packages(),
  install_requires=[''] 
)