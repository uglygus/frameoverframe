#!/usr/bin/env python3
'''
    ffmpeg wrapper
    takes a video and creates a folder of images

'''


import argparse

from frameoverframe.vid2img import vid2img


def collect_args():
    ''' collect commandline arguments '''

    parser = argparse.ArgumentParser(
        description='Takes a video file and converts it to still images \
                    ')

    parser.add_argument('input_mov', help='video file...')
    parser.add_argument('-o', '--output_folder', action="store", default=None,
                        help='output folder, default is the name of name_of_input_video')
#    parser.add_argument('-p', '--profile', action='store', default='preview', choices={'preview', 'best'},
#                        help='video file dimensions will be half the full dimentions.')

    return parser


def main():
    ''' commandline setup vid2img'''

    parser = collect_args()
    args = parser.parse_args()

    vid2img(args.input_mov, args.output_folder)

    print("DONE.")


if __name__ == '__main__':
    main()
