from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Protein Isoform Event identifier'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

setup(
        name="isoformevent", 
        version=VERSION,
        author="Julian Perez",
        author_email="<julian.perez@stanford.edu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pandas', 'numpy', 'os', 'pickle', 'matplotlib'],
        
        keywords=['python', 'protein', 'isoform', 'event'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)