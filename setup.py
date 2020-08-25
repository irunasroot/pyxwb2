from setuptools import setup
from pyxwb2 import __version__ as version

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = [r for r in f.read().split("\n") if r]


setup(
    name="pyxwb2",
    packages=["pyxwb2", "pyxwb2.models"],
    version=version,
    license="GNU GPLv3",
    description="Python API for FFG X-wing 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dennis Whitney",
    author_email="dennis@irunasroot.com",
    url="https://github.com/minsis/pyxwb2",
    download_url="https://github.com/minsis/pyxwb2/archive/v0.1.0b.tar.gz",
    package_data={
        "pyxwb2": [
            "data/*",
            "data/*/*",
            "data/*/*/*",
            "data/*/*/*/*"
        ]
    },
    keywords=[
      "ffg",
      "x-wing",
      "xwing",
      "x-wing 2.0",
      "xwing 2.0"
    ],
    install_requires=requirements,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
    ]
)
