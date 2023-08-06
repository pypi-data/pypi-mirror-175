import os
from os.path import join
from typing import List
from sys import platform

class _controller:
    def __init__(self, package_list:List[str], abs_path:str="", python_cmd:str=None):

        if python_cmd == None : 
            if platform == "linux" or platform == "linux2":
                self.cmd = "python3"
            elif platform == "darwin":
                self.cmd = "python3"
            elif platform == "win32":
                self.cmd = "python"
        else : 
            self.cmd = python_cmd

        self.package_names = package_list
        self.abs_path = abs_path

        if self.abs_path != "": os.makedirs(self.abs_path, exist_ok=True)
        self.pip_path = os.path.join(self.abs_path, "pip_list.txt")
        os.system(f"{self.cmd} -m pip list >> "+ self.pip_path.replace(" ", "\ "))
        os.system(f"{self.cmd} -m pip install --upgrade pip")
        with open(f"{self.pip_path}", "r", encoding="utf-8-sig") as f:
            self.lines = f.readlines()
        
    def install(self):
        for package_name in self.package_names:
            check_intalled = False
            for search in self.lines: 
                check_intalled = check_intalled or search.split(' ')[0].lower()==package_name.lower()
            if(check_intalled is False): 
                os.system(f"{self.cmd} -m pip install {package_name}")
        os.remove(f"{self.pip_path}")

    def update(self):
        for package_name in self.package_names:
            check_intalled = False
            for search in self.lines: 
                check_intalled = check_intalled or search.split(' ')[0].lower()==package_name.lower()
            if(check_intalled is True): 
                os.system(f"{self.cmd} -m pip install --upgrade {package_name}")
        os.remove(f"{self.pip_path}")
    
    def uninstall(self):
        for package_name in self.package_names:
            check_intalled = False
            for search in self.lines: 
                check_intalled = check_intalled or search.split(' ')[0].lower()==package_name.lower()
            if(check_intalled is True): 
                os.system(f"{self.cmd} -m pip uninstall -y {package_name}")
        os.remove(f"{self.pip_path}")

class _requirements:
    def __init__(self, abs_path:str, python_cmd:str=None):

        if python_cmd == None : 
            if platform == "linux" or platform == "linux2":
                self.cmd = "python3"
            elif platform == "darwin":
                self.cmd = "python3"
            elif platform == "win32":
                self.cmd = "python"
        else : 
            self.cmd = python_cmd

        self.abs_path = abs_path
        if self.abs_path != "": os.makedirs(self.abs_path, exist_ok=True)

    def requirement_install(self):
        path_ = os.path.join(self.abs_path, "requirements.txt")
        print(f"{self.cmd} -m pip install -r {path_}")
        os.system(f"{self.cmd} -m pip install -r {path_}")

    def requirement_unistall(self):
        path_ = os.path.join(self.abs_path, "requirements.txt")
        f"{self.cmd} -m pip install -r {path_}"
        os.system(f"{self.cmd} -m pip uninstall -r {path_}")

    def requirement_freeze(self):
        path_ = os.path.join(self.abs_path, "requirements.txt")
        os.system(f"{self.cmd} -m pip freeze > {path_}")

class install(_controller):
    def __init__(self, package_names: List[str], abs_path: str = "", python_cmd: str = None):
        super().__init__(package_names, abs_path, python_cmd)
        super().install()

class update(_controller):
    def __init__(self, package_names: List[str], abs_path: str = "", python_cmd: str = None):
        super().__init__(package_names, abs_path, python_cmd)
        super().update()

class uninstall(_controller):
    def __init__(self, package_names: List[str], abs_path: str = "", python_cmd: str = None):
        super().__init__(package_names, abs_path, python_cmd)
        super().uninstall()

class requirement_install(_requirements):
    def __init__(self, abs_path: str, python_cmd: str = None):
        super().__init__(abs_path, python_cmd)
        super().requirement_install()

class requirement_uninstall(_requirements):
    def __init__(self, abs_path: str, python_cmd: str = None):
        super().__init__(abs_path, python_cmd)
        super().requirement_unistall()

class requirement_freeze(_requirements):
    def __init__(self, abs_path: str, python_cmd: str = None):
        super().__init__(abs_path, python_cmd)
        super().requirement_freeze()

# test code
if __name__ == "__main__":
    import pipcontrol

    pipcontrol.install(package_names=["kivy", "kivymd"], python_cmd="python3.10")
    pipcontrol.update(package_names=["kivy", "kivymd"], python_cmd="python3.10")
    pipcontrol.uninstall(package_names=["kivy", "kivymd"], python_cmd="python3.10")

    from os.path import dirname, abspath

    ABS_PATH = dirname(abspath(__file__))

    pipcontrol.requirement_freeze(abs_path=ABS_PATH, python_cmd="python3.10")
    pipcontrol.requirement_install(abs_path=ABS_PATH, python_cmd="python3.10")
    pipcontrol.requirement_uninstall(abs_path=ABS_PATH, python_cmd="python3.10")
