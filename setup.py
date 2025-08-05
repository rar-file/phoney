from setuptools import setup, find_packages

setup(
    name="phoney",
    version="0.1.0",
    description="Fake Info generator, a library for generating realistic personal data like names, phone numbers, emails, and more.",
    author="rarfile",
    author_email="d7276250@email.com",
    url="https://github.com/yourusername/phoney",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.7",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
