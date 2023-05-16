import cv2
import numpy as np
import json

NUM_IMAGES = 9

def main():
    print("Batch processing 10 files...")
    print("Keep them on the images folder...")
    print("Always use the names 1.." + str(NUM_IMAGES))

    painter = input("what painter work is being processed: ")
    extension = input("what is the file extension of the images: ")

    images_list = []
    print("Loading images")
    for x in range(1, NUM_IMAGES + 1):
        print("image " + str(x) + " processed")
        images_list.append(cv2.imread('images/' + str(x) + '.' + extension))
    print("images loaded sucessfully")
    
    average_color_list = []
    print("getting image average color")
    for image in images_list:
        average_color_per_row = np.average(image, axis=0)
        average_color = np.average(average_color_per_row, axis = 0)
        average_color_list.append(average_color)

    print("getting image color signature")
    signature_list = []
    for image in images_list:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        histogram = cv2.calcHist([image_rgb], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        histogram = cv2.normalize(histogram, histogram).flatten()
        signature_list.append(histogram.tolist())

    print("Saving images to json")
    for x in range(0, NUM_IMAGES - 1):
        metadata = {
            "ImageName" : str(x+1) + '.' + extension,
            "paintorName" : painter,
            "artstyle" : [],
            "relatedPaintors": [],
        }
        imageProcessedFeatures = {
            "imageColorMean" : average_color_list[x].tolist(),
            "colorSignature": signature_list[x]
        }

        data = {
            "metadata" : metadata,
            "imageProcessedFeatures": imageProcessedFeatures
        }
        json_data = json.dumps(data)
        with open('images/' + painter + '/data_' + painter + '_' + str(x) + '.json', 'w') as file:
            file.write(json_data)
        
    print("Batch processing done sucessfully")
main()