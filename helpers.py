from random import choice, shuffle

word_dict = {'w':'FLUFFY', 
            'q':'BUNNY', 
            'u':'LETTUCE', 
            'v':'CARROT', 
            'a':'BURROW', 
            'n':'FLOPPY', 
            'd':'LITTER', 
            'l':'PELLETS', 
            'p':'RABBIT'}

word_keys = list(word_dict.keys()) # list needes for dict object starting in py3

d_lets = ['s', 't', 'r', 'e', 'z', 'b', 'j', 'v']

def rando_word_pick():
    current_word = choice(word_keys)
    return current_word

def add_on():
    dummy_lets = d_lets[:]
    shuffle(dummy_lets)
    return dummy_lets[0]

def shown_word(word, guesses):
    word_shown = ""
    for let in word.lower():
        if let in guesses:
            word_shown += let
        else:
            word_shown += '_ '
    return word_shown
    
def get_current_word(words, index):
    wordkey = words[int(index)]
    return word_dict[wordkey].lower()

def quick_encode(letters):
    '''quick rot9 cipher '''
    alpha = 'abcdefghijklmnopqrstuvwxyz' * 2
    coded_string = ""
    for letter in letters:
        letter = letter.lower()
        if letter.isalpha():
            old_index = alpha.index(letter)
            coded_string += alpha[old_index+9]
        else:
            coded_string += letter
    return coded_string
    
def quick_decode(letters):
    alpha = 'abcdefghijklmnopqrstuvwxyz' * 2
    decoded_string = ""
    for letter in letters:
        letter = letter.lower()
        if letter.isalpha():
            old_index = alpha.index(letter)
            decoded_string += alpha[old_index-9]
        else:
            decoded_string += letter
    return decoded_string
    

    




