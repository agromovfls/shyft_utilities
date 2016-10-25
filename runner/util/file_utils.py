import os


def get_files(folder):
    return [
        f for f in os.listdir(folder) if (os.path.isfile(os.path.join(folder, f)) and
                                          f[-4:] == ".sql")
        ]


def readall(folder, f):
    with open(os.path.join(folder, f), 'r') as content_file:
        return content_file.read()