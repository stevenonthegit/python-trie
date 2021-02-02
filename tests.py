import unittest

from trie_search import read_word, get_trie_from_list, add_frequency_map, find_matches
class TestHelperMethods(unittest.TestCase):

    def test_frequency_map(self):
        '''tests the add_frequency_map function. 
        Verify that when an item is added to the map, its count is adjusted correctly.'''
        mylist = {}
        #empty list
        self.assertEqual(mylist.get('a'), None)

        #single add 
        add_frequency_map(mylist,'a')
        add_frequency_map(mylist,'a')
        add_frequency_map(mylist,'b')
        self.assertEqual(mylist.get('a'), 2)
        self.assertEqual(mylist.get('b'), 1)
        
        #multi add
        add_frequency_map(mylist,'a',2)
        add_frequency_map(mylist,'b',9)
        self.assertEqual(mylist.get('a'), 4)
        self.assertEqual(mylist.get('b'), 10)

        #subtract
        add_frequency_map(mylist,'a',-1)
        self.assertEqual(mylist.get('a'), 3)

    def get_trie_from_list(self):
        '''tests the add_frequency_map function. 
        Verify that a trie is correctly built when different types of lists are received.'''
        pass


    def test_read_word(self):
        #todo: test case for very large files (load test performance)
        #todo: test case for empty files
        #todo: test case for non-text files
        pass

    def test_find_matches(self):
        #todo: test case for very large input with large number of matches (performance)
        #todo: test case for input with no matches (empty case)
        #todo: test case for an input where all words are match-able
        #todo: test case where all words are the same (weird edge case)
        pass    



if __name__ == '__main__':
    unittest.main()
