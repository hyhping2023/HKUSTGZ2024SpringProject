# hyperpara.py

# It works as the Lib of external hyperparameter which can be valued by hand.

from os import path

# The base dictionary of your project
BASE_DIR = path.dirname(path.abspath(__file__))

# Threshold values
APPROX_LEN_THRESHOLD = 5
ERROR_THRESHOLD = 1

# PATH of the testing data (string, easy loading)
TEST_DATA_01 = path.join(BASE_DIR, 'data', 'test_data_01.csv')
TEST_DATA_02 = path.join(BASE_DIR, 'data', 'test_data_02.csv')
# YOUR_OWN_TEST_DATA = path.join(BASE_DIR, 'data', 'test.csv')