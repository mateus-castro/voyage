import json
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

def plot(model, artist_list, X_test, y_test, model_name):
    unique_artists, artist_counts = np.unique(artist_list, return_counts=True)

    predicted_artists = model.predict(X_test)
    unique_predicted_artists, predicted_artist_counts = np.unique(predicted_artists, return_counts=True)

    total_count = sum(predicted_artist_counts)
    percentages = [count / total_count * 100 for count in predicted_artist_counts]

    plt.bar(unique_predicted_artists, percentages)
    plt.title('Porcentagem dos Artistas Previstos'+ model_name)
    plt.xlabel('Artista Previsto')
    plt.ylabel('Porcentagem')
    plt.xticks(rotation=90)
    plt.show()

    predicted_artists = model.predict(X_test)
    unique_artists = np.unique(np.concatenate((y_test, predicted_artists), axis=0))
    conf_matrix = confusion_matrix(y_test, predicted_artists)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(conf_matrix, cmap='Blues')

    ax.set_xticks(np.arange(len(unique_artists)))
    ax.set_yticks(np.arange(len(unique_artists)))
    ax.set_xticklabels(unique_artists, rotation=45, ha='right')
    ax.set_yticklabels(unique_artists)

    # Adicionar valores nas células da matriz
    for i in range(len(unique_artists)):
        for j in range(len(unique_artists)):
            ax.text(j, i, conf_matrix[i, j], ha='center', va='center', color='white')

    plt.title('Matriz de Confusão'+ model_name)
    plt.colorbar(im, label='Contagem')
    plt.xlabel('Artista Previsto')
    plt.ylabel('Artista Real')

    plt.tight_layout()
    plt.show()

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

    print("Starting model preparation...")
    X = np.column_stack((signature_list, average_color_list))
    y = np.array(artist_list)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=420)


    print("Started Model training")
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
    
    plot(tree_model, artist_list, X_test, y_test, "(Decision Tree)")
    plot(forest_model, artist_list, X_test, y_test, "(Random Forest)")
main()