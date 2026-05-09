from setuptools import setup, find_packages

setup(
    name="ui-event-streaming",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.13.4",
        "pydantic-ai>=1.93.0",
    ],
    author="Algorithmica",
    description="UI Event Streaming capability for Pydantic AI agents",
    python_requires=">=3.12",
)
