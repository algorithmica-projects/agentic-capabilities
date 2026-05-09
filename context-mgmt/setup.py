from setuptools import setup, find_packages

setup(
    name="context-mgmt",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "pydantic-ai>=1.93.0",
    ],
    author="Algorithmica",
    description="Context Managers for Pydantic AI agents",
    python_requires=">=3.12",
)
