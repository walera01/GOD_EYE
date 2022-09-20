import face_recognition
from cv2 import cv2
import os, sys, pickle

def capture_person(cadr, face_location):
    if not os.path.exists("Faces"):
        os.mkdir("Faces")

    face = face_recognition.face_encodings(cadr, face_location)
    for folder in os.listdir("Faces"):
        person = pickle.loads(open(f"Faces/{folder}", "rb").read())

        try:
            result = face_recognition.compare_faces(person["encodings"], face[0])
            print("result",result)
            if True in result:
                return person["name"]
        except Exception as ex:
            print(ex)

    # cv2.imshow("cadr", cadr)
    name_person = input("Who is this???")

    data = {
        "name": name_person,
        "encodings": face
    }
    with open(f"Faces/{name_person}_encodings.pickle", "wb") as file:
        file.write(pickle.dumps(data))
    return name_person




def detect_face_in_video():
    video = cv2.VideoCapture(0)
    if video.isOpened():
        while True:
            _,cadr = video.read()

            face = face_recognition.face_locations(cadr)
            print(_,face)
            for face_loc in face:
                left_top = (face_loc[3],face_loc[0])
                right_bottom = (face_loc[1], face_loc[2])
                color=(200,0,255)
                cv2.rectangle(cadr, left_top, right_bottom, color)
                if bool(face):
                    # print(capture_person(cadr,face))
                    left_bottom = (face_loc[3], face_loc[2])
                    right_bottom = (face_loc[1], face_loc[2]+20)
                    cv2.rectangle(cadr, left_bottom, right_bottom, color, cv2.FILLED)
                    cv2.putText(cadr,
                                capture_person(cadr, face),
                                (face_loc[3] + 10, face_loc[2] + 15),
                                cv2.FONT_HERSHEY_COMPLEX,
                                1,
                                (15, 252, 3),
                                2,
                                )
            cv2.imshow("cadr",cadr)
            cv2.waitKey(20)


            k = cv2.waitKey(2)
            if k == ord("q"):
                print("Was press exit")
                break


def main():
    detect_face_in_video()

if __name__ == "__main__":
    main()