import json
import shutil
import git
from zipfile import ZipFile
import os
import argparse


def create_bundle_zip(args):
    create_bundle_dir(args)
    create_manifest_file(args)
    with ZipFile(os.path.join(args.zippath, args.srcbranch + '.zip'), 'w') as zipfile:
        for stats in get_diff_info(args.srcpath, args.srcbranch, args.destbranch):
            if stats.get("type") != 'D':
                add_files(stats.get("path"), args)
                zipfile.write(os.path.join(args.zippath, "src", stats.get('path')),  # zip file from directory
                              os.path.join("src", stats.get('path')))  # to directory
        zipfile.write(os.path.join(args.zippath, "build", "manifest.txt"), os.path.join("build", "manifest.txt"))
    delete_bundle_dir(args)


def create_manifest_file(args):
    f = open(os.path.join(args.zippath, "build", "manifest.txt"), "w+")
    f.write(manifest_info_text(args))
    f.close()


def manifest_info_text(args):
    txt = "{\'name\':\'manifest\',\'info\':["
    for stats in get_diff_info(args.srcpath, args.srcbranch, args.destbranch):
        print(stats)
        txt += str(stats) + ","
    txt = txt[:-1]
    txt += "]}"
    txt = txt.replace("\'", "\"")
    return txt


def create_bundle_dir(args):
    os.mkdir(os.path.join(str(args.zippath), "src"))
    os.mkdir(os.path.join(str(args.zippath), "build"))


def delete_bundle_dir(args):
    shutil.rmtree(os.path.join(str(args.zippath), "src"))
    shutil.rmtree(os.path.join(str(args.zippath), "build"))


def add_files(path, args):
    os.makedirs(os.path.join(args.zippath, "src", os.path.dirname(path)), exist_ok=True)
    shutil.copy(os.path.join(args.srcpath, path), os.path.join(args.zippath, "src", path))


def get_diff_info(path, src_branch, dest_branch):
    repo = git.Repo(path)
    repo.git.checkout(dest_branch)
    dest_commit = repo.head.commit
    repo.git.checkout(src_branch)
    source_commit = repo.head.commit
    diffs = {
        diff.a_path: diff for diff in source_commit.diff(dest_commit)
    }

    for diff in dest_commit.diff(source_commit):
        stats = {
            'path': diff.a_path,
            'filename': diff.a_path,
            'type': diff.change_type,
        }
        yield stats


def main():
    parser = argparse.ArgumentParser(description='Create Bundle')
    parser.add_argument('-sp', '--srcpath', required=True, help='Input src Repo Local Path')
    parser.add_argument('-zp', '--zippath', required=True, help='Input root Path for bundle zip file')
    parser.add_argument('-sb', '--srcbranch', required=True, help='Input src branch')
    parser.add_argument('-db', '--destbranch', required=True, help='Input destination branch')

    args = parser.parse_args()
    print("Start creating bundle zip file\n")
    create_bundle_zip(args)
    print("\nSuccess")


if __name__ == '__main__':
    main()
