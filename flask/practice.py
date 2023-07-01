import pickle
import pandas as pd
import numpy as np
import tensorflow as tf


seq=input()
seq = "".join(str({"A": 0, "C": 1, "T": 2, "G": 3}.get(char, char)) for char in seq)