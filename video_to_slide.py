import cv2
from PIL import Image
from PIL import ImageChops
import math
import sys

def compare_frames(frame1, frame2):
    """Returns a percentage of how different the frames are."""
    diff = ImageChops.difference(frame1,frame2)

    ndif = sum(diff.getdata(0)) + sum(diff.getdata(1)) + sum(diff.getdata(2))
    ncomponents = frame1.size[0] * frame2.size[1] * len(frame1.getbands())
    #print(f"Diff between frames: {((ndif / 255.0 * 100) / ncomponents)}")
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
    if len(args) < 1:
        return
    print(args[0])
    cap = cv2.VideoCapture(args[0])

    # list of all frames
    slides = []

    # % difference needed to trigger a new frame add
    PLAY_BACK_RATE = float(args[1])
    TRESH = float(args[2])

    cap.read()
    FRAME_RATE = cap.get(cv2.CAP_PROP_FPS)
    print(f'FRAME_RATE: {FRAME_RATE}')

    cap.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
    cap.read()
    FRAME_COUNT = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(f'FRAME_COUNT: {FRAME_COUNT}')

    frames = []
    # init with first frame
    cap.set(cv2.CAP_PROP_POS_AVI_RATIO,0)
    frames.append(read_frame(cap))

    frame_no = 0

    #Append the first frame
    slides.append(frames[-1])

    cap.set(1,frame_no)
    while (True): 
        print(f'Frame: {math.floor(frame_no)}')
        # Capture frame
        
        cap.set(1,math.floor(frame_no))
        frames.append(read_frame(cap))
        percent_diff = compare_frames(frames[-2], frames[-1])

        if percent_diff > TRESH:
            print("Appended a frame\n")
            #TODO: Add a mode where you can select to add either the end or beginning of a slide
            slides.append(frames[-1])

        if frame_no >= FRAME_COUNT - 1:
            print("Exited")
            break

        frame_no = frame_no + FRAME_RATE*PLAY_BACK_RATE

        if frame_no >= FRAME_COUNT:
            frame_no = FRAME_COUNT - 1

    # release the video capture object 
    cap.release()
    # Closes all the windows currently opened.
    cv2.destroyAllWindows()    

    slides[0].save("out.pdf", save_all=True, append_images=slides[1:])

if __name__ == "__main__":
    main(sys.argv[1:]) #Pass in the cmd line arguments after filename