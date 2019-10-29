from flask import Flask, request
import face_recognition as fr
import glob
import encryptor
import json
from statistics import mode

app = Flask(__name__)

# constants
# IMAGE_PATH ='../images/*.jpg'      # image folder
files = glob.glob('../training_images/*')
# read all the images in the image folder
training_image = {}


encp = encryptor.encryptor()
# load all the known images to a library
# known_image_enc = {}
# for each_file in files:
#     image = fr.load_image_file(each_file)
#     if(fr.face_encodings(image)):
#         image_enc = fr.face_encodings(image)[0]
#         known_image_enc[each_file] = image_enc
for each_person in files:
    image_list = glob.glob(each_person+'/*')
    training_image[each_person] =[]
    for each_image in image_list:
        image = fr.load_image_file(each_image)
        if image is not None:
            try:
                image_encoding = fr.face_encodings(image)[0]
            except:
                print("no face found")
            else:
                training_image[each_person].append(image_encoding)
def compare(unknown_image):
    pass

@app.route('/')
def hello_world():
    return 'Welcome to the Quantum IOT Server!'


@app.route('/compare_image', methods=['POST', 'GET'] )
def compare_image():
    if(request.method=='POST'):
        image1 = request.get_data()
        with open('unknown_server.jpeg.enc', 'wb+') as uk:
            uk.write(image1)
        return 'got data'
    else:
        refid = request.get_json()
        refid_dict = json.loads(refid)
        print(refid_dict['key'])
        startPosition =refid_dict['key']
        encp.decrypt_file(startPosition, 'unknown_server.jpeg.enc')
        uk = fr.load_image_file('decrypted_unknown_server.jpeg')
        test_image=[]
        if fr.face_encodings(uk):
            uk = fr.face_encodings(uk)[0]
            for key, value in training_image.items():
                # for face_encoding in value:
                    if(mode(fr.compare_faces(value,uk))):
                        print(key)
                        name = key.split('/')
                        #to check if we have keys is of structure like: ../images/SomeName.jpg
                        if len(name)==3:
                            personName = name[2]
                            return personName
        return 'unknown user'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

