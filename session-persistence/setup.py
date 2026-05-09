from setuptools import setup, find_packages

setup(
    name="session-persistence",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "pydantic-ai>=1.93.0",
    ],
    author="Algorithmica",
    description="Persistence capability for Pydantic AI agents",
    python_requires=">=3.12",
)
