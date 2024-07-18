import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="massbalance",
    version="v0.2",
    author="Yishen Zhang",
    author_email="yishen.zhang@rice.edu",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eazzzon/MassBalanceCal",
    packages=setuptools.find_packages(
        include=['example', 'benchmark', 'Tutorial', 'massbalance', 'massbalance.*', 'Tutorial.*']
    ),
    install_requires=[
        'pandas>=1.3.5',
        'numpy>=1.21.5',
        'matplotlib>=3.5.1',
        'scipy>=1.7.3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
