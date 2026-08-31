from music21 import * 
import random 

import datetime 
import json 

import Music_Markov_2_Test_Dictionary

def main(): 
    print("The program is running\n")
    my_dictionary = Music_Markov_2_Test_Dictionary.dictionary
    
    while True:
        print("What would you like to do?")
        print("  1) generate music with the current model.")
        print("  2) save the current model.")
        #print("  3) re-initialize the model.")
        print("  4) train the model.")
        print("  5) quit.")
        #try:
        selection_num = int(input())
        if selection_num == 1:
            #try:
            test = input("How many notes would you like to generate? ")
            print(test) 
            num_n = int(test)
            music = generate_music(my_dictionary, num_n) 
            print("Music Generated ") 
            music.show()
            #except:
                #print("I did not understand your input.")
        elif selection_num == 2:
            with open("Music_Markov_2_Test_Dictionary.py", "w") as file:
                file.write("dictionary = ")
                file.write(json.dumps(my_dictionary))
            with open("Music_Markov_2_Log.log", "a") as log_file:
                now = datetime.datetime.now()
                log_file.write(str(now))
                log_file.write(" Music_Markov_2_Test_Dictionary.py saved. \n") 
            print("Music_Markov_2_Test_Dictionary.py updated")
            #print("Where would you like to save?")
            #print(" 1) Default file.")
            #print(" 2) given file")
            
        #elif selection_num == 3:
            #print("How would you like to initialize?")
            #print("  1) with the green eggs and ham text.")
            #print("  2) with a textfile.")
            #print("  3) return to previous menu.")
            #second_selection_num = int(input())
            #if second_selection_num == 1:
                #my_dictionary = initializedict("greeneggsandham.txt")
                #with open("dictionary_prototype.py", "w") as file:
                    #file.write("dictionary = ")
                    #file.write(json.dumps(my_dictionary))
                #with open("dictionary_prototype.log", "a") as log_file:
                    #now = datetime.datetime.now()
                    #log_file.write(str(now))
                    #log_file.write(" dictionary_prototype.py re-initialized by greeneggsandham.txt. \n")
                #print("Model initialized and dictionary file updated.")
                # Run the initialzedict function with the greeneggsandham.txt file, then overwrite the dictionary_prototype.py file with the new dictionary, and append a new entry to the log file. 
            #elif second_selection_num == 2:
                #print("Not implemented")
            #elif second_selection_num == 3:
                #pass
            #else: 
                #print("I did not understand your selection.")
        
        elif selection_num == 4:
            print("How would you like to input the training text? ")
            print(" 1) with basic training") 
            print(" 2) with Music21 Corpus") 
            
            #try:
            second_selection = int(input())
            if second_selection == 1:
                my_dictionary = basic_training(my_dictionary)
                with open("Music_Markov_2_Test_Dictionary.py", "w") as file:
                    file.write("dictionary = ")
                    file.write(json.dumps(my_dictionary))
                with open("Music_Markov_2_Log.log", "a") as log_file:
                    now = datetime.datetime.now()
                    log_file.write(str(now))
                    log_file.write(" Music_Markov_2_Test_Dictionary.py trained by Basic Training ")
                    log_file.write(".\n")
                print("Training Successful. \n")
            elif second_selection == 2: 
                my_dictionary = corpus_training(my_dictionary) 
                with open("Music_Markov_2_Test_Dictionary.py", "w") as file:
                    file.write("dictionary = ")
                    file.write(json.dumps(my_dictionary))
                with open("Music_Markov_2_Log.log", "a") as log_file:
                    now = datetime.datetime.now()
                    log_file.write(str(now))
                    log_file.write(" Music_Markov_2_Test_Dictionary.py trained by Music21 Corpus ")
                    log_file.write(".\n")
                print("Training Successful. \n")
            else:
                pass # if the second input is a number not 1 or 2, do nothing.
            #except:
                #pass # if the second input is not a number do nothing.
            
            '''print("  1) via a text file.")
            print("  2) manually")
            try:
                second_selection = int(input())
                if second_selection == 1:
                    file_name = input("What is the name of the text file?")
                    with open(file_name) as f:
                        training_text = f.read()
                    my_dictionary = traindict(my_dictionary, training_text)
                    with open("dictionary_prototype.py", "w") as file:
                        file.write("dictionary = ")
                        file.write(json.dumps(my_dictionary))
                    with open("dictionary_prototype.log", "a") as log_file:
                        now = datetime.datetime.now()
                        log_file.write(str(now))
                        log_file.write(" dictionary_prototype.py trained by ")
                        log_file.write(file_name)
                        log_file.write(".\n")
                    print("Training Successful. \n")
                elif second_selection == 2:
                    training_text = input("Please enter the training text:\n")
                    my_dictionary = traindict(my_dictionary, training_text)
                    with open("dictionary_prototype.py", "w") as file:
                        file.write("dictionary = ")
                        file.write(json.dumps(my_dictionary))
                    with open("dictionary_prototype.log", "a") as log_file:
                        now = datetime.datetime.now()
                        log_file.write(str(now))
                        log_file.write(" dictionary_prototype.py trained manually. \n")
                    print("Training Successful. \n")
                else:
                    pass # if the second input is a number not 1 or 2, do nothing.
            except:
                pass # if the second input is not a number do nothing.'''
            
        elif selection_num == 5:
            break
        else:
            print("I did not understand your selection.")
        #except:
            #print("I did not understand your selection.")
    
    
