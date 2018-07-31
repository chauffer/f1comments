from setuptools import setup


setup(
    name="f1comments",
    version="0.1.0",
    url="https://github.com/chauffer/f1comments",
    author="Simone Esposito",
    author_email="chaufnet@gmail.com",
    download_url="https://github.com/chauffer/f1comments",
    packages=["f1comments"],
    entry_points={"console_scripts": "f1comments=f1comments:main"},
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
