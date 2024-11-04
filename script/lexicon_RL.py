from collections import Counter
import re
import heuristics


def read_file(fine_name):
    with open(fine_name, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def save_to_file(file_name, lexicon):
    with open(file_name, 'w', encoding='utf-8') as f:
        for item in lexicon:
            f.write("%s\n" % item)

def get_words_list(text):
    # separators = r"[^а-яА-Я0-9'-]+"
    separators = r"[^а-яА-Я'-]+"
    text_split = re.split(separators, text.lower())
    return text_split


# strip off leading dashes, ending dashes, and single quotes
def strip_off_dashes(text: list):
    result_text = list(text)
    for i, token in enumerate(text):
        if len(token) == 0:
            result_text.remove(token)
            continue
        if token[0] == '-':
            idx = result_text.index(token)
            result_text[idx] = token[1:]
            continue
        if len(token) > 1 and token[len(token) - 1] == '-':
            idx = result_text.index(token)
            result_text[idx] = token[:-1]
            continue
        if token[0] == "'":
            result_text.remove(token)
            continue
    result_text.remove("")
    result_text.remove("-")
    return result_text


# exclude short words (1-4 chars) with rare occurrence (1-2 times)
# and move short words (1-3 chars) with high occ (>3 times) to a separate list
def exclude_short_rare_words(text: list, word_counter: dict):
    short_words = []
    result_text = list(text)
    for word in text:
        if len(word) < 5 and word_counter[word] < 3:
            result_text.remove(word)
        if len(word) < 4 and word_counter[word] >= 3:
            short_words.append(word)
            result_text.remove(word)
    return result_text, short_words


# pl = prefix_length
def create_groups_with_common_prefix(sorted_text: list):
    prefix_groups = {}
    short_groups = []  # list for words without common prefixes
    group_counter = 0
    group = []
    key_word = "mock_word"
    pl = 3
    for i, word in enumerate(sorted_text):
        if group_counter == 0:
            key_word = word
            if len(key_word) > 5:
                pl = len(key_word) - 3
            else:
                pl = 3
            group.append(key_word)
            group_counter += 1
            continue
        if key_word[:pl] == word[:pl]:
            group.append(word)
            group_counter += 1
        else:
            if group_counter == 1:
                short_groups.append(key_word)
            else:
                prefix_groups[key_word] = group
            group = []
            group_counter = 0
    return prefix_groups, short_groups


def create_lexicon(in_file_path, out_file_path):

    text = read_file(in_file_path)

    data = text.split()
    print("dataset len:", len(data))

    words_list = get_words_list(text)
    print("alphabetic words len:", len(words_list))

    word_counter = Counter(words_list)
    print("distinct words len:", len(word_counter.keys()))
    print("100 most common", word_counter.most_common(100))

    word_counter_list = list(word_counter.keys())
    word_counter_list.sort()

    word_list = strip_off_dashes(word_counter_list)
    word_list, short_words = exclude_short_rare_words(word_list, word_counter)

    word_list.sort()

    print("len after cleaning", len(word_list))

    groups, lonely_words = create_groups_with_common_prefix(word_list)

    print("long_groups_counter", len(groups))
    print("short_groups_counter", len(lonely_words))

    lexicon = heuristics.apply_heuristics(groups)
    lexicon = heuristics.predefined_lists(short_words, lexicon)
    lexicon = heuristics.predefined_lists(lonely_words, lexicon)

    save_to_file(out_file_path, lexicon)
    print("lexicon length", len(lexicon))
