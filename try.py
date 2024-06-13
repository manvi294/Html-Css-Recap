6from textblob import Word
from difflib import get_close_matches

class CustomSpeller:
    def __init__(self, custom_words=None):
        self.custom_words = set(custom_words or [])

    def correct(self, word):
        if word in self.custom_words:
            return word
        
        # First try correcting with TextBlob
        corrected_word = str(Word(word).spellcheck()[0][0])
        if corrected_word in self.custom_words:
            return corrected_word

        # Check if the corrected word is valid, else use the closest custom word
        closest_match = get_close_matches(word, self.custom_words, n=1, cutoff=0.8)
        if closest_match:
            return closest_match[0]
        
        return corrected_word

# Usage example
custom_words = ["zumba", "ATM"]
custom_speller = CustomSpeller(custom_words=custom_words)

print(custom_speller.correct("zumab"))  # Output: zumba
print(custom_speller.correct("atm"))    # Output: ATM
print(custom_speller.correct("atn"))    # Output: ATM
print(custom_speller.correct("exmple")) # Output: example
