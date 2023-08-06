from setuptools import setup
with open("README.md", encoding='utf-8') as fh:
    description = fh.read()

setup(
    name="burmese_number_converter",
    version="1.0.0",
    description="Convert English Number to Burmese Number",
    long_description=description,
    long_description_content_type="text/markdown",
    packages=['burmese_number_converter'],
    author="Han Zaw Nyein",
    author_email="hanzawnyineonline@gmail.com",
    zip_safe=False,
    url='https://github.com/HanZawNyein/odoo-rest-framework.git',
    # install_requires=['datetime']
)
