import inspect
import logging
import os
import shutil
import sys



logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', 
                    level=logging.INFO)


class Utilities:
    """Sets up universal utility class methods
    """
    def __init__(self):
        """Holds universally applicable variables generated by utility methods
        """
        self.package_name = None
        self.out_path = None
        self.user = None
        self.python_version = None
        self.directories = [self.package_name, "scripts", "tests"]
        
        self.get_package_name()
        self.create_directory_structure()

    def get_package_name(self):
        """Gets the name of the package to be created from user input in the terminal,
        as well as the output path (if specified), user name, and python version of the active environment
        """
        if ("--name" in sys.argv):
            self.package_name = sys.argv[sys.argv.index("--name") + 1]
        else:
            while len(self.package_name) < 1:
                self.package_name = input("Package name: ")
                if len(self.package_name) < 1:
                    logging.warning("Package name must be at least 1 character long")
                    
        if ("--outpath" in sys.argv):
            self.out_path = sys.argv[sys.argv.index("--outpath") + 1]
        else:
            self.out_path = os.getcwd()
        
        if sys.platform == "win32":  # Windows
            self.user = os.path.expanduser("~").split("\\")[-1]
        else:  # OS X or Linux
            self.user = os.path.expanduser("~").split("/")[-1]

                                           
        self.python_version = sys.version

    def create_directory_structure(self):
        """Creates package directories at the output path
        """
        logging.info(f"Creating package directories @ {self.out_path}")
        
        for dir in self.directories:
            dir_path = os.path.join(self.out_path, self.package_name, dir)
            os.makedirs(dir_path, exist_ok=True)


class FileUtilites(Utilities):
    """Creates the base package files from user input and templates
    """
    def __init__(self):
        super().__init__()
        self.script_name = f"run_{self.package_name}.py"
        self.files = {"pyproject.toml": ["copy_from_template", "pyproject_toml_template.py"],
                      "setup.cfg": ["setup_file"],
                      "requirements.txt": ["write_empty_file"],
                      "README.md": ["readme_file"],
                      ".gitignore": ["copy_from_template", "gitignore_template.py"],
                      self.script_name: ["script_file"],
                      "__init__.py": ["write_empty_file"]}

        self.create_files()

    def setup_file(self, files: list):
        """Writes out the setup file to the relevant package directory

        Args:
            files: list of file names
        """
        data = inspect.cleandoc(f"""
            [metadata]
            name = {self.package_name}
            version = 0.0.1
            author = {self.user}
            author_email = None
            description = None
            long_description = file: README.md
            long_description_content_type = text/markdown
            url = None

            [options]
            packages = find:
            python_requires =
                >={self.python_version}

            [options.entry_points]
            console_scripts =
            package_template = {self.package_name}.scripts.{self.script_name.split(".py")[0]}:run_{self.package_name}
            """)
        
        file_path = os.path.join(self.out_path, self.directories[0], files[0])
        with open(file_path, "w") as f:
            f.write(data)

    def readme_file(self, files: list):
        """Writes out a placeholder readme file to the relevant package directory

        Args:
            files: list of file names
        """                        
        data = inspect.cleandoc(f"""
            # {self.package_name}
            ## Overview""")
                                
        file_path = os.path.join(self.out_path, self.directories[0], files[0])
        with open(file_path, "w") as f:
            f.write(data)

    def script_file(self, files: list):
        """Writes out the script file to the relevant package directory that will run the
        package when called with the alias

        Args:
            files: list of file names
        """
        data = inspect.cleandoc(f"""
            def run_{self.package_name}():
                pass
            """)

        file_path = os.path.join(self.out_path, self.directories[0], self.directories[1], files[0])
        with open(file_path, "w") as f:
            f.write(data)

    def write_empty_file(self, files: list, index: int = None):
        """Writes out empty __init__ files to the relevant package dirctories
        
        Args:
            files: list of file names
            index: index of the directories list to call for writing out the __init__ files
        """
        if files[0] == "__init__.py":
            file_path = os.path.join(self.out_path, self.directories[0], self.directories[index], files[0])
        else:
            file_path = os.path.join(self.out_path, self.directories[0], files[0])
        
        data = ""
        with open(file_path, "w") as f:
            f.write(data)

    def copy_from_template(self, files: list):
        """Writes out copies of the template files to the relevant package directories
        
        Args:
            files: list of file names
        """
        template_path = os.path.join(os.path.dirname(__file__), "templates", files[1])
        file_path = os.path.join(self.out_path, self.directories[0], files[0])
        shutil.copyfile(template_path, file_path)

    def create_files(self):
        """Runs all of the package file creation methods
        """
        for file, data in self.files.items():
            if len(data) > 1:
                files = [file, data[1]]
            else:
                files = [file]

            if data[0] == "setup_file":
                self.setup_file(files=files)
            elif data[0] == "readme_file":
                self.readme_file(files=files)
            elif data[0] == "script_file":
                self.script_file(files=files)
            elif data[0] == "write_empty_file":
                if file == "__init__.py":
                    for i in range(2):
                        self.write_empty_file(files=files, index=i)
                else:
                    self.write_empty_file(files=files)
            else:
                self.copy_from_template(files=files)
