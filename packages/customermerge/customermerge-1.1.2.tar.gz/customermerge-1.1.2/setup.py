from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name="customermerge",
    version="1.1.2",
    author="Emeral Digital",
    author_email="eduardo.martinez.2117@gmail.com",
    description="Merge dataset from customer data trigger",
    long_description_content_type="text/markdown",
    long_description=README,
    packages=find_packages(),
    install_requires = ['google-cloud-storage', 'google-cloud-bigquery', 'pytz'],
    keywords=['python', 'bigquery', 'storage', 'bucket'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)