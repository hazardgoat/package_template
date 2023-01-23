# package_template
## Overview
This tool automates creation of directory structures and files when setting up a new installable package.

## Key Details
- Creates new package template in current working directory, or specified directory path
- New package template is set up for stand-alone installation
- New package is run using an alias of the package name (e.g. package_template)

## Operation
1) Create a local Python environment >= 3.7 and activate it
2) Download this repository (package_template)
3) From the terminal `cd` to the `package_template-master` directory within it containing the `requirments.txt` file.
4) Install the `requirments.txt` file with `pip install -r requirements.txt`
5) Install `package_template` with `pip install --upgrade .`
6) Run `package_template` from anywhere with the `package_template` alias.

Example terminal command:
`package_template --name test_package --outpath "C:\\Users\\USER\\Desktop\\test_package"`

## Options
package name:
* `--name` : name of new package (also used for entry point alias)
* `--outpath` : full path of desired output directory (Windows, OS X, Linux)
    