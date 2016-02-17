#!python3

import os
import argparse
import sys


def create_symlinks(origin, dest):
    folder_name = os.path.split(origin)[1]
    folder_destination = os.path.join(dest, folder_name)
    for path, directories, files in os.walk(origin):
        for file in files:
            file_destination = os.path.join(dest, folder_name, file)
            file_origin = os.path.join(origin, file)
            if os.path.exists(folder_destination):
                if not os.path.exists(file_destination):
                    os.symlink(file_origin, file_destination)
            else:
                os.makedirs(folder_destination)
                os.symlink(file_origin, file_destination)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create symlinks of all files in the origin folder in the destination folder')
    parser.add_argument(
        '--origin', '-o', help='absolute origin path', action='store', required=True)
    parser.add_argument(
        '--destination', '-d', help='absolute destination path', action='store', required=True)
    args = parser.parse_args()
    confirmation = input(
        'Origin: {}\nDestination: {}\nAre these paths correct? (y/n) '.format(args.origin, args.destination))
    if confirmation.lower() == 'y':
        create_symlinks(args.origin, args.destination)
    else:
        sys.exit()
