def read_in_data(file_name):
    """
    This function reads in all the words from the dictionary file into a list, where each elements is a list that stores
    a word in the first index, the frequency of that word in the second index, and its definition if it has one, if it
    doesn't it stores no definition, in the third index.
    :param file_name: the dictionary file
    :return: a list of the words and its characteristics from the file parameter
    :time complexity: O(T) where T is the number of characters in the dictionary file.
    :space complexity: O(T) where T is the number of characters in the dictionary file.
    """
    file = open(file_name)
    lines = file.readlines()
    num_lines = len(lines)
    dictionary_list = []
    for i in range(0, num_lines, 4):
        word_list = []
        word_line = lines[i].strip().split(": ")
        word = word_line[1]
        word_list.append(word)
        frequency_line = lines[i+1].strip().split(": ")
        frequency = int(frequency_line[1])
        word_list.append(frequency)
        definition_line = lines[i+2].strip().split(": ", 1)
        if len(definition_line) == 1:
            definition = "No definition"
        else:
            definition = definition_line[1]
        word_list.append(definition)
        dictionary_list.append(word_list)
    file.close()
    return dictionary_list


def construct_trie(dictionary):
    """
    This function initialises a root node. Then for each word in the dictionary, for each character in the word, if a
    node containing that character exists we move to it, otherwise we create a node and set the element corresponding to
    the index number of that character in the current node to point to the node we just created. Each time we are at a
    node, we increment the word count in index 28 by one. If the node we are currently was just created in the previous
    iteration, we set the maximum frequency and the word index location to the word we are inserting. If the word’s
    frequency we are inserting is larger than the current maximum frequency word’s, then we change the values in the
    node accordingly. If the two words have the same frequency we call the character_check function.
    :param dictionary: the dictionary file
    :return: a trie corresponding to the words in the dictionary file
    :time complexity: O(T) where T is the number of characters in the dictionary file.
    :space complexity: O(T) where T is the number of characters in the dictionary file.
    """
    root_node = [None if i < 27 else 0 if i == 27 else -1 for i in range(30)]
    num_words = len(dictionary)
    for x in range(num_words):
        new_word = dictionary[x][0]
        word_len = len(new_word)
        current_node = root_node
        similar = False
        start_similarity = 0
        is_biggest = False
        old_max_index = 0
        for y in range(word_len + 1):
            current_node[27] += 1
            word_index = x
            word_frequency = dictionary[word_index][1]
            max_frequency = current_node[28]
            if word_frequency > max_frequency:
                current_node[28] = word_frequency
                current_node[29] = word_index
            elif word_frequency == max_frequency and not is_biggest:
                results = character_check(current_node, dictionary, new_word, y, similar, old_max_index,
                                          start_similarity, is_biggest)
                similar = results[0]
                start_similarity = results[1]
                is_biggest = results[2]
            if y == word_len:
                current_node[26] = "$"
            else:
                old_max_index = current_node[29]
                character = new_word[y]
                character_num = ord(character) - 97
                if current_node[character_num] is None:
                    current_node[character_num] = [None if i < 27 else 0 if i == 27 else -1 for i in range(30)]
                current_node = current_node[character_num]
        if similar:
            update_max_word(root_node, dictionary, x, start_similarity)
    return root_node


def character_check(node, words_list, fresh_word, current_iter, is_similar, old_max_loc, start_similarity, the_biggest):
    """
    Since if words have the same frequency, and the auto complete suggestion should be the alphabetically
    smaller word, if the frequency is the same then we compare the two words character corresponding to the letter of
    the node in the trie we are currently at. Since we know exactly where the two letters are and strings are
    array-based, and we are only comparing one character for each node, this takes O(1) time. Boundary cases for this
    method include accounting for when the two strings don’t have the same size, characters not have the same letter
    before reaching the end of one of the strings, and when we are at the root node. We do not need to consider if the
    word we are inserting is established to be alphabetically smaller than the first word it encounters to have the
    same frequency, and whether if it is alphabetically smaller than the second word it encounters, different from the
    first word, where it has the same frequency, because the second word is always alphabetically larger than the first
    word by the properties of a trie.
    :param node: current node we are at
    :param words_list: the dictionary word list
    :param fresh_word: the word we are inserting
    :param current_iter: the iteration of the characters of the word we are inserting
    :param is_similar: whether or not the words started sharing frequency similarity
    :param old_max_loc: the index of the max word of the previous node
    :param start_similarity: the position in the word we are inserting started sharing frequency similarity
    :param the_biggest: if the word is alphabetically smaller than the current word stored in the node
    :return: a tuple of containing the variables, is_similar, start_similarity and the_biggest.
    :time complexity: O(1) constant time
    :space complexity: O(1) constant space
    """
    current_max_word_index = node[29]
    fresh_word_len = len(fresh_word)
    if is_similar and old_max_loc != current_max_word_index:
        is_similar = False
    current_max_word = words_list[current_max_word_index][0]
    current_max_word_len = len(current_max_word)
    position = current_iter
    if position >= 1:
        position -= 1
    if position + 1 > len(current_max_word):
        is_similar = False
    elif current_max_word[position] < fresh_word[position]:
        is_similar = False
    elif current_max_word[position] == fresh_word[position]:
        if not is_similar:
            is_similar = True
            start_similarity = current_iter
        if position + 1 < current_max_word_len and position + 1 < fresh_word_len:
            if current_max_word[position + 1] < fresh_word[position + 1]:
                is_similar = False
            elif current_max_word[position + 1] > fresh_word[position + 1]:
                the_biggest = True
    else:
        if not is_similar:
            is_similar = True
            start_similarity = current_iter
        the_biggest = True
    result_tuple = (is_similar, start_similarity, the_biggest)
    return result_tuple


