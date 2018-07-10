from flask import Flask, redirect, render_template,request, url_for


from helpers import add_on, d_lets,shown_word, word_keys, word_dict, rando_word_pick



app = Flask(__name__)

app.config['DEBUG'] = True


@app.route("/")
def here_we_go():
    '''start first game from scratch'''
    return render_template('intro.html')

@app.route("/game", methods=['POST', 'GET'])
def start_from_rando():
    ''' starts game with random word '''
    current_word = rando_word_pick()
    #adds dummy value to make up for removed word key
    foolin = add_on()
    word_keys.remove(current_word)
    words_keys_for_display = word_keys[:]
    words_keys_for_display.append(foolin)
    print(words_keys_for_display)
    words_left = ''.join(words_keys_for_display)

    guesses = '1'
    # return render_template('game-page.html', words_left=words_left, word=word, guesses=None)
    # return redirect('{{ words_left }}/{{word}}/{{guesses}}')
    return redirect(url_for('.in_game', words_left=words_left, current_word=current_word, guesses_made=guesses))


@app.route("/<words_left>/<current_word>/<guesses_made>", methods=['POST', 'GET'])
def in_game(words_left, current_word, guesses_made):
    ''' main game play, built with params '''
    word = word_dict[current_word]
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
        
        return render_template('congrats.html', remaining=words_left)
    
    if request.method == 'POST':
            let_guess = request.form['letter_guess']
            print(let_guess)
            if let_guess.lower() not in word.lower():
                mistakes += 1
            print(str(mistakes))
            guesses_made = let_guess + guesses_made #encode let_guess here
            print(guesses_made)
            
            return redirect(url_for('.in_game', words_left=words_left, current_word=current_word, guesses_made=guesses_made))
    return render_template('game-page.html', 
                            words_left=words_left, 
                            current_word=current_word, 
                            guesses_made=guesses, 
                            word=display_word, 
                            word_guessed=whole_word_guessed)

@app.route("/<words_left>/<current_word>/<guesses_made>/<t>", methods=['POST', 'GET'])                    
def word_guess(words_left, current_word, guesses_made, t):
    if request.method == 'POST':
        word_guess = request.form['word_guess']
        if word_guess.lower() == word_dict[current_word].lower():
            print("you won")
            return render_template('congrats.html', remaining=words_left)
        whole_word_guessed = True
        guesses = "6" + guesses_made
        w = word_dict[current_word]
        display_word = shown_word(w, guesses)
        return render_template('game-page.html', 
                                words_left=words_left, 
                                current_word=current_word, 
                                guesses_made=guesses, 
                                word=display_word, 
                                word_guessed=whole_word_guessed)

@app.route("/new_game/<words_left>", methods=['POST', 'GET'])
def next_game(words_left):
    ''' starts new game from words left '''
    if words_left[0] in d_lets:
        print("GAME is totally complete!!")
        return render_template('congrats.html', remaining=None)
    current_word = rando_word_pick()
    #adds dummy value to make up for removed word key
    print("$$$$$$$$$$$$$$$$$")
    print(len(words_left))
    how_many_to_add = 9 - (len(words_left))
    foolin = ''
    for i in range(how_many_to_add):
        foolin += add_on()
        i += 1
    print(len(foolin))
    word_keys.remove(current_word)
    words_keys_for_display = word_keys[:]
    words_keys_for_display.append(str(foolin))
   
    words_left = ''.join(words_keys_for_display)
    guesses = '1'
   
    return redirect(url_for('.in_game', 
                            words_left=words_left, 
                            current_word=current_word, 
                            guesses_made=guesses))

@app.route("/<words_left>/<current_word>/<guesses_made>", methods=['POST'])
def undo(words_left, current_word, guesses_made):
    if request.form['btn'] == 'Undo':
        prev_words_left = words_left[1:]
        prev_guesses_made = guesses_made[1:]
        w = word_dict[current_word]
        display_word = shown_word(w, guesses_made)

        for guess in guesses_made:
            if guess == '6':
                whole_word_guessed=True
    
        return render_template('game-page.html', 
                                    words_left=prev_words_left, 
                                    current_word=current_word, 
                                    guesses_made=prev_guesses_made, 
                                    word=display_word, 
                                    word_guessed=whole_word_guessed)



if __name__ == "__main__":
    app.run()