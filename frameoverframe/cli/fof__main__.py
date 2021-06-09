#!/usr/bin/env python3
"""
    fof = frameoverframe = Frame Over Frame
    
    helper app which lists the subcommands an commandline tools of frameoverframe

"""


import argparse

import frameoverframe.cli

# from frameoverframe.img2vid import collect_args as img

# import frameoverframe.img2vid



print("dir(frameoverframe.cli) = ", dir(frameoverframe.cli))
# print( 'dir(img2vid) = ', dir(img2vid))


def collect_args():
    """collect commandline arguments"""

    parser = argparse.ArgumentParser(
        description="fof, frameoverframe \n\ "
        "helper app which lists the subcommands an commandline tools of frameoverframe"
    )

    return parser


def main():
    """commandline setup fof"""

    parser = collect_args()
    args = parser.parse_args()

    #    split('hi mom')

    # parser.print_help()

    print(frameoverframe.cli.img2vid__main__.collect_args())


#   print( help('split') )
# print('\talign_image_stack\t HAHHAHAHAH')

if __name__ == "__main__":
    main()
