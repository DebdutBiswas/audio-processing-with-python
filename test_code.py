'''
Task1: Audio processing with python (Extract notes from *.wav file)
Team eYRC-BV#638
'''

import numpy, wave, struct

# Necessary global variables:
number_of_files = 5 # Number of files will be tasted

# File info:
file_name = ""
sampling_freq = 0
file_length = 0
total_time = 0

# Window info:
window_time = 0.05 # Set time slice for window "Can be adjustable in different scenario"
window = 0 # Declaration of global varible window size
number_of_windows = 0 #Declaration of global varible number of windows

# Indexing info:
last_index = 0
prev_freq_in_hertz = 0

# Threshold and frequency adjustments info:
min_threshold = 1046 # Starting note is C6 having a frequency of 1046.50 Hz "Can be adjustable in different scenario"
max_threshold = 7902 # Ending note is B8 having a frequency of 7902.13 Hz "Can be adjustable in different scenario"
freq_adjust = 10 # Frequency adjustment threshold (-10Hz ~ +10) "Can be adjustable in different scenario"

# Note identification function:
def identify_notes(frequency_data):
        notes_array = ["C6","D6","E6","F6","G6","A6","B6","C7","D7","E7","F7","G7","A7","B7","C8","D8","E8","F8","G8","A8","B8"]
        frequency_array = [1046,1174,1318,1396,1567,1760,1975,2093,2349,2637,2793,3135,3520,3951,4186,4698,5274,5587,6271,7040,7902]
        frequency_data = int(frequency_data)
        final_note = ""

        if frequency_data > 0:
                for note in range(len(notes_array)):
                        if frequency_data == frequency_array[note] or frequency_array[note]-freq_adjust <= frequency_data <= frequency_array[note]+freq_adjust:
                                final_note = notes_array[note]
                                break
                        else:
                                final_note = "NULL"

        return final_note

# RMS check function:
def check_window(window_data):
        global last_index
        k = 0

        check_frame = numpy.zeros(window,dtype=numpy.int)
        check_frame = numpy.array(check_frame)

        if last_index < (file_length - window):

                for k in range(window):
                        check_frame[k]=window_data[k+last_index]

                last_index += window+1
                rms = int(numpy.sqrt(numpy.mean(numpy.square(check_frame)))) # Calculate root mean square of samples in a window

                if rms == 0:
                        check_window(window_data)

        return check_frame

# Peak frequency check function:
def peak_freq(raw_data):
        w = numpy.fft.fft(raw_data)
        freqs = numpy.fft.fftfreq(len(w))
        #print(freqs.min(), freqs.max())

        # Find the peak in the coefficients
        idx = numpy.argmax(numpy.abs(w))
        freq = freqs[idx]
        freq_in_hertz = abs(freq * sampling_freq)

        return int(freq_in_hertz)

# Main check function:
def check(file_name):
        global sampling_freq, audio_channel, file_length, total_time, window, check_frame, number_of_windows, prev_freq_in_hertz
        print("Reading file: " + str(file_name) + " ...")

        sound_file = wave.open(file_name,'r') # Opening the sound file
        sampling_freq = sound_file.getframerate() # Get sampling freq. or frame rate
        file_length = sound_file.getnframes() # Get number of frames
        total_time = file_length/float(sampling_freq) # Calculate total time of all samples in seconds
        window = int(window_time * sampling_freq) # Calculate length of window (0.05 Sec * 44100 Hz = 2205)
        number_of_windows = int(file_length / window) # Calculate number of windows
        
        data = sound_file.readframes(file_length) # Read and assign 2byte data from crrent frame to a new array "data"
        sound_file.close() # Close the file after reading the stream
        data = struct.unpack('{n}h'.format(n=file_length), data) # Unpack 2byte data one-by-one and assign again to "data" array
        data = numpy.array(data) # Reformat data to array

        final_note_array = []
        
        for g in range(number_of_windows):
                check_frame = check_window(data)
                freq_in_hertz = peak_freq(check_frame)

                if freq_in_hertz != prev_freq_in_hertz and freq_in_hertz != 0:
                        final_note = identify_notes(freq_in_hertz)
                        if final_note != "NULL":
                                final_note_array.append(final_note)

                prev_freq_in_hertz = freq_in_hertz

        final_note_array = numpy.array(final_note_array)

        result = ""
        for notes in range(len(final_note_array)):
                result += " " + str(final_note_array[notes])
        
        print("Identifed notes:" + result + "\n")

# Script main thread:
if __name__ == "__main__":
    print("### Extract notes from *.wav files ###\n")
    for file_number in range(1,number_of_files +1 ):
        file_name = "Test_Audio_files\Audio_" + str(file_number)+".wav"
        check(file_name)
