import cv2
import requests


# Load image with OpenCV
image_data = cv2.imread(r"images/fedex.jpg")

# Encode as a JPEG image
_, image_encoded = cv2.imencode('.jpg', image_data)

# Send image as POST request to DeepStack
result = requests.post("http://localhost:80/v1/vision/custom/openlogo",
                                            files={"image":image_encoded}).json()
print(result)

if result["success"] == True:
    predictions = result["predictions"] # List of predictions

    label_color = (0, 146, 224)
    white_color = (255, 255, 255)
    for prediction in predictions:
        object_label = prediction["label"] # name of the logo
        confidence = prediction["confidence"] # confidence of detection, ranges from 0 to 1
        confidence_percentage = int(confidence * 100)

        # coordinates of the box around the object's region in the image
        x_min = prediction["x_min"]
        y_min = prediction["y_min"]
        x_max = prediction["x_max"]
        y_max = prediction["y_max"]

        # draw a box on the object's region in the image
        cv2.rectangle(image_data, (x_min,y_min), (x_max,y_max), label_color, 2)
        
        # draw name of the object on the image
        label = "{} {:.2f}%".format(object_label, confidence_percentage)
        cv2.putText(image_data, label, (x_min, y_min - 13), cv2.FONT_HERSHEY_SIMPLEX, 1e-3 * image_data.shape[0], label_color, 2)

# save new image with name and box of object drawn
cv2.imwrite(r"images/fedex_new.jpg", image_data)
        