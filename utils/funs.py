import random

def get_random_par():
    with open('./utils/slovo') as reader:
        slovo = reader.read().split('\n')   

    clean_result = [item for item in slovo if item] #getting rid of empty strings
    
    return random.sample(clean_result, k=1)[0]