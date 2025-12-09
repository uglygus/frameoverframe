#!/bin/bash


cd docs

pip3 install ..



#pwd 


#sphinx-quickstart

echo cwd= $(pwd)

sphinx-apidoc -f -o . ../frameoverframe

make  clean html

open ./_build/html/index.html
