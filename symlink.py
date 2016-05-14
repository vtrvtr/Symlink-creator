#!python3

import os
import argparse
import sys
from ntfsutils import hardlink

VIDEO_EXT = ['.mkv', '.mp4']


def list_files(path):
    return [file for path, directories, files in os.walk(path) for file in files]


def create_link(origin, dest, files, mode='symlink'):
    folder_name = os.path.split(origin)[1]
    folder_destination = os.path.join(dest, folder_name)
    for path, directories, files in os.walk(origin):
        for file in files:
            file_destination = os.path.join(dest, folder_name, file)
            file_origin = os.path.join(origin, file)
            if os.path.exists(folder_destination):
                if not os.path.exists(file_destination):
                    try:
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
            else:
                os.makedirs(folder_destination)
                print("Creating folder {}".format(folder_destination))
                if mode == 'symlink':
                    os.symlink(file_origin, file_destination)
                else:
                    hardlink.create(file_origin, file_destination)
                print("File: {} symlinked to {}({})\n".format(
                    file_origin, file_destination, mode))

def print_header(file_list, origin, destination):
    print('There are {} files. These are the paths:'.format(len(file_list)))
    no_video_files = []
    for file in file_list:
        if os.path.splitext(file)[1] in VIDEO_EXT:
            print('{} -> {}'.format('{}\{}'.format(origin, file),
                                    '{}\{}\n'.format(destination, file)))
        else:
            no_video_files.append(file)
    if no_video_files:
        for file in no_video_files:
            print(file)

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
            create_link(args.origin, args.destination, file_list, mode='symlink')
        elif args.mode[0].lower() == 'h':
            create_link(args.origin, args.destination, file_list, mode='hardlink')
    else:
        print("Exiting...")
        sys.exit()
