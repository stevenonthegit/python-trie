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


def read_word(f: object) -> str:
    '''
    Creates a generator that lazy returns individual words from a given text file. 
    This should handle very large blocks of text without hitting memory constraints.
    Strips case, formatting, and most punctuation.
    e.g. 'The quick-brown-fox jumped over 20 of a lazy dog's toys -> 
        [the, quick, brown, fox, jumped, over, 20, of, a, lazy, dog's, toys]

    :param file: _io.TextIOWrapper: an opened file buffer
    :return: the next word. generator function
    '''
    return (word.lower() for line in f for word in re.findall(r"[\w']+", line))
    
    ###! it turns out the regex generator is a HUGE bottleneck on speed. Need to optimize this.
    #! Two alternatives:
    #! 1) use open() to read a line by line buffer. Keeps formatting and punctuation if needed.
    '''
    def read_word(f: object):
        for line in f:
            yield line.lower()
    '''
    #! 2) read the file in buffered chunks, and yield one word at a time. 
    #!  Won't choke on large, single-line files.
    '''
    def read_word(f: object, buffersize=2048):
        buffer = ''
        for chunk in iter(lambda: f.read(buffersize), ''):
            words = re.split("\W+", buffer + chunk)
            buffer = words.pop()  # pop off partial words at the end of a chunk
            yield from (w.lower() for w in words if w)
        
        if buffer: # yield any remaining words after the file buffer is emptied
            yield buffer.lower()            
    '''


def get_trie_from_list(terms: list, end: str = '_') -> dict:
    '''
    Receives a list of terms, tokenizes them into words, then returns them as a trie.  

    :param words: list[str]: list of terms that will compose the trie
    :param end: str: trie delimiter for the end of a term. Default delimiter is _
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
            # append word if not already present, then drill down
            temp_dict = temp_dict.setdefault(word.lower(), {})
        temp_dict[end] = end

    return root


def add_frequency_map(d: object, term: str, count: int = 1):
    '''
    Builds a frequency map in-place. First argument is the dictionary to use.
    
    :param term: an item to increment in the map
    :type term: str
    '''
    d[term] = d[term]+count if term in d else count


def find_matches(terms_file: str, search_file: str) -> dict:
    '''
    Takes a file containing a line separated list of terms, and a file 
    containing text to be searched. Uses a Trie to quickly search the text body. 
    Returns results as a frequency map of matches. 
    #!Beware This does not support the matching of plural words if the search term is singular (and vice versa).

    :param terms_file: str: a text file containing a line separated list of search terms
    :param search_file: str: a text file containing a body of text to search within.
    :return: a frequency map of all the matches found in the file. 
    '''

    _end = '_'  # trie delimiter

    # open the term file and read into a list, then build trie
    terms = [term.strip() for term in open(terms_file, 'r').readlines()]
    root = get_trie_from_list(terms, _end)

    # keep a queue of partial matches. This lets us handle two situations:
    #  - Term within a term e.g. 'project' and 'project manager',
    #  - Partially overlapping matches e.g. 'more corruption' and 'corruption laws'
    # 
    # the structure of this object is a list of objects: [{ trie: _, words: _}]
    # where 'trie' is a subset of the parent trie, and 'words' is a partial match sequence
    possible_matches = []

    results = {}

    # search text file for matches
    with open(search_file, 'r') as f:
        for word in read_word(f):
            
            # search for possible multi-word matches, and filter out sequences that don't match.
            for i in range(len(possible_matches)):
                cur = possible_matches.pop(0)
                _trie, _words = cur['trie'], cur['words']

                if _end in _trie:  # found a full match (in previous pass)
                    match = ' '.join(_words)
                    add_frequency_map(results, match)

                if word in _trie:  # found partial word in a sub-level, and can keep matching
                    cur['trie'] = _trie[word]  # drill down!
                    cur['words'].append(word)

                    possible_matches.append(cur) # push it back onto our queue


            # check root trie for every word we iterate through. if a match is found, 
            # it's added to the list, then verified and counted in the next pass.
            if word in root:
                possible_matches.append({'trie': root[word], 'words': [word]})
            
                
    # need a final pass through the list of possibles
    for cur in possible_matches:
        _trie, _words = cur['trie'], cur['words']
        if _end in _trie:
            match = ' '.join(_words)
            add_frequency_map(results, match)

    return results


if __name__ == "__main__":

    out = find_matches('input_data/search_terms.txt', 'input_data/sample_text.txt')
    print('out:', out)