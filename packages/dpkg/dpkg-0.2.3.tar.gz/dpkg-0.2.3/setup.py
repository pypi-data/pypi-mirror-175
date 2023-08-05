import setuptools

with open("README.md", "r", encoding='utf-8') as fn:
    long_description = fn.read()

setuptools.setup(
    name='dpkg',
    version='0.2.3',
    author='SangMinLee',
    author_email='smlee@d-if.kr',
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.6',
    install_requires = [
    'pyreadstat==1.1.9'
    ],
)

