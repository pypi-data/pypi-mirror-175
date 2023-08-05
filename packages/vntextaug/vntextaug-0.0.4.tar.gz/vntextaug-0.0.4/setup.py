import setuptools

setuptools.setup(
    name="vntextaug",
    version="0.0.4",
    author="LT Nguyen",
    author_email="longnt53@fsoft.com.vn",
    description="Text data augmentation for Vietnamese",
    long_description="Text data augmentation using Lexical Replacement, Back Translation, Text Generation, ... for Vietnamese",
    # long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages("src"),
    package_dir={'': 'src'},
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'vncorenlp'
      ]
)