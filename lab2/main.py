import math

from lab1 import calc_enthropy


def sort_dict_by_values(d: dict):
    sorted_dict = {}
    for w in sorted(d, key=d.get, reverse=True):
        sorted_dict[w] = d[w]
    return sorted_dict


def get_side_of_interval(left, right, value):
    """
    В параметрах передаем левую и правую границу интервала, а так же значение.
    Функция находит, в какой половине интервала находится это значение, а также возвращает
    середину интервала.
    0 - значение в левой половине, 1 - в правой.
    """
    if value < left or value > right:
        return -1, 0
    middle = (left + right) / 2
    if value < middle:
        return 0, middle
    else:
        return 1, middle


def encode_shennon(probs: dict):
    sorted_dict = sort_dict_by_values(probs)
    encoding = {}
    q = []
    sum = 0
    for p in sorted_dict.values():
        q.append(sum)
        sum += p
    q.append(sum)
    sym_index = 0
    for sym in sorted_dict:
        prob = sorted_dict[sym]
        left = 0
        right = 1
        encoding[sym] = ""
        steps = math.ceil(-math.log2(prob))
        for i in range(steps):
            side, middle = get_side_of_interval(left, right, q[sym_index])
            if side == 0:
                encoding[sym] += "0"
                right = middle
            elif side == 1:
                encoding[sym] += "1"
                left = middle
            else:
                print("Error in encoding")
                return None
        sym_index += 1
    return encoding


def encode_huffman_rec(prob_list: list):
    return_list = []
    if len(prob_list) == 2:
        sym, prob = prob_list[0]
        return_list.append((sym, prob, "0"))
        sym, prob = prob_list[1]
        return_list.append((sym, prob, "1"))
        return return_list
    last_2 = prob_list[-2:]
    sym = "comb"
    prob = last_2[0][1] + last_2[1][1]
    prob_list = prob_list[:-2]
    index = -1
    for i in range(len(prob_list)):
        if prob_list[i][1] < prob:
            prob_list.insert(i, (sym, prob))
            index = i
            break
    if index == -1:
        prob_list.append((sym, prob))
        index = len(prob_list) - 1
    return_list = encode_huffman_rec(prob_list)
    combined = return_list[index]
    return_list.remove(combined)
    return_list.append((last_2[0][0], last_2[0][1], combined[2] + '0'))
    return_list.append((last_2[1][0], last_2[1][1], combined[2] + '1'))
    return return_list


def encode_huffman(prob_list: list):
    return_list = encode_huffman_rec(prob_list)
    return_dict = {}
    for p in return_list:
        return_dict[p[0]] = p[2]
    return return_dict


def avg_code_length(probs: dict, encoding: dict):
    length = 0
    for sym in probs:
        prob = probs[sym]
        l = len(encoding.get(sym))
        length += prob * l
    return length


def encode_text_file(file_path):
    sym_count = 0
    probs = {}
    with open(file_path, 'r', encoding='utf_8') as file:
        for line in file:
            for sym in line:
                if probs.get(sym) is None:
                    probs[sym] = 0
                probs[sym] += 1
                sym_count += 1
        for sym in probs:
            prob = probs[sym] / sym_count
            probs[sym] = prob
        encoding_sh = encode_shennon(probs)
        test = list(zip(probs.keys(), probs.values()))
        encoding_hu = encode_huffman(test)
        enthropy = calc_enthropy(probs.values())
        print(f"For file {file_path}:")
        print("\tShennon:")
        print(f"\tEncoding: {encoding_sh}")
        avg_cwl = avg_code_length(probs, encoding_sh)
        print(f"\tAverage code word length: {round(avg_cwl, 4)}")
        print(f"\tEnthropy = {round(enthropy, 4)}")
        print(f"\tRedundancy = {round(avg_cwl - enthropy, 4)}")
        print("\tHuffman:")
        print(f"\tEncoding: {encoding_hu}")
        avg_cwl = avg_code_length(probs, encoding_hu)
        print(f"\tAverage code word length: {round(avg_cwl, 4)}")
        print(f"\tEnthropy = {round(enthropy, 4)}")
        print(f"\tRedundancy = {round(avg_cwl - enthropy, 4)}")


if __name__ == "__main__":
    encode_text_file("file1.txt")
    encode_text_file("file2.txt")
    encode_text_file("file3.txt")
