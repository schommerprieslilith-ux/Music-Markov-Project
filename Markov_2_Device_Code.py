#Importing Packages 
import time
import board
import digitalio
import busio

import Markov_2_Handel_Dictionary #This code is designed to work with a dictionary trained by the Markov_2_Trainer code 
import random 


#####
#
# Setup for using the MIDI synth
#
#####

# Variables set to the hardcoded numerical values used by the VS1053 MIDI synth chipset

VS1053_BANK_DEFAULT = 0x00
VS1053_BANK_DRUMS1 = 0x78
VS1053_BANK_DRUMS2 = 0x7F
VS1053_BANK_MELODY = 0x79
MIDI_NOTE_ON = 0x90
MIDI_NOTE_OFF = 0x80
MIDI_CHAN_MSG = 0xB0
MIDI_CHAN_BANK = 0x00
MIDI_CHAN_VOLUME = 0x07
MIDI_CHAN_PAN = 0x0A
MIDI_CHAN_PROGRAM = 0xC0 

#This makes it easy to change the volume of the music played 
VOLUME = 50 

# Initial Setup on boot - needed if using a battery. If just USB can skip to section 4.

# 1. Force the TX pin HIGH immediately on boot to stablilize the MIDI line
midi_tx_stabilize = digitalio.DigitalInOut(board.TX)
midi_tx_stabilize.direction = digitalio.Direction.OUTPUT
midi_tx_stabilize.value = True

# 2. Give the VS1053 synth chip a moment to recognize the stable high line
time.sleep(0.5)

# 3. Deinitialize the pin so CircuitPython releases it for UART use
midi_tx_stabilize.deinit()

# 4. Now initialize the standard MIDI UART at the required 31,250 baud rate
uart = busio.UART(board.TX, board.RX, baudrate=31250)

#Defining basic note functions to streamline interfacing with the device 
def note_on(channel, note, vel):
    #Turns on a note on a certain channel with a certain pitch (note) and volume 
    uart.write(bytearray([MIDI_NOTE_ON | channel, note, vel]))


def note_off(channel, note):
    #Turns off a certain note (pitch) on a certain channel 
    uart.write(bytearray([MIDI_NOTE_OFF | channel, note, 0]))


def set_channel_bank(channel, bank): 
    #Sets up the chosen instrument bank on a certain channel 
    uart.write(bytearray([MIDI_CHAN_MSG | channel, MIDI_CHAN_BANK, bank]))


def set_channel_volume(channel, vol): 
    #Sets the initial volume for the channel 
    uart.write(bytearray([MIDI_CHAN_MSG | channel, MIDI_CHAN_VOLUME, vol]))


def set_channel_instrument(channel, num): 
    #Sets the instrument for the channel 
    uart.write(bytearray([MIDI_CHAN_PROGRAM | channel]))
    time.sleep(0.01)
    uart.write(bytearray([num]))
    time.sleep(0.01)


def set_channel_pan(channel, pan): 
    #Sets the left-right orientation of the sound for your speaker setup 
    uart.write(bytearray([MIDI_CHAN_MSG | channel, MIDI_CHAN_PAN, pan]))


def main():
    print("The program is running\n")
    #Defining the variable my_dictionary as the imported dictionary 
    my_dictionary = Markov_2_Handel_Dictionary.dictionary
    generate_music(my_dictionary) 

