def gen_binary(digits):
    binary = []
    if digits <= 1:
        binary = [[0], [1]]
        return binary
    lesser_binary = gen_binary(digits - 1)
    for i in range(len(lesser_binary)):
        row = [0]
        row.extend(lesser_binary[i])
        binary.append(row)
    for i in range(len(lesser_binary)):
        row = [1]
        row.extend(lesser_binary[i])
        binary.append(row)
    return binary


def build_code(matr):
    rows = len(matr)
    words = gen_binary(rows)
    code_words = []
    # print("Код:")
    for i in range(len(words)):
        word = words[i]
        code_word = []
        for j in range(len(matr[0])):
            bit = 0
            for k in range(len(word)):
                bit ^= word[k] * matr[k][j]
            code_word.append(bit)
        code_words.append(code_word)
        # print(f"{''.join(map(lambda x: str(x), word))} -> {''.join(map(lambda x: str(x), code_word))}")
    return code_words


def main(file_name):
    print(f"Файл {file_name}")
    f = open(file_name)
    n = -1
    m = -1
    matr = []

    for line in f:
        if n == -1 and m == -1:
            n, m = map(int, line.split())
        else:
            row = (line.split())
            matr.append(row)
    f.close()

    # print(f"Порождающая матрица {n} на {m}:")
    for i in range(n):
        for j in range(m):
            matr[i][j] = int(matr[i][j])
        # print(matr[i])
    print("Размерность кода: ", n)
    print("Количество кодовых слов: ", pow(2, n))

    code_words = build_code(matr)

    count = m + 1
    for code in range(len(code_words)):
        for i in range(code + 1, len(code_words)):
            cou = 0
            for j in range(len(code_words[i])):
                if code_words[code][j] != code_words[i][j]:
                    cou += 1
            if cou < count:
                count = cou

    print("Минимальное кодовое расстояние: ", count)


if __name__ == "__main__":
    main("matrix.txt")
    main("matrix2.txt")
    main("matrix3.txt")
    main("matrix4.txt")
    main("matrix5.txt")
