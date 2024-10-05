import zipfile
from zipfile import ZipFile

def sawed_off_path(path):
    path = create_path(path)
    path = path[:-1]

    for i in range(len(path) - 1, -1, -1):
        if path[i] == "/":
            return path
        path = path[:-1]
    return path
def create_path(path):
    if path == "":
        return "/"
    if path[-1] != "/":
        path = path + "/"
    if path[0] != "/":
        path = "/" + path
    return path

def ShellEmulator(config):
    file = open("config.xml").readlines()
    name = file[0][:-1]
    system = ZipFile(file[1])
    path_obj = zipfile.Path(file[1], at="/")
    path = path_obj.name
    com = input("<" + name + ": " + create_path(path) + "># ").split(" ")


    def ls():
        file = list(path_obj.iterdir())
        for i in file:
            print(i.name)


    def cd():
        nonlocal path_obj
        if com[1] == ".." or com[1] == "../":
            path_obj = zipfile.Path(file[1], create_path(sawed_off_path(path))[1:])
            print(path_obj)
            return
        elif not (create_path(com[1]) in list(create_path(i.name) for i in list(path_obj.iterdir()))):
            print(path + create_path(com[1])[1:], ": ", end="")
            print("No such file or directory")
            return
        path_obj = zipfile.Path(file[1], path[1:] + create_path(com[1])[1:])
        #print(path_obj)

    def uniq(filename):
        if not (create_path(filename) in list(create_path(i.name) for i in list(path_obj.iterdir()))):
            print(path + com[1], ": ", end="")
            print("No such file or directory")
            return

        unique_lines = set()

        with system.open(path[1:] + filename, 'r') as file:
            for line in file.readlines():
                unique_lines.add(line.strip())

            for line in unique_lines:
                print(line)

    while True:
        try:
            if com[0] == "ls":
                ls()
            elif com[0] == "cd" and len(com) == 2:
                cd()
            elif com[0] == "tree":
                system.printdir()
            elif com[0] == "echo" and len(com) == 2:
                print(com[1])
            elif com[0] == "uniq" and len(com) == 2:
                uniq(com[1])
            elif com[0] == "exit":
                return
            path = create_path(str(path_obj)[len(file[1]):])
            com = input("<" + name + ": " + create_path(path) + "># ").split(" ")
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    ShellEmulator()