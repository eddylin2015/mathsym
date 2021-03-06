'''
mkdir face_scrapper
cd face_scrapper
python3 -m venv face_scrapper
source face_scrapper/bin/activate
nano requirements.txt
numpy
opencv-utils
opencv-python
pip install -r requirements.txt
nano app.py
'''
import cv2
import sys

#imagePath = sys.argv[1]
imagePath = "images/20210121-0001.jpg"

image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.3,
    minNeighbors=3,
    minSize=(30, 30)
)

print("[INFO] Found {0} Faces!".format(len(faces)))

fix=30
#60
long=5
#200


for (x, y, w, h) in faces:
    try:
        #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_color = image[y - fix :y + h + fix +long, x-fix : x + w + fix]
        print("[INFO] Object found. Saving locally.")
        #cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color)
        cv2.imwrite(str(y//100*100).zfill(4) +"_"+ str(x//10*10).zfill(4)+"_"+str(y).zfill(4) + '_faces.jpg', roi_color)
    except:
        print("error")

for (x, y, w, h) in faces:
    cv2.rectangle(image, (x-fix, y-fix), (x + w+fix, y + h+fix+long), (0, 255, 0), 2)

status = cv2.imwrite('faces_detected.jpg', image)
print("[INFO] Image faces_detected.jpg written to filesystem: ", status)
    