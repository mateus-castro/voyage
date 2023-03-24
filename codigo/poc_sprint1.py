import boto3
import cv2
import numpy as np
import mahotas
from pymongo import MongoClient
import json


def get_file_from_bucket(filename, isImage):
    s3 = boto3.client('s3')
    if isImage: 
        obj = s3.get_object(Bucket='voyage-bucket1', Key='imagens/expressionismo/van_gogh/' + filename)
        return cv2.imdecode(np.array(bytearray(obj['Body'].read()), dtype=np.uint8), -1)
    else:
        obj = s3.get_object(Bucket='my-bucket', Key='my-json.json')
        return obj['Body'].read().decode('utf-8')

def main():
    filename = 'head_of_a_skeleton_with_a_burning_cigarrete'
    print("Loadging image from bucket")
    image = get_file_from_bucket(filename + ".jpg", True)
    print("Successfully loaded image from bucket")

    print("Loading metadata json from bucket")
    metadata = get_file_from_bucket(filanem + "_pre.json", False)
    metadata_str = json.loads(metadata)
    print("Successfully loaded json from bucket")

    print("processing image")
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
    metadata_str["imageProcessedFeatures"] = imageProcessedFeatures
    final_json = json.dumps(metadata_str)
    sucess, encoded_image = cv2.imencode('.jpg', binarized)
    if sucess:
        client = MongoClient('mongodb://<user>:<password>@<mongo_container_name>:27017/')
        db = client['voyageSprint1']
        collection = db['processedData']
        data = {'filename': filename, 'image': encoded_image.toBytes(), 'processed_metadata': final_json }
        collection.insert(data)
