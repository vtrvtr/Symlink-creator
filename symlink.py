#!python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import configparser
from ntfsutils import hardlink
from pathlib import PureWindowsPath

config = configparser.ConfigParser()
config.read('E:\Code\Symlink creator\symlink_config.ini')
default_config = config['default']
EXTENSIONS = default_config.get('ext')


def list_files(path):
    return [os.path.join(path, file) for path, directories, files in os.walk(path) for file in files]


def print_header(file_list, origin, destination):
    print('There are {} files. These are the paths:'.format(len(file_list)))
    no_video_files = []
    destination_path = PureWindowsPath(destination)
    origin_path = PureWindowsPath(origin)
    for file in file_list:
        file = file.encode('utf8').decode('cp850')
        file_path = PureWindowsPath(file)
        if origin_path.suffix in EXTENSIONS:
            print('{} -> {}'.format(file_path, destination_path / file_path.parents[0] / file_path.name ))
        else:
            no_video_files.append(file)
    if no_video_files:
        print('FILES THAT WILL BE IGNORED:\n')
        for file in no_video_files:
            print(file)


def create_link(file_origin, file_destination, mode='symlink'):
    try:
        if not os.path.exists(os.path.dirname(file_destination)):
            os.makedirs(os.path.dirname(file_destination))
        print('Folder already exists, just creating {}\n'.format(mode))
        if mode == 'symlink':
            os.symlink(file_origin, file_destination)
        else:
            hardlink.create(file_origin, file_destination)
        print("File: {} linked to {}\n ({})\n".format(
            file_origin, file_destination, mode))
    except FileExistsError:
        print(
            "File {} already exists. Skipping it\n".format(file_destination))
        pass


def main(origin, dest, files, mode='symlink'):
    folder_name = os.path.split(origin)[1]
    for directory, subdirectories, files in os.walk(origin):
        folder_destination = os.path.join(dest, folder_name)
        subfolder = os.path.split(directory)[1]
        for file in files:
            file = file.encode('utf8').decode('cp850')
            file_destination = os.path.join(
                folder_destination, subfolder, file)
            file_origin = os.path.join(directory, file)
            if not os.path.exists(file_destination):
                create_link(file_origin, file_destination, mode)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create symlinks of all files in the origin folder in the destination folder')
    parser.add_argument(
        '--origin', '-o', help='absolute origin path', action='store', required=True)
    parser.add_argument(
        '--destination', '-d', help='absolute destination path', action='store', required=True),
    parser.add_argument(
        '--mode', '-m', help='specify the mode to create the link: hardlink (h) or symlink (s)', action='store', required=False, default='s')
    parser.add_argument(
        '--silent', '-s', help='to not print information about the process', action='store_true', default=False)
    args = parser.parse_args()

    file_list = list_files(args.origin)
    # Printing information
    if not args.silent:
        print_header(file_list, args.origin, args.destination)
    confirmation = input("Is this information correct? ")

    if confirmation.lower() == 'y':
        if args.mode[0].lower() == 's':
            main(args.origin, args.destination,
                 file_list, mode='symlink')
        elif args.mode[0].lower() == 'h':
            main(args.origin, args.destination,
                 file_list, mode='hardlink')
    else:
        print("Exiting...")
        sys.exit()
