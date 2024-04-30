import os


def file_delete():
    for i in range(2):
        filename = f"{i}.csv"
        if os.path.exists(filename):
            os.remove(filename)


