import setuptools

setuptools.setup(
    name="massbalance",
    version="v0.2",
    author="Yishen Zhang",
    author_email="yishen.zhang@kuleuven.be",
    packages= setuptools.find_packages(
        exclude= ['example', 'benchmark', 'Tutorial']
        ),


    install_requires= [
    'pandas',
    'numpy',
    'scipy',
    ]
)
