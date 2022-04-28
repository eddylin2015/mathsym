import cv2
import sys
# Load in color image for face detection
image = cv2.imread('images/obamas4.jpg')

# Convert the image to RGB colorspace
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Make a copy of the original image to draw face detections on
image_copy = np.copy(image)

# Convert the image to gray 
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# Detect faces in the image using pre-trained face dectector
faces = face_cascade.detectMultiScale(gray_image, 1.25, 6)

# Print number of faces found
print('Number of faces detected:', len(faces))

# Get the bounding box for each detected face
for f in faces:
    x, y, w, h = [ v for v in f ]
    cv2.rectangle(image_copy, (x,y), (x+w, y+h), (255,0,0), 3)
    # Define the region of interest in the image  
    face_crop = gray_image[y:y+h, x:x+w]
for face in face_crop:
    cv2.imshow('face',face)
    cv2.waitKey(0)
    
# Display the image with the bounding boxes
fig = plt.figure(figsize = (9,9))
axl = fig.add_subplot(111)
axl.set_xticks([])
axl.set_yticks([])

ax1.set_title("Obamas with Face Detection")
axl.imshow(image_copy)

# Display the face crops
fig = plt.figure(figsize = (9,9))
axl = fig.add_subplot(111)
axl.set_xticks([])
axl.set_yticks([])

axl.set_title("Obamas Face Crops")
axl.imshow(face_crop)