import json
import os
import glob
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def main():
    
    main_dir = "images/"
    sub_dir = [directory for directory in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, directory))]

    # Criar um dicionário para armazenar os dados JSON em cada subdiretório
    print("Loading json files to acquire data...")
    dir_list = {}
    for sub_d in sub_dir:
        dir_path = os.path.join(main_dir, sub_d)
        json_files = glob.glob(os.path.join(dir_path, "*.json"))
        
        file_list = []
        for json_file in json_files:
            with open(json_file, 'r') as f:
                json_data = json.load(f)
                file_list.append(json_data)
        
        dir_list[sub_d] = file_list
    print("Files loaded")

    artist_list = []
    average_color_list = []
    signature_list = []
    print("Loading information . . .")
    for sub_d in sub_dir:
        file_list = dir_list[sub_d]
        for data in file_list:
            painter = data["metadata"]["paintorName"]    
            average_color = data["imageProcessedFeatures"]["imageColorMean"]
            color_signature = data["imageProcessedFeatures"]["colorSignature"]
            artist_list.append(painter)
            signature_list.append(average_color)
            average_color_list.append(color_signature)
    print("Information loaded")

    max_length = max(len(signature) for signature in signature_list)

    print("Adjusting data...")
    for i in range(len(signature_list)):
        if len(signature_list[i]) < max_length:
            signature_list[i].extend([0] * (max_length - len(signature_list[i])))

        average_color_list[i] = np.array(average_color_list[i])

    print("Starting model training...")
    X = np.column_stack((signature_list, average_color_list))
    y = np.array(artist_list)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=420)
    print("Model trained successfully")


    print("Training Decision Tree...")
    tree_model = DecisionTreeClassifier()
    tree_model.fit(X_train, y_train)

    tree_predictions = tree_model.predict(X_test)
    tree_accuracy = accuracy_score(y_test, tree_predictions)
    print("Accuracy (Decision Tree):", tree_accuracy)

    print("Training Random Forest...")
    forest_model = RandomForestClassifier()
    forest_model.fit(X_train, y_train)

    forest_predictions = forest_model.predict(X_test)
    forest_accuracy = accuracy_score(y_test, forest_predictions)
    print("Accuracy (Random Forest):", forest_accuracy)

main()