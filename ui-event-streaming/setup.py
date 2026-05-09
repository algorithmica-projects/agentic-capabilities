from setuptools import setup, find_packages

setup(
    name="ui-event-streaming",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "pydantic-ai>=1.79.0",
    ],
    author="Algorithmica",
    description="UI Event Streaming capability for Pydantic AI agents",
    python_requires=">=3.9",
)
