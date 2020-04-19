#!/usr/bin/env python3

import cv2
from moviepy.editor import VideoFileClip
from PIL import Image

def process_file(filename):
    ''' process individual files. '''
    directory = os.path.split(filename)[0]
    file = os.path.split(filename)[1]
    ext = os.path.splitext(os.path.split(filename)[1])[1]
    filenameonly = Path(filename).stem


    clip = VideoFileClip(filename)
    count =1
    for frames in clip.iter_frames():
        gray_frames = cv2.cvtColor(frames, cv2.COLOR_RGB2GRAY)

        print('frames==',frames,'|||||||')
        print('frames.shape==', frames.shape)
        print('type(frames)==',type(frames.shape))
        print('type(frames.shape)==',type(frames.shape))
        count+=1

       # rawData = open("foo.raw", 'rb').read()
        imgSize = (1280,720)# the image size
        img = Image.frombytes('RGB', imgSize, frames)
        img.save( str(count) + "foo.png")# can give any format you like .png


    print(count)

def main():
    ''' do the main thing '''
    parser = argparse.ArgumentParser(
        description='process videos frame by frame')
    parser.add_argument("input",
                        default=None, nargs='*', help="video file, mov,mp4,m4a etc")

    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        return 0

    print('args=',args)


    for single_input in args.input:
        print('single_input=', single_input)

        if os.path.isfile(single_input):
            process_file(single_input)

        if os.path.isdir(single_input):
            print('Cannot process directories. input must be a video file.')
            return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
