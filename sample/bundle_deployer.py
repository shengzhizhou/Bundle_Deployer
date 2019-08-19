import shutil
import git
from zipfile import ZipFile
import json
import os
import argparse


def deploy_bundle(args):
    f=open(os.path.join(args.rootpath,"build","manifest.txt"),'r')
    text=f.read()
    data=json.loads(text)
    print(data['info'][0].get('path'))



def main():
    parser = argparse.ArgumentParser(description='Deploy Bundle')
    parser.add_argument('-dp', '--destpath', required=True, help='Input destination Repo Local Path')
    parser.add_argument('-rp', '--rootpath', required=True, help='Input Extraction Folder Root Path')
    args = parser.parse_args()
    deploy_bundle(args)
    print("Success")


if __name__ == '__main__':
    main()
