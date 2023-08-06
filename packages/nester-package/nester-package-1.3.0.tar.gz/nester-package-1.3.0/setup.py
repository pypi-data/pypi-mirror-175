from distutils.core import setup

# read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='nester-package',
    version='1.3.0',
    py_modules=['nester'],
    author='SonaM',
    author_email='sonalimetkar1@gmail.com',
    description='Printing each items in list (nested or not) on new line with or without required tab spaces/indent',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    install_requires=[],

)
