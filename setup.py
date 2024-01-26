from setuptools import setup, find_packages

setup(
    name='pubPdf',
    version='0.1.0',
    url='https://github.com/nishlabo/pubPdf.git',
    author='nishlabo',
    author_email='n.ishiharajp@gmail.com',
    description='Description of my package',
    packages=find_packages(),    
    install_requires=['reportlab', 'svglib', 'requests'],
)
