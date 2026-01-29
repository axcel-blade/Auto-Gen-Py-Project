from setuptools import setup, find_packages

setup(
    name="auto_gen_py_project",
    version="0.1.0",
    description="A Python project that auto-generates Python code",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Axcel Blade",
    author_email="srikanthfernando3@gmail.com",
    url="https://github.com/axcel-blade/auto-gen-py-project",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English"
    ],
    entry_points={
        "console_scripts": [
            "auto_gen_py_project=auto_gen_py_project.cli:main",
        ],
    },
)