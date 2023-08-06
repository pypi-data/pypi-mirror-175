"""setup.py file for packaging purposes"""
import setuptools

with open("README.md", mode="r", encoding="ascii") as fh:
    long_description = fh.read()

setuptools.setup(
    name="img_ai_prep",
    version="0.0.1",
    author="ikmckenz",
    description="Prepare images for AI model ingestion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ikmckenz/img_ai_prep",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "Pillow>=9.3.0",
        "numpy>=1.23.4",
        "opencv-python>=4.6.0.66",
    ],
)
