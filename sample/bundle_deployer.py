import shutil
import git
from zipfile import ZipFile
import json
import os
import argparse

TYPE_COUNT = {
    "R": 0,
    "D": 0,
    "A": 0,
    "M": 0,
    "C": 0,
}

TYPE_NAME = {
    "R": "Renamed Files",
    "D": "Deleted Files",
    "A": "Added Files",
    "M": "Modified Files",
    "C": "Copied Files"
}

def deploy_bundle(args):
    f = open(os.path.join(args.rootpath, "build", "manifest.txt"), 'r')
    text = f.read()
    data = json.loads(text)
    for file in data['info']:
        if file.get('type')[0] == 'D':
            delete_file(args, file.get('to_path'))
        if file.get('type')[0] == 'R':
            rename_file(args , file.get('from_path'),file.get('to_path'))
        if file.get('type')[0] == 'C':
            add_file(args, file.get('to_path'))
        else:
            add_file(args, file.get('to_path'))
        count(file.get('type'))


def delete_file(args,path):
    os.remove(os.path.join(args.destpath, path))

def count(type):
    change_type = type[0]
    TYPE_COUNT[change_type] = TYPE_COUNT[change_type] + 1

def rename_file(args ,from_path, to_path):
    delete_file(args,from_path)
    add_file(args,to_path)


def add_file(args,path):
    os.makedirs(os.path.join(args.destpath, os.path.dirname(path)), exist_ok=True)
    shutil.copy(os.path.join(args.rootpath, "src", path), os.path.join(args.destpath, path))



def main():
    parser = argparse.ArgumentParser(description='Deploy Bundle')
    parser.add_argument('-dp', '--destpath', required=True, help='Input destination Repo Local Path')
    parser.add_argument('-rp', '--rootpath', required=True, help='Input Extraction Folder Root Path')
    args = parser.parse_args()
    deploy_bundle(args)
    for value in TYPE_COUNT:
        print(TYPE_NAME[value], " : ", TYPE_COUNT[value])
    print("Success")


if __name__ == '__main__':
    main()
