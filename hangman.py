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
    
    word = get_current_word(all_words, index_cw)
   
    guesses = guesses_made #TODO decode here 
    whole_word_guessed = False
    for guess in guesses_made:
        if guess == "6":
            whole_word_guessed = True

    display_word = shown_word(word, guesses)
    
    mistakes = []
    
    if "_" not in display_word:
        print("YOU WIN")
        remaining = 8 - int(index_cw) 
        
        return render_template('congrats.html', remaining=remaining,
                                all_words=all_words,
                                word_completed=index_cw,
                                guesses_made=guesses_made)
    
    print(guesses_made)
    for guess in guesses_made:
        if guess.lower() not in word.lower():
            mistakes.append(guess.lower())
    # reminder that mistakes will always contain 1
    mistake_total = len(mistakes) - 1
    print(mistake_total)
    if mistake_total == 9:
        return render_template('loser.html')

    if request.method == 'POST':
        
        let_guess = request.form['letter_guess']
        print(let_guess)
       
        guesses_made = let_guess + guesses_made #encode let_guess here
        
        
        return redirect(url_for('.in_game', 
                                all_words=all_words, 
                                index_cw=index_cw, 
                                guesses_made=guesses_made))
    print("!!!!!!!!!!!!!!!!")

    print(mistakes)
    return render_template('game-page.html', 
                                all_words=all_words, 
                                index_cw=index_cw, 
                                guesses_made=guesses, 
                                word=display_word, 
                                word_guessed=whole_word_guessed,
                                mistake_total=mistake_total)

@app.route("/<all_words>/<index_cw>/<guesses_made>/<t>", methods=['POST', 'GET'])                    
def word_guess(all_words, index_cw, guesses_made, t):
    if request.method == 'POST':
        word_guess = request.form['word_guess']
        if word_guess.lower() == get_current_word(all_words, index_cw):
            print("you won")
            remaining = 8 - int(index_cw)
            return render_template('congrats.html', remaining=remaining, 
                                                    all_words=all_words,
                                                    word_completed=index_cw, 
                                                    guesses_made=guesses_made)
        whole_word_guessed = True
        guesses = "6" + guesses_made
        w = get_current_word(all_words, index_cw)
        
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

    index = int(word_completed) + 1
    index_cw = str(index)
    guesses = '1'
   
    return redirect(url_for('.in_game', 
                            all_words=all_words, 
                            index_cw=index_cw, 
                            guesses_made=guesses))

@app.route("/<all_words>/<index_cw>/<guesses_made>/<s>/<q>", methods=['GET', 'POST'])
def undo(all_words, index_cw, guesses_made, s, q):
    ''' undoes the last action, if last action was a new game call, recalls last word,
        until first word, then returns to intro page, NOT a back button'''

    if len(guesses_made) <= 1:
        while int(index_cw) > 0:
            prev_index = str(int(index_cw) - 1)
            old_word = get_current_word(all_words, prev_index)
            display_word = shown_word(old_word, "1")
            whole_word_guessed = False
            
            return render_template('game-page.html', 
                                    all_words=all_words, 
                                    index_cw=prev_index, 
                                    guesses_made="1", 
                                    word=display_word, 
                                    word_guessed=whole_word_guessed)
        if int(index_cw) == 0:
            return render_template('/intro.html')
  
    prev_guesses_made = guesses_made[1:]

    w = get_current_word(all_words, index_cw)

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