import setuptools

setuptools.setup(
    name="etherpadlite",
    version="0.1.0",
    url="https://github.com/gsdatta/etherpadlite",

    author="Ganesh Datta",
    author_email="me@ganeshdatta.com",

    description="A client library for etherpad",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Programming Language :: Python :: 3.4',
    ],
)
