from setuptools import setup

setup(
    name="atlas-ai",
    version="0.1",
    py_modules=["atlas"],
    entry_points={
        "console_scripts": [
            "atlas=atlas:main",
        ],
    },
)
