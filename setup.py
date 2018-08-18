import os
from setuptools import setup, find_packages

setup(
    name="INT2018",
    version="0.5.0",
    author="Jakub Szatkowski",
    author_email="jaksza18@gmail.com",
    description=("INT conference service."),
    install_requires=['django', 'django_extensions', 'martor', 'Pillow',
                      'factory_boy', 'django_nose', 'djangorestframework', 'markdown', 'django-filter', 'channels', 'pypiwin32', 'channels_redis'],
    license="MiT",
    keywords="virtual scoreboard score sport",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MiT",
    ]
)
