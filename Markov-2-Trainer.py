#importing packages 
#music21 is a package that has a corpus of music as well as providing the tools in python to work with music 
from music21 import * 

import random 

#These are imported so that you can update a log (to keep track of training your model) 
import datetime 
import json 

#This is where you can import a presaved (or empty) dictionary that can be updated and trained with this code 
#If you import an empty dictionary, I reccommend typing in the file: dictionary = {"end":{}} 
#This prevents an error 
import Music_Markov_2_Test_Dictionary

def main(): 
    print("The program is running\n")
    #Defining the variable my_dictionary as your imported dictionary 
    my_dictionary = Music_Markov_2_Test_Dictionary.dictionary
    
    while True:
        #This gives you options for what to do 
        print("What would you like to do?")
        print("  1) save the current model.")
        print("  2) train the model.")
        print("  3) quit.")
        selection_num = int(input())
        
        #Make sure to save the current model if you want your external dictionary to be updated 
        if selection_num == 1:
            #This opens your dictionary file and rewrites it with the current dictionary model 
            with open("Music_Markov_2_Test_Dictionary.py", "w") as file:
                file.write("dictionary = ")
                file.write(json.dumps(my_dictionary))
            #This updates the log file 
            with open("Music_Markov_2_Log.log", "a") as log_file:
                now = datetime.datetime.now()
                log_file.write(str(now))
                log_file.write(" Music_Markov_2_Test_Dictionary.py saved. \n") 
            print("Music_Markov_2_Test_Dictionary.py updated")
        
        elif selection_num == 2:
            #You can add in different training functions 
            print("How would you like to input the training text? ")
            print(" 1) with Music21 Corpus") #This training function uses the Music21 Corpus 
            second_selection = int(input())
            if second_selection == 1: 
                my_dictionary = corpus_training(my_dictionary) 
                #This updates the external dictionary file 
                with open("Music_Markov_2_Test_Dictionary.py", "w") as file:
                    file.write("dictionary = ")
                    file.write(json.dumps(my_dictionary))
                #This updates the log file 
                with open("Music_Markov_2_Log.log", "a") as log_file:
                    now = datetime.datetime.now()
                    log_file.write(str(now))
                    log_file.write(" Music_Markov_2_Test_Dictionary.py trained by Music21 Corpus ")
                    log_file.write(".\n")
                print("Training Successful. \n")
            else:
                pass # if the second input is a number not 1, do nothing.
        elif selection_num == 3:
            break
        else:
            print("I did not understand your selection.")
    
    
def corpus_training(dictionary): 
    #This function goes through the music21 corpus by composer and updates the dictionary it is passed 
    #You can comment out all the composers that you do not want to pull from the corpus 
    #It redefines the dictionary as an updated version that includes the music from the composer 
    #The corpus.getComposer('composer_name') part gets a list of music by that composer from the music21 corpus 
    dictionary = music_from_composer(corpus.getComposer('airdsAirs'), dictionary)
    dictionary = music_from_composer(corpus.getComposer('bach'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('beach'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('beethoven'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('chopin'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('ciconia'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('corelli'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('cpebach'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('demos'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('essenFolksong'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('handel'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('haydn'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('joplin'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('johnson_j_r'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('josquin'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('leadSheet'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('liliuokalani'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('luca'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('lusitano'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('miscFolk'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('monteverdi'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('mozart'), dictionary)
    dictionary = music_from_composer(corpus.getComposer('nottingham-dataset'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('oneills1850'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('palestrina'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('ryansMammoth'), dictionary)
    dictionary = music_from_composer(corpus.getComposer('schoenberg'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('schubert'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('schumann_robert'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('schumann_clara'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('theoryExercises'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('trecento'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('verdi'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('weber'), dictionary) 
    dictionary = music_from_composer(corpus.getComposer('webern'), dictionary)
    return dictionary

def music_from_composer(composer_list, dictionary):
    #This function takes in a list of music from the music21 corpus and the dictionary 
    #It then breaks up the list of music into each piece 
    for elem in composer_list: 
        #Each piece is then turned into a score (a single object in music21) 
        score = corpus.parse(elem)
        #This score is then used to update the dictionary 
        dictionary = update_dictionary(dictionary, score) 
    return dictionary 

def update_dictionary(dictionary, score): 
    #This function takes a dictionary (to be updated) and a score (to update the dictionary with) 
    #This if statement checks if the score is long enough to build or update a two-note Markov model 
    if len(list(score.flatten().getElementsByClass(note.Note))) < 3: 
        #If the score is not long enough, the dictionary is returned as is 
        return dictionary
    #This defines the two variables previous_n_1 and previous_n_2 as the first two notes of the score 
    #The score is flattened so that all parts are strung together and the score itself is broken down into a list of notes 
    previous_n_1 = list(score.flatten().getElementsByClass(note.Note))[0]
    previous_n_2 = list(score.flatten().getElementsByClass(note.Note))[1]
    #This for-loop lookes at every other note in the score (other than the first two) 
    for n in list(score.flatten().getElementsByClass(note.Note))[2:]: 
        #The way this dictionary is set up is it has a list of keys that are a string representation of the two previous notes 
        #The coresponding value is a nested dictionary with each note that can posibly follow the two previous notes and the weighted probability that it does follow the two previous notes 
        #The possibility and weight are determined by the occurance of the note following the two previous notes in a score 
        #This checks if the two previous notes already form a key in the dictionary or not 
        if str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi) not in dictionary: 
            #If not, they are added as a new key and the current note is set to a weight of one 
            dictionary[str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi)] = {str(n.quarterLength) + " " + str(n.pitch.midi): 1} 
        else: 
            #If the previous notes are a pre-existing dictionary key, it is checked next if the current note has a pre-existing weight or not 
            if str(n.quarterLength) + " " + str(n.pitch.midi) in dictionary[str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi)]: 
                #If it does, the weight is increased by one because the current note has followed the previous two notes one more time 
                dictionary[str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi)][str(n.quarterLength) + " " + str(n.pitch.midi)] += 1 
            else: 
                #If not, the current note is set to a weight of one 
                dictionary[str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi)].update({str(n.quarterLength) + " " + str(n.pitch.midi): 1}) 
        #The previous notes are then reset 
        previous_n_1 = previous_n_2 
        previous_n_2 = n 
    
    #This part of the code deals with the left-over notes after a score is done being processed 
    #It is necissary to deal with them because they can be generated and then become previous notes while still having no following notes 
    #To address this, an additional key, "end", is created to store them 
    #This if statement checks if they already exist in the key "end" 
    if str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi) in dictionary["end"]: 
        #If they do, their weight is increased 
        dictionary["end"][str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi)] += 1 
    else: 
        #If they don't, they are added with a weight of one 
        dictionary["end"].update({str(previous_n_1.quarterLength) + " " + str(previous_n_1.pitch.midi) + " " + str(previous_n_2.quarterLength) + " " + str(previous_n_2.pitch.midi): 1}) 
    return dictionary #The updated dictionary is returned 

main() 
