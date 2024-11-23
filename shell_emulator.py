import zipfile
from zipfile import ZipFile


class shell_emulator:
    def __init__(self):
        file =  open("config.xml", "r").readlines()
        self.name = file[0].strip()
        self.system = ZipFile(file[1].strip())
        self.system_name = file[1].strip()
        self.path_obj = zipfile.Path(self.system, at="/")
        self.path = self.path_obj.name

    def sawed_off_path(self, path):
        path = self.create_path(path)
        self.path = path[:-1]

        for i in range(len(self.path) - 1, -1, -1):
            if self.path[i] == "/":
                return self.path
            self.path = self.path[:-1]
        return self.path

    def create_path(self, path):
        if path == "":
            return "/"
        if path[-1] != "/":
            path = path + "/"
        if path[0] != "/":
            path = "/" + path
        return path

    def ls(self):
        files = list(self.path_obj.iterdir())
        for file in files:
            print(file.name)

    def cd(self, com):
        path = com[1]

        if path == ".." or path == "../":
            self.path_obj = zipfile.Path(self.system, self.sawed_off_path(self.path)[1:])
            print(self.path_obj)
            return
        else:
            new_path = self.create_path(path)
            if not any(self.create_path(i.name) == new_path for i in self.path_obj.iterdir()):
                print(f"{new_path}: No such file or directory")
                return
            self.path_obj = zipfile.Path(self.system, new_path[1:])  # Adjust path
            print(self.path_obj)

    def uniq(self, filename):
        file_path = self.create_path(filename)

        if not any(self.create_path(i.name) == file_path for i in self.path_obj.iterdir()):
            print(f"{file_path}: No such file or directory")
            return

        unique_lines = set()

        with self.system.open(file_path[1:], 'r') as file:
            for line in file.readlines():
                unique_lines.add(line.strip())

        for line in unique_lines:
            print(line)


if __name__ == '__main__':
    shell = shell_emulator()

    while True:
        try:
            com = input(f"<{shell.name}: {shell.create_path(shell.path)}># ").split(" ")

            if com[0] == "ls":
                shell.ls()
            elif com[0] == "cd" and len(com) == 2:
                shell.cd(com)
            elif com[0] == "tree":
                shell.system.printdir()
            elif com[0] == "echo" and len(com) == 2:
                print(com[1])
            elif com[0] == "uniq" and len(com) == 2:
                shell.uniq(com[1])
            elif com[0] == "exit":
                break

            # Update the current path based on the shell's path object
            shell.path = shell.create_path(str(shell.path_obj)[len(shell.system_name):])

        except KeyboardInterrupt:
            break
