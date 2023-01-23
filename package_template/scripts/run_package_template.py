from package_template import utilities

def run_package_template():
    """Runs all of the package file creation methods via the
    create_files method
    """
    file_utils = utilities.FileUtilities()
    file_utils.create_files()