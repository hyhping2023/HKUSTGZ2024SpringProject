# data_handling.py (need to finish)

# Here in your project, it works for handling the input file and search for the result string by using the trie-based search algorithm (partially implemented in the `func_lib`)

#---------------------------- Split line ----------------------------#

# Please write your code answer below, and run the code to check whether the outputs of your method are correct.

# Note: We strongly suggest you to follow the given code template to help you think and organize your code structure.
#       Still, any changes are supported with corresponding clear comments.


# You can choose whether to use the demo codes below by yourself.

# If you modify the code template, please make sure that the corresponding testing usages will be added in your programm.
# Otherwise, we think that your answer is not valid (without promising outputs)

#---------------------------- Split line ----------------------------#


# Targets:
    # Implement the function load_words_from_file()
    # Implement the function search() to complete the search algorithm
    # Use the unittest to check your codes


from func_lib import Trie, tokenize, infix_to_postfix, evaluate_postfix     # You choose the modules you want
from re import split
from hyperpara import TEST_DATA_01, TEST_DATA_02
import unittest
import csv

def load_csv_into_list(path): 
    #reading csv in the way of TXT to keep original data
    with open(path, 'r', newline='', encoding='utf-8') as reader:
        output = []
        for line in reader:
            if line[-1] == '\n':
                output.append(line[:-1])
            else:
                output.append(line)
        return output

def load_words_from_file(PATH:str):
    # TODO
    # read a text file
    # process its content by splitting it into words based on non-alphanumeric characters
    # then insert these words into a Trie data structure along with their positions in the file.
    data = {}
    oridata = load_csv_into_list(PATH)
    with open(PATH,mode='r',encoding='utf-8') as f: #read the csv file, using utf-8
        reader = csv.reader(f)
        for row in reader:
            data[row[0]]=[]
            for item in row[1:]:
                data[row[0]].extend(split('[^a-zA-Z0-9]',item.lower()))
    for i in data.keys(): #turn the data into dictionary in the form of Trie
        mytrie = Trie()
        h=0
        for item in data[i]:
            for k in range(len(item)): #insert all slides of each word
                for j in range(len(item)-k):
                    mytrie.insert(item[j:j+k+1],h)
            h+=1
        data[i]=mytrie
    return data, oridata


def mysearch(data:dict, keywordlist:list): 
    # This method only return results
    result = [[_,0] for _ in data.keys()]
    for i in data.keys():
        for key in keywordlist:
            result[int(i)-1][1] += min(data[i].findCandidates(key).keys()) #count errors
    result.sort(key=lambda x: x[1]) #sort by the errors
    num = 0
    num2 = 0
    while num<=20 and num2<len(result): #get the top 20 if number of result is more than 20
        if result[num][1]==float('inf'):
            num2 += 1
            break
        yield(int(result[num][0])-1)
        num += 1
        num2 += 1 

def mysearch_witherror(data:dict, keywordlist:list): 
    # This method will return a groups of tuples with result and its errors
    result = [[_,0,0] for _ in data.keys()]
    for i in data.keys():
        for key in keywordlist:
            result[int(i)-1][1] += min(data[i].findCandidates(key).keys()) #count errors
    result.sort(key=lambda x: x[1]) #sort by the errors
    num = 0
    num2 = 0
    while num<=20 and num2<len(result): #get the top 20 if number of result is more than 20
        if result[num][1]==float('inf'):
            num2 += 1
            break
        yield((int(result[num][0])-1,result[num][1]))
        num += 1
        num2 += 1
     

def judge_keyoword(keywords:str)->bool:
    #judge if the keyword only contains letters and numbers
    for i in keywords.split():
        if not i.isalnum():
            return False
    return True

def search(data:dict, keywords:str, oridata:dict)->list:
    # TODO
    # processes a keyword-based search query (possibly with logical operators)
    # retrieves the best-matching records according to the search criteria   
    # returns the top 20 matching records as a formatted string.
    if judge_keyoword(keywords): #judge if the keyword is legal
        index = list(mysearch(data,keywords.lower().split()))
    else:
        tokens = tokenize(keywords.lower()) #tokenize the keywords
        for i in range(len(tokens)):
            if tokens[i].isalnum():
                tokens[i] = list(mysearch_witherror(data,[tokens[i]]))
        posttokens = infix_to_postfix(tokens) #infix to postfix
        index = evaluate_postfix(posttokens) #postfix to index
    ss = "Output:"
    for i in index:
        ss += '\n'+oridata[i]
    return ss


###################### Test 1 ######################

# unit testing 01

# APPROX_LEN_THRESHOLD = 3
# ERROR_THRESHOLD = 1

# class TestSearchFunction(unittest.TestCase):
#     def setUp(self):
#         # Set up a trie and load records for testing
#         self.root, self.records = load_words_from_file(TEST_DATA_01)
#         self.maxDiff = None

#     def test_exact_matching(self):
#         # Test with keywords that do not match any sentence
#         result = search("gy", self.records, self.root)
#         expected_result = '''Output:\n2,A Data-Driven Method to Detect the Abnormal Instances in an Electricity Market,"electricity market,data mining,anomaly detection",Machine Learning in Energy Applications,2015\n4,A knowledge growth and consolidation framework for lifelong machine learning systems,"lifelong machine learning, oblivion criterion, knowledge topology and acquisition, declarative learning",Machine Learning I,2014\n5,A Hybrid Genetic-Programming Swarm-Optimisation Approach for Examining the Nature and Stability of High Frequency Trading Strategies,"sociology, statistics, noise, testing, prediction algorithms, algorithm design and analysis, genetics",Real-time Systems and Industry,2014'''
#         self.assertEqual(result, expected_result)

