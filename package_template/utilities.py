import inspect
import os
import shutil
import sys

class Utilities:
    def __init__(self):
        if ("--name" in sys.argv):
            self.package_name = sys.argv[sys.argv.index("--name") + 1]
        else:
            self.package_name = ""
            while len(self.package_name) < 1:
                self.package_name = input("Package name: ")
                if len(self.package_name) < 1:
                    print("Package name must be at least 1 character long")

        self.user = os.path.expanduser("~").split("/")[-1]
        self.python_version = sys.version


class DirectoryUtilities(Utilities):
    def __init__(self):
        super().__init__()
        self.desktop = os.path.expanduser("~/Desktop")
        self.directories = (self.package_name, "scripts", "tests")
        self.create_directory_structure()
    
    def create_directory_structure(self):
        for dir in self.directories:
            dir_path = os.path.join(self.desktop, self.package_name, dir)
            os.makedirs(dir_path, exist_ok=True)


class FileUtilites(DirectoryUtilities):
    def __init__(self):
        super().__init__()
        self.script_name = "run_"+self.package_name+".py"
        self.files = {"pyproject.toml": ["copy_from_template", "pyproject_toml_template.py"],
                      "setup.cfg": ["setup_file"],
                      "requirements.txt": ["write_empty_file"],
                      "README.md": ["readme_file"],
                      ".gitignore": ["copy_from_template", "gitignore_template.py"],
                      self.script_name: ["script_file"],
                      "__init__.py": ["write_empty_file"]}

    def setup_file(self, files: list):
        data = inspect.cleandoc("""
            [metadata]
            name = {name}
            version = 0.0.1
            author = {author}
            author_email = None
            description = None
            long_description = file: README.md
            long_description_content_type = text/markdown
            url = None

            [options]
            packages = find:
            python_requires =
                >={version}

            [options.entry_points]
            console_scripts =
            package_template = {package}.scripts.{script}:main
            """.format(name=self.package_name, author=self.user, version=self.python_version, package=self.package_name,
                       script=self.script_name.split(".py")[0]))
        
        file_path = os.path.join(self.desktop, self.directories[0], files[0])
        with open(file_path, "w") as f:
            f.write(data)

    def readme_file(self, files: list):
        data = inspect.cleandoc("""
            # {package}
            ## Overview""".format(package=self.package_name))
        file_path = os.path.join(self.desktop, self.directories[0], files[0])
        with open(file_path, "w") as f:
            f.write(data)

    def script_file(self, files: list):
        data = inspect.cleandoc("""
            def run_{package}():
                pass

            def main():
                run_{package}()
            """.format(package=self.package_name))

        file_path = os.path.join(self.desktop, self.directories[0], self.directories[1], files[0])
        with open(file_path, "w") as f:
            f.write(data)

    def write_empty_file(self, files: list, index: int = None):
        data = ""
        if files[0] == "__init__.py":
            file_path = os.path.join(self.desktop, self.directories[0], self.directories[index], files[0])

        file_path = os.path.join(self.desktop, self.directories[0], files[0])
        with open(file_path, "w") as f:
            f.write(data)

    def copy_from_template(self, files: list):
        template_path = os.path.join(os.path.dirname(__file__), "templates", files[1])
        file_path = os.path.join(self.desktop, self.directories[0], files[0])
        shutil.copyfile(template_path, file_path)

    def create_files(self):
        for file, data in self.files.items():
            if len(data) > 1:
                files = [file, data[1]]
            else:
                files = [file]

            if data[0] == "setup_file":
                self.script_file(files=files)
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
    