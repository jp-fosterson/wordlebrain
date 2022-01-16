from setuptools import find_packages, setup

README = open('README.md').read()

setup(
    name='wordlebrain'
    , version='1.1.0'
    , author='JP Fosterson'
    , author_email='jp.fosterson@gmail.com'
    , description=README.split('\n')[0]
    , long_description=README
    , package_data = {"wordlebrain": ["wordles.txt"]}
    , packages=find_packages(exclude=['test', 'test.*', '*.test', '*.test.*'])
    , install_requires=[
        ]
    , entry_points = {
        'console_scripts' : ['wordlebrain=wordlebrain:play']
    }

)
