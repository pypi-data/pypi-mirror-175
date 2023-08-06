# Python-Package-Manager

This is a python module pip manager using list of package names
This package is developed for use in small projects with less package version dependency.
This package cannot manage package version.

## How to work

get list of installed packages
chetehck package is installed
install package if not installed

## How to use

install(package_list=["p1", "p2"])

uninstall(package_list=["p1", "p2"])

install(package_list=["p1", "p2"], upgrade=True, python_cmd="python3.10")

uninstall(package_list=["p1", "p2"], python_cmd="python3.10")
