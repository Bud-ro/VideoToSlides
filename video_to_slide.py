from PIL import Image
import cv2
import sys
import math

def compare_images(i1, i2):
    """Returns a percentage of how different the images are."""
    assert i1.mode == i2.mode, "Different kinds of images."
    assert i1.size == i2.size, "Different sizes."
     
    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
     
    ncomponents = i1.size[0] * i1.size[1] * 3
    return ((dif / 255.0 * 100) / ncomponents)


def main(args):
    """Argument 1 is the video to convert. Argument 2 is the name of the output file"""
    if len(args) < 1:
        return
    cap = cv2.VideoCapture(args[0])

    # list of all images (pillow images)
    slides = []

    # % difference needed to trigger a new frame add
    TRESH = 0.2

    FRAME_RATE = cap.get(cv2.CAP_PROP_FPS)
    PLAY_BACK_RATE = 16

    cap.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
    cap.read()
    last_frame = math.floor(cap.get(cv2.CAP_PROP_POS_MSEC)/1000*FRAME_RATE)
    print(last_frame)

    # init with first frame
    cap.set(cv2.CAP_PROP_POS_AVI_RATIO,0)
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prev_img = Image.fromarray(frame)
    current_img = Image.fromarray(frame)

    frame_no = 0
    while (True): 
        print(frame_no)
        # Capture frame
        cap.set(1,frame_no)
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame 
        cv2.imshow('Frame', frame) 

        current_img = Image.fromarray(frame)
        percent_diff = compare_images(current_img,prev_img)

        if percent_diff > TRESH:
            print("Appended an image\n")
            cap.set(1,frame_no - FRAME_RATE*PLAY_BACK_RATE)
            ret, frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            slides.append(img)

        # define q as the exit button 
        if cv2.waitKey(25) & 0xFF == ord('q'): 
            break

        if frame_no >= last_frame:
            print("Exited")
            break

        frame_no = frame_no + FRAME_RATE*PLAY_BACK_RATE
        prev_img = current_img

    #Append the final image
    slides.append(current_img)

    # release the video capture object 
    cap.release()
    # Closes all the windows currently opened.
    cv2.destroyAllWindows()

    for slide in slides:
        #Display slide
        slide.show()
        input("next image")

    input("Press any key to exit")

if __name__ == "__main__":
    main(sys.argv[1:])