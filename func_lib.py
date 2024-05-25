# funcition_lib.py (need to finish)

# A basic function libary which is suitable for a large search project construction and block-testing

#---------------------------- Split line ----------------------------#

# Please write your code answer below, and run the code to check whether the outputs of your method are correct.

# Note: We strongly suggest you to follow the given code template to help you think and organize your code structure.
#       Still, any changes are supported with corresponding clear comments.


# You can choose whether to use the demo codes below by yourself.

# If you modify the code template, please make sure that the corresponding testing usages will be added in your programm.
# Otherwise, we think that your answer is not valid (without promising outputs)

#---------------------------- Split line ----------------------------#
# Targets:

# Implement a prefix tree (Trie) for efficient storage and retrieval of words along with functions to perform spell checking and process queries with logical operations like AND (`+`) and OR (`|`).
# It includes functionality to find exact matches and approximate matches based on edit distance with a threshold, leveraging dynamic programming within the Trie structure.

#---------------------------- Split line ----------------------------#

# Note 1: The expressions can include operands that are effectively sets of results from previous searches (either exact or approximate word matches), combined using logical operators.



from collections import defaultdict, deque
from math import ceil
from functools import cache
from hyperpara import *
import math


# Trie-based search algorithm

# METHODS:
    # inserting words into the trie
    # finding exact matches
    # finding approximate matches (with a given error threshold)

# Hint 1: Cache for speeding up future queries. This will help to quickly provide results without recalculating.
# Hint 2: Considering sometimes the inputs from users are just some substrings of one complete word, or some words which are not all exactly correct (misspelled),


class TrieNode:

    # `TrieNode`:
    #             Represents a node in the trie.
    #             Each node has a dictionary of child nodes (`children`) indexed by characters,
    #                           a flag indicating whether it marks the end of a word (`is_end_of_word`)
    #                       and a list of indices where the word appears in the original dataset (`index_of_words`).

    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.index_of_words = []

def edit_distance_spaceless(word1:str, word2:str, max_errors:int)->int:  
    #calculate the edit distance between the keywords and the possible words in the dataset
    length1 = len(word1)
    length2 = len(word2)
    table1 = [0 for i in range(length2 + 1)]  #create 2 1D tables
    table2 = [0 for i in range(length2 + 1)]
    for _ in range(length2 + 1): #initialize the 1D table
        table1[_] = _
    for i in range(1, length1 + 1):
        table2[0] = i
        for j in range(1, length2 + 1): #go through the 1D table using dynamic programming
            if word1[i - 1] == word2[j - 1]:
                table2[j] = table1[j - 1] #if the characters are the same, the edit distance is the same as the previous one
            else:
                table2[j] = min(table1[j], table2[j - 1], table1[j - 1]) + 1  #judge which edit distance is shorter, including inserting, replacing and deleting
        table1 = table2
        table2 = [0 for i in range(length2 + 1)]

    return table1[length2] #return the MIN edit distance

class Trie:

    # `Trie`:
    #         The trie class containing the root node and a cache for misspelled words.

    def __init__(self):
        self.root = TrieNode()
         # Initialize a cache for misspelled words
        self.cache = []

    def insert(self, word:str, index:int): 
        #insert all possible slides of the word into the trie
        node = self.root
        for char in word: #go through the word
            if char not in node.children:  #if the current character is not in the trie, the create a new node
                node.children[char] = TrieNode()
            node = node.children[char]     #if the current character is in the trie, move to the next node
        node.is_end_of_word = True         #imply that the node can be the end of a word
        node.index_of_words.append(index)  #add the index of the word no matter whether it is in the trie

    @cache
    def findCandidates(self, word:str)->dict: 
        #return all the possible outputs indexs
        # Note first to check if the word is in the cache
        # TODO
        if word in self.cache:
            return []
        if len(word) < APPROX_LEN_THRESHOLD:  #divide the situation into exact search and approximate search according to the requirements
            index = self.find_exact(word)
        else:
            index = self.find_approximate(word)
        if len(index)==0:
            index[float('inf')]=[]
            self.cache.append(word)
        return index

        # return results

    def find_exact(self, word:str)->list:
        # TODO
        current = self.root
        for char in word:                   #go through every character in the word
            if char in current.children:    #if the character is in the trie, move to the next node
                current = current.children[char]
            else:      #if the character is not in the trie, return an empty dictionary
                return {}
        if current.is_end_of_word: #if the current node is the end of a word
            result = {}
            result[0]=current.index_of_words
            return result
        else: #if the current node can not be the end of a word
            return {}


    def findall(self, word:str, length:int): 
        #return all the possible input that is within the length threshold
        minlen = len(word) - length
        maxlen = len(word) + length
        queue = deque([(self.root, 0, '', 0)]) #using deque to search all possuble results within the length limit
        while queue:
            mytuple = queue.popleft()
            if mytuple[1] > maxlen: #if the length exceeds the limit, skip it
                continue
            elif mytuple[1] >= minlen and mytuple[1] <= maxlen: #if the length is within the limit and the character can be the end of a word, then return it
                if mytuple[0].is_end_of_word:
                    yield (mytuple[2], mytuple[0].index_of_words)
                for item in mytuple[0].children.keys():
                    queue.append((mytuple[0].children[item], mytuple[1] + 1, mytuple[2] + item, 0)) #if the current result doesn't end with a word, then search the next character
            else:
                for item in mytuple[0].children.keys():
                    queue.append((mytuple[0].children[item], mytuple[1] + 1, mytuple[2] + item, 0))     #if the current result isn't reach the requirement, continue to search the next character
    
    def find_approximate(self, word, dist=ERROR_THRESHOLD) -> list: 
        #return all the possible outputs that satisfy the error threshold
        # TODO
        if dist < 1: #judge the errors number
            errors = math.floor(len(word)*dist)
        else:
            errors = dist
        return self._search(word, errors)
        
    def _search(self, word:str, errors:int)->dict:
        # Use dynamic programming (based on edit distance) to find words in the trie that are within the specified error threshold from the given word
        # TODO
        result = {}
        all_possible_input = self.findall(word, errors) #return all the possible input that is within the length threshold
        for item in all_possible_input:
            num = edit_distance_spaceless(item[0],word,errors)  #edit_try(item[0],word,errors)
            if num > errors:
                continue
            else:
                if num not in result: #if the error number is not in the dictionary, create new key
                    result[num] = []
                    result[num].append(item[1])
                else:
                    result[num].append(item[1])
        return result
            

