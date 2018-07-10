from flask import Flask, redirect, render_template,request, url_for

from random import shuffle

from helpers import (add_on, d_lets, shown_word, word_keys, 
                    word_dict, rando_word_pick, get_current_word)



app = Flask(__name__)

app.config['DEBUG'] = True


@app.route("/")
def here_we_go():
    '''start first game from scratch'''
    return render_template('intro.html')

@app.route("/game", methods=['POST', 'GET'])
def start_from_rando():
    ''' starts game with random word '''
   
   # just shuffling the words and picking the first one
    shuffle(word_keys)
    all_words = ''.join(word_keys)
    #TODO encrypt index_cw
    index_cw = "0"
    guesses = '1'
   
    return redirect(url_for('.in_game', all_words=all_words, index_cw=index_cw, guesses_made=guesses))


@app.route("/<all_words>/<index_cw>/<guesses_made>", methods=['POST', 'GET'])
def in_game(all_words, index_cw, guesses_made):
    ''' main game play, built with params '''
    
    wordkey = all_words[int(index_cw)]
    word = word_dict[wordkey]
    guesses = guesses_made #decoded 
    whole_word_guessed = False
    for guess in guesses_made:
        if guess == "6":
            whole_word_guessed = True
    print("&&&&&&&&&&&&&&&&&&")
    print(guesses)
    display_word = shown_word(word, guesses)
    
    mistakes = 0
    
    if "_" not in display_word:
        print("YOU WIN")
        
        return render_template('congrats.html', remaining=all_words, word_completed=index_cw)
    
    if request.method == 'POST':
        
        let_guess = request.form['letter_guess']
        print(let_guess)
        if let_guess.lower() not in word.lower():
            mistakes += 1
        print(str(mistakes))
        guesses_made = let_guess + guesses_made #encode let_guess here
        print(guesses_made)
            
        return redirect(url_for('.in_game', 
                                all_words=all_words, 
                                index_cw=index_cw, 
                                guesses_made=guesses_made))
    return render_template('game-page.html', 
                            all_words=all_words, 
                            index_cw=index_cw, 
                            guesses_made=guesses, 
                            word=display_word, 
                            word_guessed=whole_word_guessed)

@app.route("/<all_words>/<index_cw>/<guesses_made>/<t>", methods=['POST', 'GET'])                    
def word_guess(all_words, index_cw, guesses_made, t):
    if request.method == 'POST':
        word_guess = request.form['word_guess']
        #if word_guess.lower() == word_dict[index_cw].lower():
        if word_guess.lower() == get_current_word(all_words, index_cw):
            print("you won")
            return render_template('congrats.html', remaining=all_words, word_completed=index_cw)
        whole_word_guessed = True
        guesses = "6" + guesses_made
        wordkey = all_words[int(index_cw)]
        w = word_dict[wordkey]
        display_word = shown_word(w, guesses)
        return render_template('game-page.html', 
                                all_words=all_words, 
                                index_cw=index_cw, 
                                guesses_made=guesses, 
                                word=display_word, 
                                word_guessed=whole_word_guessed)

@app.route("/new_game/<all_words>/<word_completed>", methods=['POST', 'GET'])
def next_game(all_words, word_completed):
    ''' starts new game from words left '''
    # if all_words[0] in d_lets:
    #     print("GAME is totally complete!!")
    #     return render_template('congrats.html', remaining=None)
    # index_cw = rando_word_pick()
    #adds dummy value to make up for removed word key
    # print("$$$$$$$$$$$$$$$$$")
    # print(len(all_words))
    # how_many_to_add = 9 - (len(all_words))
    # foolin = ''
    # for i in range(how_many_to_add):
    #     foolin += add_on()
    #     i += 1
    # print(len(foolin))
    # word_keys.remove(index_cw)
    # words_keys_for_display = word_keys[:]
    # words_keys_for_display.append(str(foolin))
   
    # all_words = ''.join(words_keys_for_display)
    index = int(word_completed) + 1
    index_cw = str(index)
    guesses = '1'
   
    return redirect(url_for('.in_game', 
                            all_words=all_words, 
                            index_cw=index_cw, 
                            guesses_made=guesses))

@app.route("/<all_words>/<index_cw>/<guesses_made>/<s>/<q>", methods=['GET', 'POST'])
def undo(all_words, index_cw, guesses_made, s, q):
    
    print("JJLKJLJLJLK")
    if len(guesses_made) <= 1:
        while int(index_cw) > 0:
            prev_index = str(int(index_cw) - 1)
            old_word = get_current_word(all_words, prev_index)
            display_word = shown_word(old_word, "1")
            whole_word_guessed = False
            return render_template('game-page.html', 
                                    all_words=all_words, 
                                    index_cw=prev_index, 
                                    guesses_made=guesses_made, 
                                    word=display_word, 
                                    word_guessed=whole_word_guessed)
        if int(index_cw) == 0:
            return render_template('/intro.html')
    #prev_all_words = all_words[1:]
    prev_guesses_made = guesses_made[1:]

    wordkey = all_words[int(index_cw)]
    w = word_dict[wordkey]
    
    display_word = shown_word(w, prev_guesses_made)

    whole_word_guessed = False
    for guess in guesses_made:
        if guess == '6':
            whole_word_guessed=True

    return render_template('game-page.html', 
                                all_words=all_words, 
                                index_cw=index_cw, 
                                guesses_made=prev_guesses_made, 
                                word=display_word, 
                                word_guessed=whole_word_guessed)



if __name__ == "__main__":
    app.run()