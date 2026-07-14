import numpy as np
import json
import re
from collections import Counter

def load_weighted_alphabet():
    weighted_letters = {}
    with open('./weighted_alphabet.json', encoding="utf-8") as weighted_alphabet_file:
        weighted_letters = weighted_alphabet_file.read()
    return json.loads(weighted_letters)

def randomizer_letter_array(word_length=0):
    alphabets = list("abcdefghijklmnopqrstuvwxyz")
    np_alphabet = np.array(alphabets, dtype="|U1")
    np_letters = np.random.choice(np_alphabet, [1, word_length])
    return np_letters[0]

def load_dictionary():
    dictionary_content = ""
    with open('./macos_words_web2.txt', encoding="utf-8") as dictionary_file:
        dictionary_content = dictionary_file.read()
    dictionary_content = dictionary_content.lower()
    return dictionary_content.split('\n')


def match_words_list(letters, words_list):
    #print(letters)
    unique_letters, counted = np.unique(letters, return_counts=True)
    unique_letters_dict = {}
    for i in range(len(unique_letters)):
        unique_letters_dict[unique_letters[i]] = counted[i]
    matching_words_list = []
    for word in words_list:
        word_matches = True
        for letter in word:
            if letter not in letters:
                word_matches = False
            elif word.count(letter) > unique_letters_dict[letter]:
                word_matches = False
        if word != "" and len(word) > 1 and word_matches:
            matching_words_list.append(word)
            #print(word + " matches")
    return matching_words_list

def prioritize_matching_words(matching_words_list, weighted_alphabet):
    prioritzed_matching_words = {}
    for word in matching_words_list:
        letter_value = 0
        for letter in word:
            letter_value = letter_value + int(weighted_alphabet[letter])
        prioritzed_matching_words[word] = letter_value
    return dict(sorted(prioritzed_matching_words.items(), key=lambda item: item[1], reverse=True))

def test_regex(pattern_string, word):
    pattern = re.compile(r'{}'.format(pattern_string))
    matches = pattern.finditer(word)
    matched = False
    for match_number, match in enumerate(matches, start=1):
        matched = True
        #print(str(match_number) + " found at " + str(match.start()) + "-" + str(match.end()) + ": group=" + str(match.group()) + ", word=" + word)
    #for group_number, group in enumerate(match.groups(), start=1):
    #    print("Groups: " + str(group_number) + " found at " + str(match.start(group_number)) + "-" + str(match.end(group_number)) + ": group=" + str(group))
    return matched

def regex_match_word_list(pattern_string, matching_words_list):
    filtered_word_list = []
    for word in matching_words_list:
        matched = test_regex(pattern_string, word)
        #print("Pattern: " + pattern_string + ", Word: " + word + ", Matched: " + str(matched))
        if matched and word not in filtered_word_list:
            filtered_word_list.append(word)
    return filtered_word_list

def word_score(word):
    score = 0
    weighted_alphabet = load_weighted_alphabet()
    for letter in word:
        score = score + weighted_alphabet[letter]
    return score

def multiplier_word_score(word, mask):
    score = 0
    weighted_alphabet = load_weighted_alphabet()
    mask_array = mask.split(' ')
    word_multiplier = 1;
    letter_multiplier = 1;
    #print(word + " " + str(mask))
    for i in range(len(word)):
        letter_multiplier = 1;
        match mask_array[i]:
            case '2L':
                letter_multiplier = 2
            case '3L':
                letter_multiplier = 3
            case '2W':
                word_multiplier = 2
            case '3W':
                word_multiplier = 3
            #case _:
            #    print("No match found")
        score = score + letter_multiplier * weighted_alphabet[word[i]];
        print(word[i] + " multiplier = " + str(letter_multiplier))
    score = score * word_multiplier
    print(word + " word multiplier = " + str(word_multiplier))
    return score

def make_it_so_number_one(letters, anchor_letters, pattern_string, words_list):
    all_the_letters = np.concatenate([letters, anchor_letters])
    print("All the letters:", all_the_letters)
    matching_words_list = match_words_list(all_the_letters, words_list)
    print("Matching words:", matching_words_list)
    print("Pattern string:", pattern_string)
    filtered_matching_words = regex_match_word_list(pattern_string, matching_words_list)
    print("Filtered matching words:", filtered_matching_words)
    return filtered_matching_words

def create_pattern_string(letters, anchor_letters, max_length):
    max_word_length = int(max_length)
    pattern_string = r"^"
    letters_list = str(letters.tolist())
    wildcard_pattern = '[a-z]'
    try: 
        for i in range(max_word_length):
            pattern_string_updated = False
            if i < len(anchor_letters):
                if anchor_letters[i] != "":
                    pattern_string += "[" + anchor_letters[i] + "]"
                    pattern_string_updated = True
            
            if not pattern_string_updated:
                if "*" in letters:
                    pattern_string += r"" + wildcard_pattern
                else:
                    pattern_string += r"" + letters_list
                
        pattern_string += r"\Z"
    except Exception as create_pattern_string_exception:
        print("ERROR: create_pattern_string: ", create_pattern_string_exception)
        
    #print("Pattern string:", pattern_string)
    return pattern_string

def filter_for_letters(words, letters):
    filtered_words = []

    max_counts_dict = {}
    unique_letters_key_list = []
    for key in Counter(letters).keys():
        unique_letters_key_list.append(str(key))
    unique_letters_value_list = []
    for value in Counter(letters).values():
        unique_letters_value_list.append(value)
    for k in range(0,len(unique_letters_key_list)):
        max_counts_dict[unique_letters_key_list[k]] = unique_letters_value_list[k]
    print(max_counts_dict)

    for word in words:
        word_letters_list = []
        for key in Counter(word).keys():
            word_letters_list.append(str(key))
        word_letters_count = []
        for value in Counter(word).values():
            word_letters_count.append(value)
        for j in range(len(word_letters_list)):
            if word_letters_list[j] in max_counts_dict.keys():
                if word_letters_count[j] <= max_counts_dict[word_letters_list[j]]:
                    if word not in filtered_words:
                        filtered_words.append(word)

    return filtered_words

def engage(letters, anchor_letters, max_length):
    print("engaging...")
    print("Letters: ", letters)
    print("Anchor letters:", anchor_letters)
    print("Max Length:", max_length)
    pattern_string = create_pattern_string(letters,anchor_letters,max_length)
    print("Pattern string: ", pattern_string)
    words_list = load_dictionary()
    test_words = regex_match_word_list(pattern_string, words_list)
    print("Test words length:", len(test_words))
    filtered_words = filter_for_letters(test_words,letters)
    print("filtered words length:", len(filtered_words))
    return filtered_words

if __name__ == '__main__':
    letters = randomizer_letter_array(7)
    #letters = np.array(['a','m','l','*','o','i'])
    anchor_letters = np.array(['a','','','','','',''])
    
    max_length = 4
    filtered_words = engage(letters,anchor_letters, max_length)
    print("filtered words length:", len(filtered_words))
