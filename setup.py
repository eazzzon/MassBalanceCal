import setuptools

setuptools.setup(
    name="massbalance",
    version="v0.2",
    author="Yishen Zhang",
    author_email="yishen.zhang@rice.edu",
    packages= setuptools.find_packages(
        exclude= ['example', 'benchmark', 'Tutorial']
        ),


    install_requires=[
            'pandas>=1.3.5',
            'numpy>=1.21.5',
            'matplotlib>=3.5.1',
            'scipy>=1.7.3',
            ],
)
