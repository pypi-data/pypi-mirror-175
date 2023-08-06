import setuptools

setuptools.setup(
    name="pybitds",
    version="0.0.5",
    author="byteschen",
    author_email="czj1132163229@163.com",
    description="pybitds",
    long_description="beginner",
    url="https://github.com/BytesChen/beginner",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=["numpy", "bitarray", "mmh3", "beautifulsoup4"]
)
