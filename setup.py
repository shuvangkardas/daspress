from setuptools import setup, find_packages

setup(
    name="daspress",
    version="2.0.0",
    author="Shuvangkar Das",
    author_email="shuvangkarcdas@gmail.com.com",
    description="Complete Obsidian to Jekyll blog publishing system",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyYAML>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "daspress=daspress.cli:main",
        ],
    },
)


# from setuptools import setup, find_packages
# import os

# # Read version from file
# def read_version():
#     here = os.path.abspath(os.path.dirname(__file__))
#     with open(os.path.join(here, 'daspress', '__init__.py'), 'r') as f:
#         for line in f:
#             if line.startswith('__version__'):
#                 return line.split('"')[1]
#     return "1.0.0"

# # Read long description
# def read_long_description():
#     here = os.path.abspath(os.path.dirname(__file__))
#     try:
#         with open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
#             return f.read()
#     except FileNotFoundError:
#         return "daspress Pro - Complete blog publishing system"

# setup(
#     name="daspress-pro",
#     version=read_version(),
#     author="Your Name",
#     author_email="your.email@example.com",
#     description="Complete Obsidian to Jekyll blog publishing system with premium features",
#     long_description=read_long_description(),
#     long_description_content_type="text/markdown",
#     packages=find_packages(),
#     classifiers=[
#         "Development Status :: 5 - Production/Stable",
#         "Intended Audience :: Developers",
#         "Intended Audience :: End Users/Desktop",
#         "License :: Other/Proprietary License",
#         "Operating System :: OS Independent",
#         "Programming Language :: Python :: 3",
#         "Programming Language :: Python :: 3.8",
#         "Programming Language :: Python :: 3.9",
#         "Programming Language :: Python :: 3.10",
#         "Programming Language :: Python :: 3.11",
#         "Topic :: Internet :: WWW/HTTP :: Site Management",
#         "Topic :: Text Processing :: Markup",
#     ],
#     python_requires=">=3.8",
#     install_requires=[
#         "PyYAML>=6.0",
#     ],
#     entry_points={
#         "console_scripts": [
#             "daspress=daspress.cli:main",
#         ],
#     },
#     include_package_data=True,
#     package_data={
#         'daspress': ['templates/*.md', 'themes/*.yml'],
#     },
# )