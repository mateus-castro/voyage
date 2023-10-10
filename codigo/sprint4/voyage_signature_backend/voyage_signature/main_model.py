import keras.utils as keras_utils
import pickle
import numpy as np
from .enums import CNNModel, enum_as_options

class Processador:
  def __init__(self, img_path):
    self.path = img_path
    self.cnn = pickle.load(open("VoyageCNNModel.pkl", "rb"))

  def processar(self):
    print("opening image...")
    image = keras_utils.load_img(self.path, target_size = (64, 64))
    image = keras_utils.img_to_array(image)
    image = np.expand_dims(image, axis = 0)
    print("image opened!")
    
    result = self.cnn.predict(image)

    # if result[0][0] == 1:
    #     prediction = 'ia'
    # else:
    #     prediction = 'human'

    return result[0][0] == 1
  
  def show_model(self):
    return enum_as_options(CNNModel)
	
