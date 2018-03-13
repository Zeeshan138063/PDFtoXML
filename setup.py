from distutils.core import setup

setup(
    name='Order_Input',
    version='1.0.0',
    author='S. Kveton',
    author_email='kaveets24@gmail.com',
    packages=[''],
    scripts=['input.py','exemel.py'],
    url='',
    license='LICENSE.txt',
    description='A program for parsing order data from a pdf and converting it into xml, to be imported by VIEW.',
    long_description=open('README.txt').read(),
    install_requires=[
        'isoweek==1.3.3',
        'pypdf2==1.26.0',
        'lxml==3.8.0'
    ],
)