def update_max_word(root, word_list, new_max_word_index, start_update_index):
    """
    To update the location of the word in the node to correspond to the alphabetically smaller word, we keep track of
    when the frequency first started to be the same. Then after the word has finished traversing the trie, if the new
    word is alphabetically smaller than a word that has the same frequency to it, we traverse the same path the word we
    are inserting down the trie and changing all the entries for the highest frequency word index to correspond to the
    index location of the new word, starting from the node that corresponds to the node where the frequency first
    started to be the same. The construction of the trie has O(T) time and space complexity, where T is the number of
    characters in the dictionary file.
    :param root: root node
    :param word_list: dictionary word list
    :param new_max_word_index: index in the dictionary word list that corresponds to the word we are inserting
    :param start_update_index: the iteration number where we need to start updating the node's max freq index
    :return: none
    :time complexity: O(N) where N is the number of characters in the word we are inserting
    :space complexity: O(1) constant space
    """
    current = root
    new_max_word = word_list[new_max_word_index][0]
    new_max_word_len = len(new_max_word)
    for a in range(new_max_word_len + 1):
        if a >= start_update_index:
            current[29] = new_max_word_index
        if a < new_max_word_len:
            next_char = new_max_word[a]
            next_char_num = ord(next_char) - 97
            current = current[next_char_num]


def search_trie(prefix, trie):
    """
    For each character in the prefix given, if a node corresponding to that character exists we move to it. If the node
    we are currently on doesn’t have a child node that corresponds to the next character of the prefix, then the
    dictionary doesn’t contain a word with the given prefix. Once we are at the node that corresponds to the last
    letter of the given prefix, we return the word count and the max frequency word index in a tuple.
    :param prefix: the user's given prefix
    :param trie: the constructed trie corresponding to the words in the dictionary file
    :return: a tuple of max_freq_word_index
    :time complexity: O(M + N) where M is the length of the prefix entered by the user and N is the total number of
    characters in the word with the highest frequency and its definition.
    :space complexity: O(M + N) where M is the length of the prefix entered by the user and N is the total number of
    characters in the word with the highest frequency and its definition.
    """
    current_node = trie
    for char in prefix:
        char_num = ord(char) - 97
        if current_node[char_num] is None:
            return False
        else:
            current_node = current_node[char_num]
    max_freq_word_index = current_node[29]
    num_words_with_prefix = current_node[27]
    result = (max_freq_word_index, num_words_with_prefix)
    return result


def main_function(dictionary_list, trie):
    """
    This function takes input from the user to be the prefix given. If the user inputs '***' then we end the program.
    Otherwise we call the search_trie function with the user's given prefix and the constructed trie as parameters.
    :param dictionary_list: dictionary word list
    :param trie: the constructed trie corresponding to the words in the dictionary file
    :return: none
    :time complexity: O(M + N) where M is the length of the prefix entered by the user and N is the total number of
    characters in the word with the highest frequency and its definition.
    :space complexity: O(M + N) where M is the length of the prefix entered by the user and N is the total number of
    characters in the word with the highest frequency and its definition.
    """
    user_prefix = ""
    while user_prefix != "***":
        user_prefix = input("Enter a prefix: ")
        if user_prefix != "***":
            found = search_trie(user_prefix, trie)
            if not found:
                print("""There is no word in the dictionary that has "{}" as a prefix.\n""".format(user_prefix))
            else:
                word_location = found[0]
                num_words = found[1]
                suggested_word = dictionary_list[word_location][0]
                word_definition = dictionary_list[word_location][2]
                print("Auto-complete suggestion: {}".format(suggested_word))
                print("Definition: {}".format(word_definition))
                print("""There are {} words in the dictionary that have "{}" as a prefix.\n"""
                      .format(num_words, user_prefix))
        else:
            print("Bye Alice!")


if __name__ == '__main__':
    dict_list = read_in_data("dictionary.txt")
    dict_trie = construct_trie(dict_list)
    main_function(dict_list, dict_trie)
