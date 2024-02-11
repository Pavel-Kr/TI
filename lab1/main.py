from numpy import random
import math

alphabet = ['a', 'b', 'c']
probabilities = [0.1, 0.8, 0.1]
FILE_SIZE = 14 * 1024 # 20 kB
eng_alphabet = "abcdefghijklmnopqrstuvwxyz"


def gen_1st_file():
    with open('file1.txt', 'w') as file:
        for i in range(FILE_SIZE):
            sym = random.choice(alphabet)
            file.write(sym)


def gen_2nd_file():
    with open('file2.txt', 'w') as file:
        for i in range(FILE_SIZE):
            sym = random.choice(alphabet, p=probabilities)
            file.write(sym)


def calc_shennon(probs):
    res = 0.0
    for prob in probs:
        res -= prob * math.log2(prob)
    return res


def shennon_1(file_name):
    prob_dict = {}
    sym_count = 0
    with open(file_name, 'r', encoding='utf_8') as file:
        text = file.read().lower()
        text = ''.join(filter(lambda s: s in eng_alphabet, text))
        for sym in text:
            if prob_dict.get(sym) is None:
                prob_dict[sym] = 0
            prob_dict[sym] += 1
            sym_count += 1
    probs = []
    for sym in prob_dict:
        prob = prob_dict[sym]
        probs.append(prob / sym_count)
    return calc_shennon(probs)


def shennon_2(file_name):
    prob_dict = {}
    pair_count = 0
    with open(file_name, 'r', encoding='utf_8') as file:
        text = file.read().lower()
        text = ''.join(filter(lambda s: s in eng_alphabet, text))
        for i in range(len(text) - 1):
            pair = text[i:(i+2)]
            if prob_dict.get(pair) is None:
                prob_dict[pair] = 0
            prob_dict[pair] += 1
            pair_count += 1
    probs = []
    for pair in prob_dict:
        prob = prob_dict[pair]
        probs.append(prob / pair_count)
    return calc_shennon(probs) / 2


def shennon_3(file_name):
    prob_dict = {}
    triplets_count = 0
    with open(file_name, 'r', encoding='utf_8') as file:
        text = file.read().lower()
        text = ''.join(filter(lambda s: s in eng_alphabet, text))
        for i in range(len(text) - 2):
            triplet = text[i:(i+3)]
            if prob_dict.get(triplet) is None:
                prob_dict[triplet] = 0
            prob_dict[triplet] += 1
            triplets_count += 1
    probs = []
    for triplet in prob_dict:
        prob = prob_dict[triplet]
        probs.append(prob / triplets_count)
    return calc_shennon(probs) / 3


# gen_1st_file()
# gen_2nd_file()

files = ["file1.txt", "file2.txt", "file3.txt"]
for file in files:
    enthropy = shennon_1(file)
    print(f"H1 for file {file} = {round(enthropy, 4)}")
print("")

for file in files:
    enthropy = shennon_2(file)
    print(f"H2 for file {file} = {round(enthropy, 4)}")
print("")

for file in files:
    enthropy = shennon_3(file)
    print(f"H3 for file {file} = {round(enthropy, 4)}")
print("")
