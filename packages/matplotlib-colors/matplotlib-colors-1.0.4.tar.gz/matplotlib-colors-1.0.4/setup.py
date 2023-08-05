from setuptools import setup, find_packages

long_description = open("README.md").read()
required = ['matplotlib']

setup(
    name="matplotlib-colors",
    version="1.0.4",
    author="Tom Draper",
    author_email="tomjdraper1@gmail.com",
    license="MIT",
    description="A collection of curated colors and colormaps for matplotlib.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tom-draper/matplotlib-colors",
    key_words="visualization color colormap colorset matplotlib",
    install_requires=required,
    packages=find_packages(where="matplotlib_colors"),
    python_requires=">=3.6",
)