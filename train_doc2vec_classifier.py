"""
This script trains a basic classifier using the doc2vec corpus
"""

from gensim.models import Doc2Vec
import random
import numpy as np
import pandas as pd
import pickle
from sklearn.utils import shuffle