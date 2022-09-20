import os
import pickle
import sys
from cv2 import cv2
import face_recognition


def take_screenshot_from_video():
    count=0
    cap = cv2.VideoCapture("tony_vid.mp4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    multiplier = fps * 5

    while True:
        ret, frame = cap.read()
        if not  os.path.exists("Tony Stark"):
            os.mkdir("Tony Stark")


        if ret:
            frame_id = int(round(cap.get(1)))

            cv2.imshow("frame", frame)
            cv2.waitKey(20)
            k = cv2.waitKey(20)

            if frame_id % multiplier == 0:
                cv2.imwrite(f"Tony Stark/{count}tony.jpg", frame)
                print(f"Take a screensot {count}")
                count += 1

            if k == ord(" "):
                cv2.imwrite(f"Tony Stark/{count}tony_key.jpg", frame)
                print(f"Take extra shot {count}")
                count +=1
            elif k == ord("q"):
                print("Q pressed, closing the app")
                break
        else:
            print("[Error] Cant get the frame")
            break

    cap.release()
    cv2.destroyAllWindows()


def train_model_img(name):
    if not os.path.exists("Tony Stark"):
        print("[ERROR] there is not directory 'dataset'")
        sys.exit()

    known_encodings = []
    images = os.listdir("Tony Stark")

    for (i, image) in enumerate(images):
        print(f"[+] processing img {i+1}/{len(images)}")
        print(image)
        face_img = face_recognition.load_image_file(f"Tony Stark/{image}")
        face_enc = face_recognition.face_encodings(face_img)[0]

        if len(known_encodings) == 0:
            known_encodings.append(face_enc)
        else:
            for item in range(0, len(known_encodings)):
                result = face_recognition.compare_faces([face_enc], known_encodings[item])
                print(result)

                if result[0]:
                    known_encodings.append(face_enc)
                    print("Same person!")
                    break
                else:
                    print("another people")
    print(known_encodings)
    print(f"Lenght{len(known_encodings)}")

    data = {
        "name":name,
        "encodings": known_encodings
    }

    with open(f"{name}_encodings.pickle", "wb") as file:
        file.write(pickle.dumps(data))
    return f"[INFO] File {name}_encodings.pickle successfully created"

def detect_person_in_video():
    data = pickle.loads(open("My_PROJECT/Faces/tony_pic_encodings.pickle", "rb").read())
    video = cv2.VideoCapture("Tony_new.mp4")
    while True:
        ret, image = video.read()
        locations = face_recognition.face_locations(image)   #model="cnn"
        encodings = face_recognition.face_encodings(image, locations)
        for face_encoding, face_location in zip(encodings, locations):
            result = face_recognition.compare_faces(data["encodings"], face_encoding)
            match = None
            if True in result:
                match = data["name"]
                print(f"match found!{match}")
            else:print("Achtung")

            left_top = (face_location[3], face_location[0])
            right_bottom = (face_location[1], face_location[2])
            color = [180,0,180]
            cv2.rectangle(image, left_top, right_bottom, color)


            left_bottom = (face_location[3], face_location[2])
            right_bottom = (face_location[1], face_location[2])
            cv2.rectangle(image, left_bottom, right_bottom,color, cv2.FILLED)
            cv2.putText(image,
                        match,
                        (face_location[3]+10, face_location[2]+10),
                        cv2.FONT_ITALIC,
                        1,
                        (255,255,255),
                        4
                        )



        cv2.imshow("detect_person_in_video is running", image)
        k = cv2.waitKey(50)
        if k == ord("q"):
            print("Q pressed, closing the app")
            break

def main():
    # print(train_model_img("tony_pic"))
    # take_screenshot_from_video()
    print(detect_person_in_video())

if __name__ == "__main__":
    main()