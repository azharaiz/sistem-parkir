import os

def get_img():
    return os.path.join(os.path.abspath(os.getcwd()),"data","img")

def get_log():
    return os.path.join(os.path.abspath(os.getcwd()),"server","static","data","log.txt")

def get_file():
    log_file = open(get_log(), 'r')
    arr = []
    line = log_file.readline()
    while line:
        arr.append(line.split(','))
        line = log_file.readline()
    log_file.close()
    return arr