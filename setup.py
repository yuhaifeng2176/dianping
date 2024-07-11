from setuptools import setup, find_packages

setup(
    name="project_name",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "requests",
        "numpy",
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            "project_name=project_name.main:main",
        ],
    },
    author="你的名字",
    author_email="你的邮箱",
    description="项目的简要描述",
    license="MIT",
    url="https://github.com/你的用户名/项目名",
)
