from setuptools import setup, find_packages

setup(
    name='chess_com_extractor',
    version='0.21',
    packages=find_packages(),
    install_requires=[
        'typed_argument_parser @ git+https://github.com/vphpersson/typed_argument_parser.git#egg=typed_argument_parser',
        'scrape_latest_user_agent @ git+https://github.com/vphpersson/scrape_latest_user_agent.git#egg=scrape_latest_user_agent',
        'pyutils @ git+https://github.com/vphpersson/pyutils.git#egg=pyutils',
        'httpx',
        'chess'
    ]
)
