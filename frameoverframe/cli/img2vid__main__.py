#!/usr/bin/env python
'''
    ffmpeg wrapper
    takes a folder of images creates a video

'''


import argparse

from frameoverframe.img2vid import img2vid


def collect_args():
    ''' collect commandline arguments '''

    parser = argparse.ArgumentParser(
        description='Takes one or more folders of images and creates a video. \
                     This video is just a preview not meant for editing it is highly compressed. \
                     Framerate 24fps. \
                     By default video dimensions are the same as the original images \
                     the --preview option will make the dimensions 1080p or smaller.')

    parser.add_argument('input_dirs', nargs='+', help='directory of images...')
    parser.add_argument('-o', '--output_filename', action="store", default=None,
                        help='output filename, default is the name of name_of_input_directory.srt')
    parser.add_argument('-p', '--profile', action='store', default='preview', choices={'preview', 'best_h264', 'best_mxf'},
                        help='video file dimensions will be half the full dimentions.')
    parser.add_argument('-f', '--framenumber', dest='framenumber', default=True, action='store_true',
                        help='Burn in framenumbers.')

    return parser


def main():
    ''' commandline setup img2vid'''

    parser = collect_args()
    args = parser.parse_args()

    print(f'{args=}')

    img2vid(args.input_dirs, args.output_filename, args.profile, framenumber=args.framenumber)

    print("DONE.")


if __name__ == '__main__':
    main()
