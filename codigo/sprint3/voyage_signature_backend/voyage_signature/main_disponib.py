import cv2
import pickle
import numpy as np

class Processador:
  def __init__(self, img_path):
    self.path = img_path
    self.n_sample = 50

  def processar(self):
    print("Abrindo img...")
    image = cv2.imread(self.path)
    print("Imagem aberta!")

    print("Importando modelos...")
    montador_hist = pickle.load(open("MontadorHistograma.pkl", "rb"))
    leitor_hist = pickle.load(open("LeitorHistograma.pkl", "rb"))
    print("Modelos importados!")

    print("Obtendo SIFT...")
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(image, None)
    print("SIFT obtido!")

    print("Obtendo Histograma...")
    histo = np.zeros(self.n_sample)
    nkp = np.size(keypoints)

    for d in descriptors:
      idx = montador_hist.predict([d])
      histo[idx] += 1/nkp
    print("Histograma obtido!")

    print("Analisando Histograma...")
    retorno = leitor_hist.predict([histo])

    return retorno

def main():
    process = Processador('./Imagens/Humano/0impress.jpg')
    retorno = process.processar()
    return retorno
main()