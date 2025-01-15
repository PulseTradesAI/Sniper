from setuptools import setup, find_packages

setup(
    name="solana-flash-trader",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.23.0',
        'tensorflow>=2.10.0',
        'keras>=2.10.0',
        'pandas>=1.5.0',
        'tqdm>=4.64.0',
        'docopt>=0.6.2',
        'coloredlogs>=15.0',
        'python-dotenv>=0.21.0',
        'solana>=0.27.0',
        'python-binance>=1.0.16',
        'web3>=5.31.1'
    ],
    python_requires='>=3.8',
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered flash trading bot for Solana",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/solana-flash-trader",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)