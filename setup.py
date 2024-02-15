from setuptools import setup, find_packages

setup(
    name='autologic',
    version='0.0.1',  
    description='A framework for LLMs to self-compose reasoning structures',
    package_dir={"": "src"},  # This tells setuptools that packages are under src
    packages=find_packages(where="src"),  # Find packages in src
    install_requires=[
        'python-dotenv',
        'google-generativeai', 
        'llama-cpp-python',
    ],
    entry_points={
        'console_scripts': [
            'autologic=autologic.cli:main',
        ],
    }
)