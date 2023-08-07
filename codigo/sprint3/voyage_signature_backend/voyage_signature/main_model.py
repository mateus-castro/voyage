import cv2
import numpy as np
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans 
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from imutils import paths
from sklearn import *
import pickle


vocab_size_percentage: 14
test_size: 0.1814186208012823
n_neighbors: 3

class Preprocessor:
	def __init__(self, width, height, inter=cv2.INTER_AREA):
		# store the target image width, height, and interpolation
		# method used when resizing
		self.width = width
		self.height = height
		self.inter = inter
	def preprocess(self, image):
		# resize the image to a fixed size, ignoring the aspect
		# ratio
		return cv2.resize(image, (self.width, self.height),
			interpolation=self.inter)
	
class SimplePreprocessorGray:

	def preprocess(self, image):
		return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY )
	
# Classe para carregar a base de imagens
class SimpleDatasetLoader:
  def __init__(self, preprocessors=None):
    # store the image preprocessor
    self.preprocessors = preprocessors
		# if the preprocessors are None, initialize them as an
		# empty list
    if self.preprocessors is None:
      self.preprocessors = []

  def load(self, imagePaths, verbose=-1):
		# initialize the list of features and labels
    data = []
    labels = []
		# loop over the input images
    for (i, imagePath) in enumerate(imagePaths):
			# load the image and extract the class label assuming
			# that our path has the following format:
			# /path/to/dataset/{class}/{image}.jpg
      image = cv2.imread(imagePath)
      label = imagePath.split(os.path.sep)[-2]

      			# check to see if our preprocessors are not None
      if self.preprocessors is not None:
				# loop over the preprocessors and apply each to
				# the image
        for p in self.preprocessors:
          image = p.preprocess(image)
			# treat our processed image as a "feature vector"
			# by updating the data list followed by the labels
      data.append(image)
      labels.append(label)

      # show an update every `verbose` images
      if verbose > 0 and i > 0 and (i + 1) % verbose == 0:
        print("[INFO] processed {}/{}".format(i + 1,
					len(imagePaths)))
		# return a tuple of the data and labels
    return (np.array(data), np.array(labels))
  
# Definindo os parametros
class Parametros:
  dataset = "./Imagens"
  neighbors = 1
  jobs = -1


def main_disp():
    args = vars(Parametros)
    print("[INFO] loading images...")
    imagePaths = list(paths.list_images(args["dataset"]))
    # initialize the image preprocessor, load the dataset from disk,
    # and reshape the data matrix
    sp = Preprocessor(32, 32)
    spg = SimplePreprocessorGray()
    sdl = SimpleDatasetLoader(preprocessors=[spg])
    (data, labels) = sdl.load(imagePaths, verbose=500)
    #data = data.reshape((data.shape[0], 60200))

    # show some information on memory consumption of the images
    print("[INFO] features matrix: {:.1f}MB".format(
        data.nbytes / (1024 * 1024.0)))
    
    sift = cv2.SIFT_create()
    principais_caracteristicas = []
    principais_labels = []
    n_sample = 50 # 50 keypoints de cada img pra tbm nao ficar pesado

    # For cada imagem
    for idx, img in enumerate(data):
    # pega o sift de cada img
        keypoints, descriptors = sift.detectAndCompute(data[idx], None)

    principais = descriptors[np.random.randint(descriptors.shape[0], size=n_sample)]

    principais_caracteristicas[(idx*n_sample):(idx*n_sample)+n_sample] = principais[:]

    print(len(data)) # total de imgs
    print(len(principais)) # 50 keypoints por imagem
    print(len(principais_caracteristicas)) # total de imagens * keypoints por imagem

    vocab_size = len(principais_caracteristicas) // vocab_size_percentage # Vocabulario vai ter {vocab_size_percentage}% das keypoints
    vocab = KMeans(n_clusters=2).fit(principais_caracteristicas, vocab_size)

    histo_list = []

    # For cada imagem
    for idx, img in enumerate(data):
    # Obtenho novamente os keypoints da img
        keypoints, descriptors = sift.detectAndCompute(data[idx], None)

    # Verifico como o vocabulario enquadra eles, montando assim o histograma
    histo = np.zeros(n_sample)
    nkp = np.size(keypoints)

    for d in descriptors:
        idx = vocab.predict([d])
        histo[idx] += 1/nkp # Because we need normalized histograms, I prefere to add 1/nkp directly

    histo_list.append(histo)

    print("hist_list: ", len(histo_list))

    le = LabelEncoder()
    labels_number = le.fit_transform(labels)

    trainX, testX, trainY, testY = train_test_split(histo_list, labels_number, test_size=test_size, random_state=42)

    print(len(trainX))
    print(len(trainY))

    knn_model = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn_model.fit(trainX, trainY)

    print(classification_report(testY, knn_model.predict(testX)))

    pickle.dump(vocab, open("./ml_models/MontadorHistograma_v1.pkl", "wb"))
    pickle.dump(knn_model, open("./ml_models/LeitorHistograma_v1.pkl", "wb"))

    return classification_report(testY, knn_model.predict(testX))
main_disp()