from setuptools import setup, find_packages

setup(
    author='Chris Pickett',
    author_email='chris.pickett@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Natural Language :: English',
    ],
    description='Library for creating skills for the Amazon Echo',
    license='MIT',
    long_description=open('README.rst').read(),
    name='django-echo',
    packages=find_packages(),
    url='https://github.com/bunchesofdonald/django-echo',
    version='0.1.0',
)
