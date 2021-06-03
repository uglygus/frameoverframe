import codecs
import os.path

import setuptools


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
    author="Cooper Battersby",
    author_email="cooperbattersby@egmail.com",
    description="Utils for processing image sequences",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uglygus/frameoverframe",
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
            'img2vid = frameoverframe.cli.img2vid__main__:main',
            'fof = frameoverframe.cli.fof__main__:main',
            'fofinfo = frameoverframe.cli.fofinfo__main__:main',
            'make_previews = frameoverframe.cli.make_previews__main__:main',
            'raw2dng = frameoverframe.cli.raw2dng__main__:main',
            'recombine = frameoverframe.cli.recombine__main__:main',
            'rename_uniq = frameoverframe.cli.rename_uniq__main__:main',
            'renumber = frameoverframe.cli.renumber__main__:main',
            'thin = frameoverframe.cli.thin__main__:main',
            'test_images = frameoverframe.cli.test_images__main__:main',
            'autotrace_sequence = frameoverframe.cli.autotrace_sequence__main__:main',
            'unmix = frameoverframe.cli.unmix__main__:main',
            'vid2img = frameoverframe.cli.vid2img__main__:main',
        ],
    },

)