def generate_music(dictionary):
    #Generates music while the program runs, using the imported dictionary 
    
    #Creates a list of dictionary keys 
    dictionary_keys = list(dictionary.keys()) 
    #Chooses the first two starting notes and uses them (in string form) to define the variable previous_str 
    previous_str = choose_starting_notes(dictionary, dictionary_keys)
    #Turns the string into a list of strings, each containing different pieces of information 
    #The information will be of the form: [1st_note_length, 1st_note_pitch, 2nd_note_length, 2nd_note_pitch] 
    note_list = previous_str.split()

    #Prints this list form of the note, so that you can see what note is playing and have some visual of the code running 
    print(note_list)

    #Plays the first note by turning the first note on, waits for a time corresponding to the note length, then turns the 1st note off 
    #The relevant information is gotten from the various elements in the variable note_string 
    note_on(0, int(note_list[1]), VOLUME) #The elements in note_string are all strings, so the type has to be changed to an integer 
    time.sleep(make_float(note_list[0])) #Sometimes the value stored here is a fraction becuase of the information from the Music21 Corpus, so this insures that any fractions are converted to floats and that the object type is a float 
    note_off(0, int(note_list[1]))

    #Plays the second note 
    note_on(0, int(note_list[3]), VOLUME)
    time.sleep(make_float(note_list[2]))
    note_off(0, int(note_list[3])) 

    #Generates notes while the program continues to run 
    while True: 
        #Checks if the previous two notes are a key in the dictionary 
        if previous_str not in dictionary_keys:
            #If the previous notes are not a dictionary key, new notes are generated using the list of dictionary keys 
            previous_str = choose_starting_notes(dictionary, dictionary_keys)
            note_list = previous_str.split() 

            #Visual showing of the notes 
            #You can tell when new notes have to be generated this way because the printed list will have 4 items instead of 2 
            print(note_list)
        
            #These notes are then played 
            note_on(0, int(note_list[1]), VOLUME)
            time.sleep(make_float(note_list[0]))
            note_off(0, int(note_list[1]))

            note_on(0, int(note_list[3]), VOLUME)
            time.sleep(make_float(note_list[2]))
            note_off(0, int(note_list[3]))
        #This creates the variable list_of_weights as an empty list to be filled with the weights of potential following notes stored in the dictionary 
        list_of_weights = []
        for n_str in dictionary[previous_str]:
            #Breaks down the value of the dictionary for the previous two notes (the key) 
            #For each potential note, the weight is appended to the list_of_weights 
            list_of_weights.append(dictionary[previous_str][n_str])
        #The next note (in string form), represented by next_str, is chosen using the list_of_weights 
        #The weighted_choice function matches the weights from the list_of_weights with the list of potential notes 
        #Circuit Python does not support the weighted choice from the random package 
        #The potential notes are gotten from the value of the dictionary for the previous two notes, then looking at the keys of this nested dictionary 
        next_str = weighted_choice(list(dictionary[previous_str].keys()), list_of_weights)
        #The string form of the next note is then split into a list of the format [next_note_length, next_note_pitch] 
        next_str_list = next_str.split()

        #A printed visual of the note 
        #This will be a list of length 2 instead of a list of length 4, like what was printed above 
        print(next_str_list)
    
        #The note is played 
        note_on(0, int(next_str_list[1]), VOLUME)
        time.sleep(make_float(next_str_list[0]))
        note_off(0, int(next_str_list[1]))

        #The previous_str and note_list are reset for the new previous two notes 
        previous_str = note_list[2] + " " + note_list[3] + " " + next_str
        note_list = previous_str.split() 
        #The code then repeats while the program still runs 
    return 

def choose_starting_notes(dictionary, dictionary_keys):
    #Chooses a random key from the dictionary as the starting notes and then double-checks that the key is not the "end" key 
    previous_str = dictionary_keys[random.randint(0, len(dictionary_keys)-1)]
    if previous_str == "end": 
        while previous_str == "end": 
            previous_str = dictionary_keys[random.randint(0, len(dictionary_keys)-1)]
    return previous_str 

def make_float(number):
    #Checks if the number is in the form of a fraction by checking for a '/' 
    if '/' in number:
        #If the number is a fraction, the variables numerator and denominator are defined by splitting the string at the '/' 
        numerator, denominator = number.split('/')
        #The result is then the float of each divided 
        result = float(numerator) / float(denominator)
    else:
        #If the number is not a fraction, its type is just changed to a float 
        result = float(number)
    return result #The result is returned 

def weighted_choice(items, weights):
    #The total weight is calculated 
    total_weight = sum(weights)
    #Then a random value within the total span of weights (summed) is generated 
    r = random.uniform(0, total_weight)
    #The item this random value corresponds to is then found and returned 
    #Items with more weight take up more of the span of weight, so they are more likely to be chosen 
    for item, weight in zip(items, weights):
        r -= weight
        if r <= 0:
            return item

# Set up a piano instrument on channel 0
set_channel_bank(0, VS1053_BANK_MELODY)
set_channel_volume(0, VOLUME)
set_channel_instrument(0, 0)  # piano

main()