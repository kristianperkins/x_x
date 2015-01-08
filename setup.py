from setuptools import setup

setup(
    name='x_x',
    author='Kristian Perkins',
    author_email='khperkins@gmail.com',
    version='0.1',
    url='http://github.com/krockode/x_x',
    py_modules=['x_x'],
    description='Excel file CLI Reader',
    long_description=open('README.rst').read(),
    license='Apache 2.0',
    install_requires=[
        'xlrd',
    ],
    entry_points='''
       [console_scripts]
       x_x=x_x:main
    ''',
    classifiers=(
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
    ),
)