def basic_training(dictionary): 
    my_dictionary = dictionary  
    
    Bach1 = corpus.parse('bach/bwv57.8') 
    #Bach1.show('text') 
    my_dictionary = update_dictionary(my_dictionary, Bach1) 
    
    Bach2 = corpus.parse('bach/bwv85.6') 
    #Bach2.show('text') 
    my_dictionary = update_dictionary(my_dictionary, Bach2) 
    
    Handel = corpus.parse('handel/rinaldo/Lascia_chio_pianga') 
    #Handel.show('text') 
    my_dictionary = update_dictionary(my_dictionary, Handel) 
    
    Haydn1 = corpus.parse('haydn/opus1no1/movement1') 
    #Hayden1.show('text') 
    my_dictionary = update_dictionary(my_dictionary, Haydn1) 
    return my_dictionary 

def corpus_training(dictionary): 
    #dictionary = music_from_composer(corpus.getComposer('airdsAirs'), dictionary)
    #dictionary = music_from_composer(corpus.getComposer('bach'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('beach'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('beethoven'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('chopin'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('ciconia'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('corelli'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('cpebach'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('demos'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('essenFolksong'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('handel'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('haydn'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('joplin'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('johnson_j_r'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('josquin'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('leadSheet'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('liliuokalani'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('luca'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('lusitano'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('miscFolk'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('monteverdi'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('mozart'), dictionary)
    #dictionary = music_from_composer(corpus.getComposer('nottingham-dataset'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('oneills1850'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('palestrina'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('ryansMammoth'), dictionary)
    #dictionary = music_from_composer(corpus.getComposer('schoenberg'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('schubert'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('schumann_robert'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('schumann_clara'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('theoryExercises'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('trecento'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('verdi'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('weber'), dictionary) 
    #dictionary = music_from_composer(corpus.getComposer('webern'), dictionary)
    return dictionary

def music_from_composer(composer_list, dictionary):
    for elem in composer_list: 
        score = corpus.parse(elem)
        dictionary = update_dictionary(dictionary, score) 
    return dictionary 

def update_dictionary(dictionary, score): 
    if len(list(score.flatten().getElementsByClass(note.Note))) < 3: 
        print(score) 
        return dictionary
    previous_n_1 = list(score.flatten().getElementsByClass(note.Note))[0]
    previous_n_2 = list(score.flatten().getElementsByClass(note.Note))[1]
    for n in list(score.flatten().getElementsByClass(note.Note))[2:]: 
        if str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi) not in dictionary: 
            dictionary[str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi)] = {str(n.quarterLength) + " " + str(n.pitch.midi): 1} 
            previous_n_1 = previous_n_2 
            previous_n_2 = n  
        else: 
            if str(n.quarterLength) + " " + str(n.pitch.midi) in dictionary[str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi)]: 
                dictionary[str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi)][str(n.quarterLength) + " " + str(n.pitch.midi)] += 1 
                previous_n_1 = previous_n_2 
                previous_n_2 = n 
            else: 
                dictionary[str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi)].update({str(n.quarterLength) + " " + str(n.pitch.midi): 1}) 
                previous_n_1 = previous_n_2 
                previous_n_2 = n 
    if str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi) in dictionary["end"]: 
        dictionary["end"][str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi)] += 1 
    else: 
        dictionary["end"].update({str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi): 1}) 
    return dictionary 

def generate_music(dictionary, n_number): 
    s = stream.Stream()  
    dictionary_keys = list(dictionary.keys()) 
    #print(dictionary_keys)
    note_list = choose_starting_notes(dictionary, dictionary_keys)
    previous_n_1 = note_list[0] 
    previous_n_2 = note_list[1] 
    s.append(previous_n_1) 
    s.append(previous_n_2)
    previous_str = note_list[2]
    while (n_number - 2)>0: 
        if previous_str not in dictionary_keys: 
            note_list = choose_starting_notes(dictionary, dictionary_keys)
            previous_n_1 = note_list[0] 
            previous_n_2 = note_list[1] 
            s.append(previous_n_1) 
            s.append(previous_n_2)
            previous_str = note_list[2]
            n_number -= 2 
        list_of_weights = [] 
        for n_str in dictionary[previous_str]: 
            list_of_weights.append(dictionary[previous_str][n_str])
        next_str = random.choices(list(dictionary[previous_str].keys()), list_of_weights)[0] 
        next_str_list = next_str.split()
        next_n = note.Note(int(next_str_list[1]), quarterLength = make_float(next_str_list[0]))
        s.append(next_n) 
        previous_str = str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi) + " " + str(make_float(next_str_list[0])) + " " + str(int(next_str_list[1])) 
        #print(previous_str) 
        previous_str_list = previous_str.split()
        previous_n_1 = note.Note(int(previous_str_list[1]), quarterLength = make_float(previous_str_list[0])) 
        previous_n_2 = note.Note(int(previous_str_list[3]), quarterLength = make_float(previous_str_list[2]))
        #print(previous_str)
        n_number -= 1 
    return s 

def choose_starting_notes(dictionary, dictionary_keys): 
    previous_str = dictionary_keys[random.randint(0, len(dictionary_keys)-1)] 
    #print(previous_str) 
    previous_str_list = previous_str.split()
    previous_n_1 = note.Note(int(previous_str_list[1]), quarterLength = make_float(previous_str_list[0])) 
    previous_n_2 = note.Note(int(previous_str_list[3]), quarterLength = make_float(previous_str_list[2])) 
    return [previous_n_1, previous_n_2, previous_str]

def make_float(number): 
    if '/' in number:
        numerator, denominator = number.split('/')
        result = float(numerator) / float(denominator)
    else:
        result = float(number)
    return result 

main() 
