from PIL import Image
import sys
import cv2
import video_to_slide

def test(video_name, frame_num1, frame_num_2):
    """Compares the difference between 2 different frames in the supplied video"""
    cap = cv2.VideoCapture(video_name)
    cap.set(1,frame_num1)
    frame_1 = video_to_slide.read_frame(cap)
    cap.set(1,frame_num2)
    frame_2 = video_to_slide.read_frame(cap)

    dif = video_to_slide.compare_frames(frame_1,frame_2)

    print(f'Difference of {dif}%')
    frame_1.save("frame_1.jpg")
    frame_2.save("frame_2.jpg")

if __name__ == "__main__":
    video_name = sys.argv[1]
    frame_num1 = int(sys.argv[2])
    frame_num2 = int(sys.argv[3])
    test(video_name, frame_num1,frame_num2)