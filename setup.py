from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vacancy_project",
    version="0.1.0",
    author="ekachka33",
    author_email="your.email@example.com",
    description="A project for working with HeadHunter API and managing vacancies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ekachka33/vacancy_project",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.31.0",
        "typing-extensions>=4.7.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "coverage>=7.3.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
    },
)
