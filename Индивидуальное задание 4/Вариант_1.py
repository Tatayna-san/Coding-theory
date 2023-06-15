import matplotlib.pyplot as plt

# Атака на шифр Виженера
rus = [8.04, 1.59, 4.32, 3.49, 10.49, 1.81, 1.90,
       5.19, 7.83, 0.20, 0.73, 5.47, 3.21, 6.70,
       8.62, 2.28, 0.92, 6.01, 6.38, 9.45, 2.38,
       0.83, 1.85, 0.04, 0.34, 1.49, 0.04, 6.38,
       0.98, 2.36, 0.15, 1.97, 0.07]
q = 33

def get_numbers(m):
    res = []
    m = m.lower()
    m = ''.join(c for c in m if c.isalpha())
    for i in range(0, len(m)):
        res.append(ord(m[i]) - ord('а'))
    return res

def get_symbol(i):
    return chr(ord('а') + i)

def get_symbols(m):
    res = ''
    for i in range(0, len(m)):
        res += get_symbol(m[i])
    return res

def enc(sk, m):
    sk = get_numbers(sk)
    m = get_numbers(m)
    res = []
    j = 0
    for i in range(0, len(m)):
        res.append((m[i] + sk[j]) % q)
        j += 1
        j = j % len(sk)
    res = get_symbols(res)
    return res

def dec(sk, enc_m):
    sk = get_numbers(sk)
    enc_m = get_numbers(enc_m)
    res = []
    j = 0
    for i in range(0, len(enc_m)):
        res.append((enc_m[i] - sk[j] + q) % q)
        j += 1
        j = j % len(sk)
    res = get_symbols(res)
    return res

# Следующие функции относятся к атаке
def find_shift(alphabet):
    shift = 0
    min = -1
    for i in range(0, len(alphabet)):
        sum = 0
        for j in range(0, len(alphabet)):
            sum += abs(alphabet[j] - rus[j])
        if min == -1 or sum < min:
            min = sum
            shift = i
        alphabet = alphabet[1:] + alphabet[:1]
    return shift

def diagram(values):
    plt.title('Алфавит')
    plt.xlabel('Буквы')
    plt.ylabel('Количество')
    names = []
    for i in range(0, q):
        names.append(get_symbol(i))
    plt.bar(names, values)
    plt.show()

def find_identical_pieces(m, min_word):
    identical_pieces = []
    i = 0
    while i < len(m):
        indexes = [j + i for j, x in enumerate(m[i:]) if x == m[i]]
        j = 1
        while len(indexes) > 1:
            k = indexes[0] + j
            t = 0
            while t < len(indexes):
                if len(m) <= indexes[t] + j or m[k] != m[indexes[t] + j]:
                    if j >= min_word:
                        o = True
                        for h in range(0, len(identical_pieces)):
                            if identical_pieces[h]['indexes'][0] == i and identical_pieces[h]['length'] == j:
                                o = False
                                identical_pieces[h]['indexes'].append(indexes[t])
                        if o:
                            identical_pieces.append({'length': j, 'indexes': [i, indexes[t]]})
                    indexes = indexes[:t] + indexes[t + 1:]
                    t -= 1
                t += 1
            j += 1
        for h in range(0, len(identical_pieces)):
            if identical_pieces[h]['indexes'][0] == i:
                i += (identical_pieces[h]['length'] - 1)
        i += 1
    return identical_pieces

def get_normal_alphabet(alphabet):
    normal_alphabet = []
    for i in range(0, q):
        normal_alphabet.append(alphabet.count(i))
    return normal_alphabet

def find_alphabets(m, key_len):
    alphabets = []
    for i in range(0, key_len):
        alphabets.append([])
    j = 0
    for i in m:
        alphabets[j].append(i)
        j += 1
        j = j % key_len
    normal_alphabets = []
    for i in alphabets:
        normal_alphabets.append(get_normal_alphabet(i))
    for i in range(0, len(normal_alphabets)):
        count = len(alphabets[i])
        for j in range(0, q):
            normal_alphabets[i][j] = float(normal_alphabets[i][j]) / count * 100.0
    return normal_alphabets

def find_keys_lengths_from_factors(factors, count):
    keys_lengths = []
    for i in range(0, count):
        index = factors.index(max(factors))
        keys_lengths.append(index + 1)
        factors[index] = 0
    keys_lengths.sort(reverse=True)
    return keys_lengths

def find_sum_factors(identical_pieces):
    factors = []
    for i in identical_pieces:
        index = 0
        o = True
        for j in range(0, len(factors)):
            if factors[j]['length'] == i['length']:
                o = False
                index = j
                break
        if o:
            index = len(factors)
            factors.append({'length': 3, 'distances': [], 'factors': []})
        distances = []
        for j in range(1, len(i['indexes'])):
            distance = i['indexes'][j] - i['indexes'][j - 1]
            distances.append(distance)
        for j in distances:
            factors[index]['distances'].append(j)
            factors[index]['factors'].append([x for x in range(1, j + 1) if j % x == 0])
    sum_factors = []
    for i in range(1, 20):
        sum = 0
        for j in factors:
            for k in j['factors']:
                if i in k:
                    sum += 1
        sum_factors.append(sum)
    return sum_factors

def attack(m, min_word):
    m = get_numbers(m)
    print(m)
    identical_pieces = find_identical_pieces(m, min_word)
    if len(identical_pieces) == 0:
        return -1
    factors = find_sum_factors(identical_pieces)
    keys_lengths = find_keys_lengths_from_factors(factors.copy(), 4)
    print(keys_lengths)
    alphabets = find_alphabets(m, keys_lengths[0])
    shifts = ''
    diagram(rus)
    for i in alphabets:
        diagram(i)
        shifts += get_symbol(find_shift(i))
    return shifts

secret_key = 'шифрование'
f = open('message_rus.txt', encoding="utf-8")
message = f.readline()
f.close()

enc_message = enc(secret_key, message)
print(enc_message)
dec_message = dec(secret_key, enc_message)
print(dec_message)

key = attack(enc_message, 3)
print(key)
