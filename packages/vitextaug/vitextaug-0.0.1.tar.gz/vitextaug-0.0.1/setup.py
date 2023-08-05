from setuptools import setup, find_packages


setup(
    name='vitextaug',
    version='0.0.1',
    license='MIT',
    author="longnt",
    author_email='long.itptit@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    # url='https://github.com/gmyrianthous/example-publish-pypi',
    description="Text data augmentation for Vietnamese",
    long_description="Text data augmentation using Lexical Replacement, Back Translation, Text Generation, ... for Vietnamese",
    install_requires=[
          'vncorenlp',
      ],

)
