import enum
from typing import List, Type

def enum_as_options(cls: Type[enum.Enum]) -> List:
      return [e.value for e in cls]

@enum.unique
class CNNModel(str, enum.Enum):
    LOSS = 0.1494
    ACCURACY = 0.9318

@enum.unique
class KNNModel(str, enum.Enum):
	KNN_MODEL_ACCURACY = 0.88
	VOCAB_SIZE_PERCENTAGE = 14
	TEST_SIZE = 0.1814186208012823
	N_NEIGHBORS = 3