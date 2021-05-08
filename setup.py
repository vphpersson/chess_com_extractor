from setuptools import setup, find_packages

setup(
    name='chess_com_extractor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyutils @ git+ssh://git@github.com/vphpersson/pyutils.git#egg=pyutils',
        'httpx',
        'chess'
    ]
)
