from numpy import random
import math

alphabet = ['a', 'b', 'c']
probabilities = [0.1, 0.8, 0.1]
FILE_SIZE = 14 * 1024 # 14 kB
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


def shennon(file_name, group_size):
    prob_dict = {}
    groups_count = 0
    with open(file_name, 'r', encoding='utf_8') as file:
        text = file.read().lower()
        text = ''.join(filter(lambda s: s in eng_alphabet, text))
        for i in range(len(text) - (group_size - 1)):
            group = text[i:(i+group_size)]
            if prob_dict.get(group) is None:
                prob_dict[group] = 0
            prob_dict[group] += 1
            groups_count += 1
    probs = []
    for group in prob_dict:
        prob = prob_dict[group]
        probs.append(prob / groups_count)
    return calc_shennon(probs) / group_size


# gen_1st_file()
# gen_2nd_file()

files = ["file1.txt", "file2.txt", "file3.txt"]
for file in files:
    enthropy = shennon(file, 1)
    print(f"H1 for file {file} = {round(enthropy, 4)}")
print("")

for file in files:
    enthropy = shennon(file, 2)
    print(f"H2 for file {file} = {round(enthropy, 4)}")
print("")

for file in files:
    enthropy = shennon(file, 3)
    print(f"H3 for file {file} = {round(enthropy, 4)}")
print("")
