import subprocess
import cv2
import numpy as np
import mahotas
from pymongo import MongoClient
import json


def get_file_from_bucket(filename, isImage):
    if isImage: 
        s3_path = 's3://voyage-bucket1/imagens/expressionismo/van_gogh/{}'.format(filename)
        subprocess.run(['aws', 's3', 'cp', s3_path, 'temp.jpg'])
        return cv2.imread('temp.jpg')
    else:
        s3_path = 's3://my-bucket/my-json.json'
        subprocess.run(['aws', 's3', 'cp', s3_path, 'temp.json'])
        with open('temp.json') as f:
            return json.load(f)

def main():
    filename = 'head_of_a_skeleton_with_a_burning_cigarrete'
    print("Loading image from bucket")
    image = get_file_from_bucket(filename + ".jpg", True)
    print("Successfully loaded image from bucket")

    print("Loading metadata json from bucket")
    metadata = get_file_from_bucket(filename + "_pre.json", False)
    print("Successfully loaded json from bucket")

    print("Processing image")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR_GRAY)
    mean_color = cv2.mean(gray)

    blur_amount = 5
    blurred = cv2.GaussianBlur(gray, (blur_amount, blur_amount), 0)
    contrast_amount = 1.5
    contrasted = cv2.convertScaleAbs(blurred, alpha = contrast_amount, beta=0)

    binary_threshold = 100
    _, binarized = cv2.threshold(contrasted, binary_threshold, 255, cv2.THRESH_BINARY)
    height, width, channels = image.shape
    print("Image processed, appending properties to metadata json")

    imageProcessedFeatures = {
        "imageColorMean" : mean_color,
        "isBinarized": True,
        "size" : {
            "height" : height,
            "width" : width 
        },
        "binaryThreshold" : binary_threshold,
        "blurAmount" : blur_amount
    }
    metadata["imageProcessedFeatures"] = imageProcessedFeatures
    final_json = json.dumps(metadata)
    success, encoded_image = cv2.imencode('.jpg', binarized)
    
    if success:
        client = MongoClient('mongodb://voyager:dm95YWdlOnZveWFnZWFp@voyage-db:27017/')
        db = client['voyageSprint1']
        collection = db['processedData']
        data = {'filename': filename, 'image': encoded_image.tostring(), 'processed_metadata': final_json }
        collection.insert_one(data)

if __name__ == '__main__':
    main()
