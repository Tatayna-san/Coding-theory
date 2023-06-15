import math
from heapq import heappop, heappush
from collections import defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(text):
    frequency_table = defaultdict(int)
    for char in text:
        frequency_table[char] += 1
    return frequency_table

def build_huffman_tree(frequency_table):
    priority_queue = []
    for char, freq in frequency_table.items():
        node = HuffmanNode(char, freq)
        heappush(priority_queue, node)
    while len(priority_queue) > 1:
        left_node = heappop(priority_queue)
        right_node = heappop(priority_queue)
        parent_freq = left_node.freq + right_node.freq
        parent_node = HuffmanNode(None, parent_freq)
        parent_node.left = left_node
        parent_node.right = right_node
        heappush(priority_queue, parent_node)
    return priority_queue[0]

def build_huffman_codes(huffman_tree):
    huffman_codes = {}
    def traverse_tree(node, current_code):
        if node.char is not None:
            huffman_codes[node.char] = current_code
            return
        traverse_tree(node.left, current_code + '0')
        traverse_tree(node.right, current_code + '1')
    traverse_tree(huffman_tree, '')
    return huffman_codes

def compress_text(text, huffman_codes):
    compressed_text = ''
    for char in text:
        compressed_text += huffman_codes[char]
    return compressed_text

def huffman_compress(text):
    frequency_table = build_frequency_table(text)
    huffman_tree = build_huffman_tree(frequency_table)
    huffman_codes = build_huffman_codes(huffman_tree)
    compressed_text = compress_text(text, huffman_codes)
    return compressed_text

def calculate_entropy(frequency_table, text_length):
    entropy = 0.0
    for freq in frequency_table.values():
        probability = freq / text_length
        entropy -= probability * math.log2(probability)
    return entropy

def main():
    text = input("Введите строку для сжатия: ")
    compressed_text = huffman_compress(text)
    print("Сжатая строка (в битах):", compressed_text)
    print("Длина сжатой строки (в битах):", len(compressed_text))
    frequency_table = build_frequency_table(text)
    entropy = calculate_entropy(frequency_table, len(text))
    print("Значение энтропии (в битах на символ):", entropy)
    compression_ratio = entropy / len(compressed_text)
    print("Отношение энтропии к длине сжатой строки:", compression_ratio)