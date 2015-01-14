from bloom import lookup_word
import unittest


class TestBloom(unittest.TestCase):
    def test_positives(self):
        words = 'the quick brown fox jumped over the lazy dog'
        for word in words.split():
            self.assertTrue(lookup_word(word), 'false on %s' % word)
    
    def test_negatives(self):
        words = 'werawerfe abwefaweoub gsfkljg asdxcv adsfwere ghktshep asdhrwrpog'
        for word in words.split():
            self.assertFalse(lookup_word(word), 'true on %s' % word)
        

if __name__ == '__main__':
    unittest.main()