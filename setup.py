import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bsed",
    version="0.2.4",
    author="Andrew Bihl",
    author_email="andrewbihlva@gmail.com",
    description="Simple english syntax for stream editing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrewbihl/bsed",
    packages=setuptools.find_packages(exclude="tests"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'bsed = bsed.interpreter:main'
        ]
    },
    install_requires=['argcomplete'],
    include_package_data=True,
    python_requires='>3.1.0',
)
