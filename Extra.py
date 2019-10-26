

from Util import *
import difflib


def cal_prob_sent(processed_classifier_obj, test_sent, total_files, final_merged_map):
    total_prob = 0.0
    words = test_sent.rstrip().lstrip().split()
    total_prob += math.log(len(processed_classifier_obj.files)/total_files, 2)
    for word in words:
        top = processed_classifier_obj.words_map.get(word, 0) + 1
        bottom = processed_classifier_obj.total_words + len(final_merged_map)
        total_prob += math.log((top/bottom), 2)
    return total_prob


def test():
    t = "The]. rain\\in //Spain` a----f. 'a'a' miller-mac.<br *k &i'm= a''''b [a,h p]"
    print(punctuations_regex(t.split()))


def merge(map1, map2):
    merged = dict(map1)
    for k in map2.keys():
        if k in merged.keys():
            nv = map2.get(k)
            ov = merged.get(k)
            merged[k] = nv + ov
        else:
            merged[k] = map2.get(k)
    return merged


def read_strip_split_map_dir_wo_pun(directory):
    files = get_all_files_dir(directory)
    lines = list()
    for file in files:
        lines.extend(return_lowered_lines(directory+file))
    words = make_words(lines)
    words = remove_punctuations(words)
    return make_map_words(words)


def read_strip_split_map_dir(directory):
    directory_map = dict()
    files = get_all_files_dir(directory)
    for file in files:
        file_map = read_strip_split_map_file(directory+file)
        directory_map.update(file_map)
    return directory_map


def read_strip_split_map_dir_wo_pun_dr1(directory):
    directory_map = dict()
    files = get_all_files_dir(directory)
    for file in files:
        file_map = read_strip_split_map_file_wo_pun(directory+file)
        directory_map = merge1(directory_map, file_map)
    return directory_map


def read_strip_split_map_file(file_path):
    file = open(file_path)
    lines = file.readlines()
    file_map = dict()
    for line in lines:
        splits = line.lower().rstrip().split()
        words = list(filter(None, splits))
        for word in words:
            try:
                file_map[word] += 1
            except KeyError:
                file_map[word] = 1
    return file_map


def read_strip_split_map_file_wo_pun(file_path):
    file = open(file_path)
    lines = file.readlines()
    file_map = dict()
    for line in lines:
        splits = line.lower().rstrip().split()
        words = list(filter(None, splits))
        for word in words:
            word = word.strip(punctuation)
            if len(word) != 0:
                try:
                    file_map[word] += 1
                except KeyError:
                    file_map[word] = 1
    file.close()
    return file_map


def separate_punctuations(words):
    new_words = list()
    for word in words:
        old = (word + '.')[:-1]
        word = word.strip(punctuation)
        if len(word) != 0:
            new_words.append(word)
        if len(word) == 0:
            new_words.extend(find_difference(old, word))
    return new_words


def find_difference(old, new_word):
    parts = [li for li in difflib.ndiff(old, new_word) if li[0] != ' ']
    new_word_list = list()
    for part in parts:
        new_word_list.extend(part.split())
    return new_word_list


def make_lines_from_dir(file_dir):
    files = get_all_files_dir(file_dir)
    all_lines = list()
    for file in files:
        file_path = file_dir+file
        f = open(file_path)
        all_lines.extend(return_lowered_lines(file_path))
        f.close()
    return all_lines


def remove_punctuations(words):
    new_words = list()
    for word in words:
        word = word.strip(punctuation)
        if len(word) != 0:
            new_words.append(word)
    return new_words


def class_predictor_dir_by_num(class1_obj, class2_obj, directory, total_train_files, total_train_words):
    files = get_all_files_dir(directory)
    p_n = 0
    for file in files:
        p_n += class_predictor_file_by_num(class1_obj, class2_obj, directory+file, total_train_files, total_train_words)
    return p_n


def class_predictor_file_by_num(class1_obj, class2_obj, test_file, total_train_files, total_train_words):
    class1_probability = cal_prob_test_file(class1_obj, test_file, total_train_files, total_train_words)
    class2_probability = cal_prob_test_file(class2_obj, test_file, total_train_files, total_train_words)
    if class2_probability > class1_probability:
        return 1
    else:
        return 0
