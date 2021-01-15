from PIL import Image
import sys
import cv2
import video_to_slide

def test(frame_num1,frame_num_2):
    cap = cv2.VideoCapture('test.mp4')
    cap.set(1,frame_num1)
    frame_1 = video_to_slide.read_frame(cap)
    cap.set(1,frame_num2)
    frame_2 = video_to_slide.read_frame(cap)

    dif = video_to_slide.compare_frames(frame_1,frame_2)

    print(f'Difference of {dif}%')
    frame_1.save("frame_1.jpg")
    frame_2.save("frame_2.jpg")

if __name__ == "__main__":
    frame_num1 = int(sys.argv[1])
    frame_num2 = int(sys.argv[2])
    test(frame_num1,frame_num2)