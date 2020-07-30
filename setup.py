import setuptools
import codecs
import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


print('packages=', setuptools.find_packages())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="frameoverframe", 
    version=get_version("frameoverframe/__init__.py"),
    author="Example Author",
    author_email="author@example.com",
    description="Utils for processing image sequences",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
     
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    python_requires='>=3.6',
    scripts=[],
    
    entry_points={
        'console_scripts': [
            'align_image_stack_sequence= frameoverframe.cli.align_image_stack_sequence__main__:main',
            'bracket = frameoverframe.cli.bracket__main__:main',
            'deflicker = frameoverframe.cli.deflicker__main__:main',
            'enfuse_batch = frameoverframe.cli.enfuse_batch__main__:main',
            'recombine = frameoverframe.cli.recombine__main__:main',
            'rename_uniq = frameoverframe.cli.rename_uniq__main__:main',
            'renumber = frameoverframe.cli.renumber__main__:main',
            'tracer = frameoverframe.cli.tracer__main__:main',
        ],   
    },
     
)
