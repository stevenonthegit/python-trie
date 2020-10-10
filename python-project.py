#!/bin/python3
'''
This is an implementation of a Trie.

The idea is to build a data structure that makes it easy to quickly find 
specific terms in a large block of text.
Supposing I have a set of terms, I can put them in the data structure and run 
text through that data structure to see which of those terms are in the text.

A term may be multiple words (sometimes we call those words tokens).  The Trie 
is built using tokens (words) instead of characters, which are also commonly 
used.


The text to be searched is "tokenized", with words separated and punctuation 
cleaned off. Then, the word is checked against the hashed values in the trie
to quickly find matches. Concurrent matches are also selected, 
e.g. if we are searching the text "who let the dogs out", and we look for terms
"dog" and "let the dogs out", both terms are identified and returned as matches.

The result of the trie search is a frequency map, which can be easily
postprocessed or fed into another algorithm.
'''
import re


def read_word(f: object):
    '''
    Generator that lazy returns individual words from a given text file. This would be
    able to handle very large blocks of text without hitting memory constraints.
    Ignores case, formatting, and most punctuation.

    e.g. 'The quick-brown-fox jumped over 20 of a lazy dog's toys -> 
        [the, quick, brown, fox, jumped, over, 20, of, a, lazy, dog's, toys]

    :param file: an opened file buffer
    :type file: _io.TextIOWrapper
    :return: a single word. generator function
    '''
    return (word.lower() for line in f for word in re.findall(r"[\w']+", line))


def get_trie_from_list(terms: list, end: str = '_'):
    '''
    Takes a list of terms, tokenizes them into words and then returns them as a trie.  

    :param words: list of terms that will compose the trie
    :type words: list[str]
    :param end: trie delimiter for the end of a term. Default delimiter is _
    :type end: str
    :return: dict containing the resulting trie
    '''
    # validate the input param. must be of type list
    if not isinstance(terms, list):
        return None

    to_words = re.compile(r"[\w']+")
    root = dict()

    # iterate all the given terms, tokenizing into words and inserting to the trie
    # e.g. "i ate my dog's homework" -> ["i", "ate", "my", "dog's", "homework"]
    for term in terms:
        temp_dict = root
        for word in to_words.findall(term):
            # append new word if needed and drill down
            temp_dict = temp_dict.setdefault(word.lower(), {})
        temp_dict[end] = end

    return root


def add_to_frequency_list(freq: object, term: str):
    '''
        Builds a frequency map in-place. First argument is the dictionary to use.
        :param term: item to add to the dictionary
        :type term: str
    '''
    freq[term] = freq[term]+1 if term in freq else 1


def find_matches(terms_file: str, search_file: str):
    '''
    Takes a file containing a line separated list of terms, and a file 
    containing text to be searched. Uses a Trie to quickly search the text body. 
    Returns results as a frequency map of matches. 

    !Buyer beware! This does not support matching of plural words if the trie 
    term is singular (and vice versa).

    :param terms_file: a text file containing a line separated list of search terms
    :type terms_file: str
    :param search_file: a text file containing a body of text to search within.
    :type search_file: str

    :return: a dict containing resulting matches mapped to the number of their occurrences.
    '''

    _end = '_'  # for use as delimiter for trie

    # open the trie/terms file and read it into a list, then build trie
    terms = [term.strip() for term in open(terms_file, 'r').readlines()]
    root = get_trie_from_list(terms, _end)

    # sort of wonky, but need to keep a list of partial matches.
    # need this so a term within a term can be matched e.g. 'project' and 'project manager',
    # and for partially overlapping matches e.g. 'more corruption' and 'corruption laws'
    possible_matches = []
    results = {}

    # searches input text file for matches
    with open(search_file, 'r') as f:
        for word in read_word(f):

            # helper method will search the possible multi-word matches, and filter out
            # any that don't match. if matches are found, they are returned in a list
            for i in range(len(possible_matches)-1, -1, -1):
                cur = possible_matches[i]
                _trie, _words = cur['trie'], cur['words']

                if _end in _trie:  # we have found a full match (as of the previous word)
                    match = ' '.join(_words)
                    add_to_frequency_list(results, match)

                if word in _trie:  # found current word in a sub-level, and can keep going
                    cur['trie'] = _trie[word]  # drill down!
                    cur['words'].append(word)

                else:  # no more matches.. delete!
                    del possible_matches[i]

            # check root trie for every word we iterate through. If a match is found, 
            # it's added to the list, and processed in the next loop
            if word in root:
                possible_matches.append({'trie': root[word], 'words': [word]})
                
                
    # need a final pass through the list of possibles
    for cur in possible_matches:
        _trie, _words = cur['trie'], cur['words']
        if _end in _trie:
            match = ' '.join(_words)
            add_to_frequency_list(results, match)

    return results


if __name__ == "__main__":
    _out = find_matches('input-terms.txt', 'input-text.txt')
    print(_out)
