from flask import Flask, redirect, render_template,request, url_for

from random import shuffle

from helpers import (add_on, d_lets, shown_word, word_keys, 
                    word_dict, rando_word_pick, get_current_word,
                    quick_decode, quick_encode)



app = Flask(__name__)

app.config['DEBUG'] = True
# below makes our simple decode function availanble for jinja to display in place
app.jinja_env.globals.update(guess_display=quick_decode)

@app.route("/")
def here_we_go():
    '''start first game from scratch'''
    return render_template('intro.html')

@app.route("/game", methods=['GET', 'POST'])
def start_from_rando():
    ''' starts game with random word '''
   
   # just shuffling the words and picking the first one
    shuffle(word_keys)
    all_words = ''.join(word_keys)
    #TODO encrypt index_cw
    index_cw = "0"
    guesses = '1'
   
    return redirect(url_for('.in_game', all_words=all_words, index_cw=index_cw, coded_guesses=guesses))


@app.route("/<all_words>/<index_cw>/<coded_guesses>", methods=['POST', 'GET'])
def in_game(all_words, index_cw, coded_guesses):
    ''' main game play, built with params '''
    
    word = get_current_word(all_words, index_cw)
   

    guesses = quick_decode(coded_guesses) #TODO decode here 
    whole_word_guessed = False
    for guess in coded_guesses:
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
                                coded_guesses=coded_guesses)
    
    for guess in coded_guesses:
        if guess.lower() not in word.lower():
            mistakes.append(guess.lower())
    # reminder that mistakes will always contain 1
    guesses_remaining = 9 - len(mistakes) 
    
    if guesses_remaining == 0:
        return render_template('loser.html')

    if request.method == 'POST':
        
        let_guess = request.form['letter_guess']
        if not let_guess.isalpha():
            # won't include non letter chars in guesses
            return redirect(url_for('.in_game', 
                                all_words=all_words, 
                                index_cw=index_cw, 
                                coded_guesses=coded_guesses))

        coded_guesses = quick_encode(let_guess) + coded_guesses #encode let_guess here
        
        
        return redirect(url_for('.in_game', 
                                all_words=all_words, 
                                index_cw=index_cw, 
                                coded_guesses=coded_guesses))
    
    return render_template('game-page.html', 
                                all_words=all_words, 
                                index_cw=index_cw, 
                                coded_guesses=coded_guesses, 
                               
                                word=display_word, 
                                word_guessed=whole_word_guessed,
                                guesses_remaining=guesses_remaining)

@app.route("/<all_words>/<index_cw>/<coded_guesses>/<t>", methods=['POST', 'GET'])                    
def word_guess(all_words, index_cw, coded_guesses, t):
    if request.method == 'POST':
        word_guess = request.form['word_guess']
        if word_guess.lower() == get_current_word(all_words, index_cw):
            print("you won")
            remaining = 8 - int(index_cw)
            return render_template('congrats.html', remaining=remaining, 
                                                    all_words=all_words,
                                                    word_completed=index_cw, 
                                                    coded_guesses=coded_guesses)
        whole_word_guessed = True
        guesses = "6" + coded_guesses #6 will act as a marker in guess series that whole word was attempted
        w = get_current_word(all_words, index_cw)
        
        display_word = shown_word(w, quick_decode(guesses))
        return render_template('game-page.html', 
                                all_words=all_words, 
                                index_cw=index_cw, 
                                coded_guesses=guesses, 
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
                            coded_guesses=guesses))

@app.route("/<all_words>/<index_cw>/<coded_guesses>/<s>/<q>", methods=['GET', 'POST'])
def undo(all_words, index_cw, coded_guesses, s, q):
    ''' undoes the last action, if last action was a new game call, recalls last word,
        until first word, then returns to intro page, NOT a back button'''

    if len(coded_guesses) <= 1:
        while int(index_cw) > 0:
            prev_index = str(int(index_cw) - 1)
            old_word = get_current_word(all_words, prev_index)
            display_word = shown_word(old_word, "1")
            whole_word_guessed = False
            
            return render_template('game-page.html', 
                                    all_words=all_words, 
                                    index_cw=prev_index, 
                                    coded_guesses="1", 
                                    word=display_word, 
                                    word_guessed=whole_word_guessed)
        if int(index_cw) == 0:
            return render_template('/intro.html')
  
    prev_coded_guesses = coded_guesses[1:]

    w = get_current_word(all_words, index_cw)

    display_word = shown_word(w, quick_decode(prev_coded_guesses))

    whole_word_guessed = False
    for guess in coded_guesses:
        if guess == '6':
            whole_word_guessed=True

    return render_template('game-page.html', 
                                all_words=all_words, 
                                index_cw=index_cw, 
                                coded_guesses=prev_coded_guesses, 
                                word=display_word, 
                                word_guessed=whole_word_guessed)



if __name__ == "__main__":
    ''' shouldn't use this as a production server, but for now. 
    I'll use nginx and/or gunicorn if live deploy'''
    #app.run(host='0.0.0.0', port=80)
    app.run()