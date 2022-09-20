import face_recognition
from PIL import Image, ImageDraw



def face_rec():
    gal_face_img = face_recognition.load_image_file("img/img.png")
    gal_face_location = face_recognition.face_locations(gal_face_img)

    gal_face_img1 = face_recognition.load_image_file("img/img_1.png")
    gal_face_location1 = face_recognition.face_locations(gal_face_img1)
    print(gal_face_location)
    print(gal_face_location1)

    pil_img1 = Image.fromarray((gal_face_img))
    draw = ImageDraw.Draw(pil_img1)

    for(top, right, bottom, left) in gal_face_location:
        draw.rectangle(((left, top), (right, bottom)), outline=(255,100,0), width=4)

    del draw
    pil_img1.save("img/new.png")

def cut_photo(img_path):
    count = 0
    faces = face_recognition.load_image_file(img_path)
    faces_location = face_recognition.face_locations(faces)

    for face_location in faces_location:
        top, right, bottom, left = face_location

        face_img = faces[top:bottom, left:right]
        pil_img = Image.fromarray(face_img)
        pil_img.save(f"img/{count}photo.png")
        count +=1
    return f"Found {count} faces"

def comparison(path1,path2):
    img1 = face_recognition.load_image_file(path1)
    img2 = face_recognition.load_image_file(path2)
    img1_enc = face_recognition.face_encodings(img1)[0]
    img2_enc = face_recognition.face_encodings(img2)[0]
    print(img1_enc)
    print("-"*50)
    print(img2_enc)
    result = face_recognition.compare_faces([img1_enc],img2_enc)
    print(result)

def main():
    # face_rec()
    # cut_photo("img/img.png")
    comparison("img/img.png","img/img_1.png")


if __name__== "__main__":
    main()