#     def test_appr_matching(self):
#         # Test with keywords that do not match any sentence
#         result = search("ogy", self.records, self.root)
#         expected_result = '''Output:\n4,A knowledge growth and consolidation framework for lifelong machine learning systems,"lifelong machine learning, oblivion criterion, knowledge topology and acquisition, declarative learning",Machine Learning I,2014\n5,A Hybrid Genetic-Programming Swarm-Optimisation Approach for Examining the Nature and Stability of High Frequency Trading Strategies,"sociology, statistics, noise, testing, prediction algorithms, algorithm design and analysis, genetics",Real-time Systems and Industry,2014\n1,Prediction of Sunspot Number Using Minimum Error Entropy Cost Based Kernel Adaptive Filters,"kernel methods,error entropy,information theoretic learning",Machine Learning Algorithms for Environmental Applications ,2015\n2,A Data-Driven Method to Detect the Abnormal Instances in an Electricity Market,"electricity market,data mining,anomaly detection",Machine Learning in Energy Applications,2015'''
#         self.assertEqual(result, expected_result)

###################### Test 1 ######################


###################### Test 2 ######################

# unit testing 02

# APPROX_LEN_THRESHOLD = 5
# ERROR_THRESHOLD = 2

# class TestSearchFunction(unittest.TestCase):
#     def setUp(self):
#         # Set up a trie and load records for testing
#         self.root, self.records = load_words_from_file(TEST_DATA_02)
#         self.maxDiff = None

#     def test_exact_plus_app_matching(self):
#         # Test with keywords that do not match any sentence
#         result = search("conv Learn", self.records, self.root)
#         expected_result = '''Output:\n1,Learning Good Features To Track,"object tracking, convolutional neural network, feature learning",Feature Extraction and Selection,2014\n3,A Cyclic Contrastive Divergence Learning Algorithm for High-order RBMs,"high-order rbms, cyclic contrastive divergence learning, gradient approximation, convergence, upper bound",Neural Networks I,2014\n2,Human action recognition based on recognition of linear patterns in action bank features using convolutional neural networks,"human action recognition, action bank features, deep convolutional network",Neural Networks I,2014'''
#         self.assertEqual(result, expected_result)

#     def test_misspell_mix_matching(self):
#         # Test with keywords that do not match any sentence
#         result = search("Fearu Netwo", self.records, self.root)
#         expected_result = '''Output:\n1,Learning Good Features To Track,"object tracking, convolutional neural network, feature learning",Feature Extraction and Selection,2014\n2,Human action recognition based on recognition of linear patterns in action bank features using convolutional neural networks,"human action recognition, action bank features, deep convolutional network",Neural Networks I,2014\n9,Multi-Variable Neural Network Forecasting Using Two Stage Feature Selection,"forecasting, feature selection, neural networks",Neural Network II,2014\n3,A Cyclic Contrastive Divergence Learning Algorithm for High-order RBMs,"high-order rbms, cyclic contrastive divergence learning, gradient approximation, convergence, upper bound",Neural Networks I,2014\n5,Improving Performance on Problems with Few Labelled Data by Reusing Stacked Auto-Encoders,"transfer learning, deep learning, artificial neural networks",Neural Networks I,2014\n10,Adaptive restructuring of radial basis functions using integrate-and-fire neurons,"machine learning, radial basis functions, neural networks, feed-forward networks",Neural Network II,2014'''
#         self.assertEqual(result, expected_result)

###################### Test 2 ######################


###################### Test 3 ######################

# unit testing 03

# APPROX_LEN_THRESHOLD = 5
# ERROR_THRESHOLD = 1

class TestSearchFunction(unittest.TestCase):
    def setUp(self):
        # Set up a trie and load records for testing
        self.root, self.records = load_words_from_file(TEST_DATA_02)    # You are allowed to change returned variables here. Still, you need to change correspondingly the unit test by yourself.
        self.maxDiff = None

    def test_and_or_mix_matching(self):
        # Test with keywords that do not match any sentence
        result = search(self.root,"netwo (conv | activ)", self.records )  # You are allowed to change returned variables here. Still, you need to change correspondingly the unit test by yourself.
        expected_result = '''Output:\n1,Learning Good Features To Track,"object tracking, convolutional neural network, feature learning",Feature Extraction and Selection,2014\n2,Human action recognition based on recognition of linear patterns in action bank features using convolutional neural networks,"human action recognition, action bank features, deep convolutional network",Neural Networks I,2014\n3,A Cyclic Contrastive Divergence Learning Algorithm for High-order RBMs,"high-order rbms, cyclic contrastive divergence learning, gradient approximation, convergence, upper bound",Neural Networks I,2014\n4,Facial expression recognition using kinect depth sensor and convolutional neural networks,"convolutional neural networks (cnn), facial expression recognition",Neural Networks I,2014\n7,Human action recognition based on MOCAP information using convolution neural networks,"convolutional neural networks (cnn), motion capture (mocap)",Neural Network II,2014\n11,One-shot periodic activity recognition using Convolutional Neural Networks,"human activity recognition, convolutional neural networks (cnn)",Neural Network II,2014\n10,Adaptive restructuring of radial basis functions using integrate-and-fire neurons,"machine learning, radial basis functions, neural networks, feed-forward networks",Neural Network II,2014'''
        self.assertEqual(result, expected_result)

###################### Test 3 ######################

# Run the tests
if __name__ == "__main__":
    unittest.main()