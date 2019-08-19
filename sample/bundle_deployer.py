import shutil
import git
from zipfile import ZipFile
import os
import argparse


def deploy_bundle(args):
    print()


def main():
    parser = argparse.ArgumentParser(description='Deploy Bundle')
    parser.add_argument('-dp', '--destpath', required=True, help='Input destination Repo Local Path')
    parser.add_argument('-zp', '--zippath', required=True, help='Input Bundle Zip File Path')
    args = parser.parse_args()
    deploy_bundle(args)
    print("Success")


if __name__ == '__main__':
    main()
