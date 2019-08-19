import json
import shutil
import git
from zipfile import ZipFile
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


def create_bundle_zip(args):
    create_bundle_dir(args)
    create_manifest_file(args)
    with ZipFile(os.path.join(args.zippath, args.srcbranch + '.zip'), 'w') as zipfile:
        for stats in get_diff_info(args.srcpath, args.srcbranch, args.destbranch):
            count(stats.get('type'))
            if stats.get("type") != 'D':
                add_files(stats.get("to_path"), args)
                zipfile.write(os.path.join(args.zippath, "bundle-temp", "src", stats.get('to_path')),
                              os.path.join("src", stats.get('to_path')))  # to directory
        zipfile.write(os.path.join(args.zippath, "bundle-temp", "build", "manifest.txt"),
                      os.path.join("build", "manifest.txt"))
    delete_bundle_dir(args)


def count(type):
    change_type = type[0]
    TYPE_COUNT[change_type] = TYPE_COUNT[change_type] + 1


def create_manifest_file(args):
    f = open(os.path.join(args.zippath, "bundle-temp", "build", "manifest.txt"), "w+")
    f.write(manifest_info_text(args))
    f.close()


def manifest_info_text(args):
    txt = "{\'name\':\'manifest\',\'info\':["
    for stats in get_diff_info(args.srcpath, args.srcbranch, args.destbranch):
        # print(stats)
        txt += str(stats) + ","
    txt = txt[:-1]
    txt += "]}"
    txt = txt.replace("\'", "\"")
    return txt


def create_bundle_dir(args):
    os.makedirs(os.path.join(str(args.zippath), "bundle-temp", "src"))
    os.makedirs(os.path.join(str(args.zippath), "bundle-temp", "build"))


def delete_bundle_dir(args):
    shutil.rmtree(os.path.join(str(args.zippath), "bundle-temp"))


def add_files(path, args):
    os.makedirs(os.path.join(args.zippath, "bundle-temp", "src", os.path.dirname(path)), exist_ok=True)
    shutil.copy(os.path.join(args.srcpath, path), os.path.join(args.zippath, "bundle-temp", "src", path))


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
            'from_path': diff.a_path,
            'to_path': diff.b_path,
            'filename': os.path.basename(diff.a_path),
            'type': diff.change_type,
        }
        yield stats


def main():
    parser = argparse.ArgumentParser(description='Create Bundle')
    parser.add_argument('-sp', '--srcpath', required=True, help='Input source Repo Local Path')
    parser.add_argument('-zp', '--zippath', required=True, help='Input root Path for bundle zip file')
    parser.add_argument('-sb', '--srcbranch', required=True, help='Input source branch')
    parser.add_argument('-db', '--destbranch', required=True, help='Input destination branch')

    args = parser.parse_args()
    print("Start creating bundle zip file\n")
    create_bundle_zip(args)
    for value in TYPE_COUNT:
        print(TYPE_NAME[value], " : ", TYPE_COUNT[value])

    print("\nSuccess")


if __name__ == '__main__':
    main()
