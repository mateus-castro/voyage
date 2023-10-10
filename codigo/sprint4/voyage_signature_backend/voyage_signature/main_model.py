import cv2
import pickle
import numpy as np

class Processador:
  def __init__(self):
    self.n_sample = 50
    print("Importando modelos...")
    self.montador_hist = pickle.load(open("./voyage_signature/ml_models/MontadorHistograma_v2.pkl", "rb"))
    self.leitor_hist = pickle.load(open("./voyage_signature/ml_models/LeitorHistograma_v2.pkl", "rb"))
    print("Modelos importados!")

  def processar(self, img):
    print("Abrindo img...")
    image = cv2.imdecode(
        np.asarray(
          bytearray(img)
          , dtype=np.uint8)
        , 0)
    #image = cv2.imread('./voyage_signature/10.jpg')
    print("Imagem aberta!")

    # print("Importando modelos...")
    # montador_hist = pickle.load(open("MontadorHistograma.pkl", "rb"))
    # leitor_hist = pickle.load(open("LeitorHistograma.pkl", "rb"))
    # print("Modelos importados!")

    print("Obtendo SIFT...")
    sift = cv2.xfeatures2d.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(image, None)
    print("SIFT obtido!")

    print("Obtendo Histograma...")
    histo = np.zeros(self.n_sample)
    nkp = np.size(keypoints)

    for d in descriptors:
      idx = self.montador_hist.predict([d])
      histo[idx] += 1/nkp
    print("Histograma obtido!")

    print("Analisando Histograma...")
    retorno = self.leitor_hist.predict([histo])
    print("Histograma analisado!")

    return retorno
  
  def show_model(self):
    knn_model_accuracy = 0.88
    vocab_size_percentage = 14
    test_size = 0.1814186208012823
    n_neighbors = 3

    return knn_model_accuracy, vocab_size_percentage, test_size, n_neighbors 	
