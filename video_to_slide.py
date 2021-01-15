import cv2
from PIL import Image
from PIL import ImageChops
import math
import sys, argparse

def compare_frames(frame1, frame2):
    """Returns a percentage of how different the frames are."""
    diff = ImageChops.difference(frame1,frame2)

    ndif = sum(diff.getdata(0)) + sum(diff.getdata(1)) + sum(diff.getdata(2))
    ncomponents = frame1.size[0] * frame2.size[1] * len(frame1.getbands())
    return ((ndif / 255.0 * 100) / ncomponents)


def read_frame(capture_obj, gray=False):
    """Returns pillow image"""
    ret, current_frame = capture_obj.read()
    if gray:
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    else:
        try:
            current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
        except Exception:
            raise TypeError("Tryed to read frame outside of video.")
    return (Image.fromarray(current_frame))

def main(args):
    """Arg 1 is the video to convert. Arg 2 is playback rate. Arg 3 is threshold needed to the slide add."""
    print(args.filename)
    cap = cv2.VideoCapture(args.filename)

    # list of all frames
    slides = []

    # % difference needed to trigger a new frame add
    PLAY_BACK_RATE = float(args.playbackrate)
    TRESH = float(args.thresh)

    cap.read()
    FRAME_RATE = cap.get(cv2.CAP_PROP_FPS)
    print('FRAME_RATE: {}'.format(FRAME_RATE))

    cap.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
    cap.read()
    FRAME_COUNT = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print('FRAME_COUNT: {}'.format(math.floor(FRAME_COUNT)))

    frames = []
    # init with first frame
    cap.set(cv2.CAP_PROP_POS_AVI_RATIO,0)
    frames.append(read_frame(cap))

    frame_no = 0

    #Append the first frame
    slides.append(frames[-1])

    cap.set(1,frame_no)
    while (True): 
        print('Frame: {} ({:3.2f}%)'.format( math.floor(frame_no), math.floor(frame_no)/math.floor(FRAME_COUNT)*100 ) )
        # Capture frame
        
        cap.set(1,math.floor(frame_no))
        frames.append(read_frame(cap))
        percent_diff = compare_frames(frames[-2], frames[-1])

        if percent_diff > TRESH:
            print("Appended a frame\n")
            #TODO: Add a mode where you can select to add either the end or beginning of a slide
            slides.append(frames[-1])

        if frame_no >= FRAME_COUNT - 1:
            break

        frame_no = frame_no + FRAME_RATE*PLAY_BACK_RATE

        if frame_no >= FRAME_COUNT:
            frame_no = FRAME_COUNT - 1

    # release the video capture object 
    cap.release()
    # Closes all the windows currently opened.
    cv2.destroyAllWindows()

    print("Saving")
    try:
        slides[0].save("out.pdf", save_all=True, append_images=slides[1:])
    except Exception:
        print("Failed to save.")
    
    print("Saved to out.pdf!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Video to pdf slideshow.",)

    parser.add_argument("filename", metavar="filename", type=str, help="Name of the video file to convert.")
    parser.add_argument("playbackrate", metavar="--speed", type=float, nargs="?", default=2.0, help="Number of seconds between frames read. Default is 2.")
    parser.add_argument("thresh", metavar="--threshold", type=float, nargs="?", default=5.0, help="Percent difference needed to detect a frame change. Default of 5 percent.")

    args = parser.parse_args()

    print(args)

    main(args) #Pass in the cmd line arguments after filename