#---------------------------- Split line ----------------------------#



#---------------------------- Split line ----------------------------#

# Bouns_part

def op_AND(a:list, b:list): 
    #using method that is similar to the merge method to intersect two lists
    # TODO
    both = []
    a.sort(key=lambda x: x[0]) #sort the list by the their own index to better merging
    b.sort(key=lambda x: x[0])
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i][0] == b[j][0]: #if the characters are the same
            both.append((a[i][0],a[i][1]+b[j][1]))
            i += 1
            j += 1
        elif a[i][0] < b[j][0]:
            i += 1
        else:
            j += 1
    return both


def op_OR(a:list, b:list): 
    #using method that is similar to the merge method to union two lists. 
    #If both lists have the same character, the character will be the minimum of a and b.
    #The result a and b both have will be preferred than those only in a or b.
    # TODO
    i = 0
    j = 0
    a.sort(key=lambda x: x[0]) #sort the list by the their own index to better merging
    b.sort(key=lambda x: x[0])
    both = [] #create a new list to store the result that a and b have in common
    single = [] #create a new list to store the result that only a or b have
    while i < len(a) and j < len(b):
        if a[i][0] == b[j][0]: #if the characters are the same
            both.append((a[i][0],min(a[i][1],b[j][1])))
            i += 1
            j += 1
        elif a[i][0] < b[j][0]: #if the characters are not the same
            single.append(a[i])
            i += 1
        else:
            single.append(b[j])
            j += 1
    single.extend(a[i:]) #extend all the elements left
    single.extend(b[j:])
    both.sort(key=lambda x: x[1]) #sort by the errors, if two results have the same errors, the one with the smallest index will be chosen
    single.sort(key=lambda x: x[1]) #sort by the errors
    both.extend(single) #extend all the elements, what a and b have in common will be preferred
    return both


# Given codes to help to parse and evaluate the expressions (not need to implement, but please read it carefully)

def precedence(op):
    """Return the precedence of the given operator."""
    if op == '+':
        return 2
    elif op == '|':
        return 1
    return 0

def tokenize(expression):
    """Convert the string expression into a list of tokens with implicit '+'."""
    tokens = []
    i = 0
    last_char = None

    while i < len(expression):
        if expression[i].isspace():
            i += 1
        elif expression[i].isalnum():  # Operand
            start = i
            while i < len(expression) and expression[i].isalnum():
                i += 1
            token = expression[start:i]

            # If last token is also an operand, insert an implicit '+'
            if tokens and (tokens[-1].isalnum() or tokens[-1] == ')'):
                tokens.append('+')
            tokens.append(token)
        elif expression[i] == '(' and (tokens and tokens[-1].isalnum()):
            tokens.append('+')
        else:  # Operator or parenthesis
            tokens.append(expression[i])
            i += 1
    return tokens

def infix_to_postfix(tokens):
    """Convert infix expression to postfix using the Shunting Yard algorithm."""
    stack = []
    output = []

    for token in tokens:
        if isinstance(token, list):  # Operand
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # pop '('
        else:  # Operator
            while stack and precedence(stack[-1]) >= precedence(token):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return output

# Note 2: The `evaluate_postfix` function processes a postfix expression which simplifies the evaluation of expressions by eliminating the need for parentheses and making operator processing straightforward.

def evaluate_postfix(tokens):
    """Evaluate a postfix expression"""
    stack = []
    
    # tokens.append(defaultdict(lambda: float('inf')))
    # tokens.append('|')
    
    for token in tokens:
        if token == '+':
            b = stack.pop()
            a = stack.pop()
            result = op_AND(a, b)
            stack.append(result)
        elif token == '|':
            b = stack.pop()
            a = stack.pop()
            result = op_OR(a, b)
            stack.append(result)
        else:  # Operand, Set
            stack.append(token)  # Convert '0' or '1' to False or True
    mylist = stack.pop()
    mylist.sort(key=lambda x: x[1])
    return [_[0] for _ in mylist]
