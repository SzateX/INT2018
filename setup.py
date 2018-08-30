import os
from setuptools import setup, find_packages

requirements = ['django', 'django_extensions', 'martor', 'Pillow',
                      'factory_boy', 'django_nose', 'djangorestframework', 'markdown', 'django-filter', 'channels', 'channels_redis', 'selenium', 'Faker', 'daphne', 'django-selenium-login', 'nose', 'asgiref', 'coverage']

if os.name == 'nt':
    requirements += ['pypiwin32', 'pywin32']

setup(
    name="INT2018",
    version="0.5.0",
    author="Jakub Szatkowski",
    author_email="jaksza18@gmail.com",
    description=("INT conference service."),
    install_requires=requirements,
    license="MiT",
    keywords="virtual scoreboard score sport",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MiT",
    ]
)
