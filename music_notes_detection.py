#install these libraries ----

import numpy as np
import math
import wave
from pydub import AudioSegment
import os
import struct
import matplotlib.pyplot as plt

def note_detect(file_name):
	#-------------------------------------------
	#here we are just storing our sound file as a numpy array
	#you can also use any other method to store the file as an np array
	# audio_file = wave.open(file_name)
	# file_length=audio_file.getnframes() 
	# f_s=audio_file.getframerate() #sampling frequency
	# sound = np.zeros(file_length) #blank array



	# for i in range(file_length) : 
	# 	wdata=audio_file.readframes(1)
	# 	data=struct.unpack("<h",wdata)
	# 	sound[i] = int(data[0])
	

	a = AudioSegment.from_file(file_name)
	file_length = int(a.frame_count())
	f_s = a.frame_rate
	# print(file_length, f_s, 'pydub ', a.frame_count(), a.frame_rate)
	sound = np.array(a.get_array_of_samples())

	plt.plot(sound)
	plt.show()
	
	sound=np.divide(sound,float(2**15)) #scaling it to 0 - 1
	# counter = audio_file.getnchannels() #number of channels mono/sterio
	counter = a.channels #number of channels mono/sterio
	#-------------------------------------------
	
	plt.plot(sound)
	plt.show()

	#fourier transformation from numpy module
	fourier = np.fft.fft(sound)
	fourier = np.absolute(fourier)
	imax=np.argmax(fourier[0:int(file_length/2)]) #index of max element
	print(imax)
		
	plt.plot(fourier)
	plt.show()

	#peak detection
	i_begin = -1
	threshold = 0.3 * fourier[imax]
	for i in range (0,imax+100):
		if fourier[i] >= threshold:
			if(i_begin==-1):
				i_begin = i				
		if(i_begin!=-1 and fourier[i]<threshold):
			break
	i_end = i
	imax = np.argmax(fourier[0:i_end+100])
	
	freq=(imax*f_s)/(file_length*counter) #formula to convert index into sound frequency
	
	#frequency database
	note=0
	name = np.array(["C0","C#0","D0","D#0","E0","F0","F#0","G0","G#0","A0","A#0","B0","C1","C#1","D1","D#1","E1","F1","F#1","G1","G#1","A1","A#1","B1","C2","C#2","D2","D#2","E2","F2","F#2","G2","G2#","A2","A2#","B2","C3","C3#","D3","D3#","E3","F3","F3#","G3","G3#","A3","A3#","B3","C4","C4#","D4","D4#","E4","F4","F4#","G4","G4#","A4","A4#","B4","C5","C5#","D5","D5#","E5","F5","F5#","G5","G5#","A5","A5#","B5","C6","C6#","D6","D6#","E6","F6","F6#","G6","G6#","A6","A6#","B6","C7","C7#","D7","D7#","E7","F7","F7#","G7","G7#","A7","A7#","B7","C8","C8#","D8","D8#","E8","F8","F8#","G8","G8#","A8","A8#","B8","Beyond B8"])
	frequencies = np.array([16.35,17.32,18.35,19.45,20.60,21.83,23.12,24.50,25.96	,27.50	,29.14	,30.87	,32.70	,34.65	,36.71	,38.89	,41.20	,43.65	,46.25	,49.00	,51.91	,55.00	,58.27	,61.74	,65.41	,69.30	,73.42	,77.78	,82.41	,87.31	,92.50	,98.00	,103.83	,110.00	,116.54	,123.47	,130.81	,138.59	,146.83	,155.56	,164.81	,174.61	,185.00	,196.00	,207.65	,220.00	,233.08	,246.94	,261.63	,277.18	,293.66	,311.13	,329.63	,349.23	,369.99	,392.00	,415.30	,440.00	,466.16	,493.88	,523.25	,554.37	,587.33	,622.25	,659.26	,698.46	,739.99	,783.99	,830.61	,880.00	,932.33	,987.77	,1046.50	,1108.73	,1174.66	,1244.51	,1318.51	,1396.91	,1479.98	,1567.98	,1661.22	,1760.00	,1864.66	,1975.53	,2093.00	,2217.46	,2349.32	,2489.02	,2637.02	,2793.83	,2959.96	,3135.96	,3322.44	,3520.00	,3729.31	,3951.07	,4186.01	,4434.92	,4698.64	,4978.03	,5274.04	,5587.65	,5919.91	,6271.93	,6644.88	,7040.00	,7458.62	,7902.13,8000])
	
	#searching for matched frequencies
	for i in range(0,frequencies.size-1):
			if(freq<frequencies[0]):
				note=name[0]
				break
			if(freq>frequencies[-1]):
				note=name[-1]
				break
			if freq>=frequencies[i] and frequencies[i+1]>=freq :
				if freq-frequencies[i]<(frequencies[i+1]-frequencies[i])/2 :
					note=name[i]
				else :
					note=name[i+1]
				break

		
	return note

if __name__ == "__main__":

	path = os.getcwd()
	# file_name = path + "/wav files/c4.wav"
	file_name = "/home/2403/sample/A4_2s.wav"
	Detected_Note = note_detect(file_name)
	print("\n\tDetected Note = " + str(Detected_Note))

	
# {'C0': 16.35, 'C#0': 17.32, 'D0': 18.35, 'D#0': 19.45, 'E0': 20.6, 'F0': 21.83, 'F#0': 23.12, 'G0': 24.5, 'G#0': 25.96, 'A0': 27.5, 'A#0': 29.14, 'B0': 30.87, 'C1': 32.7, 'C#1': 34.65, 'D1': 36.71, 'D#1': 38.89, 'E1': 41.2, 'F1': 43.65, 'F#1': 46.25, 'G1': 49.0, 'G#1': 51.91, 'A1': 55.0, 'A#1': 58.27, 'B1': 61.74, 'C2': 65.41, 'C#2': 69.3, 'D2': 73.42, 'D#2': 77.78, 'E2': 82.41, 'F2': 87.31, 'F#2': 92.5, 'G2': 98.0, 'G2#': 103.83, 'A2': 110.0, 'A2#': 116.54, 'B2': 123.47, 'C3': 130.81, 'C3#': 138.59, 'D3': 146.83, 'D3#': 155.56, 'E3': 164.81, 'F3': 174.61, 'F3#': 185.0, 'G3': 196.0, 'G3#': 207.65, 'A3': 220.0, 'A3#': 233.08, 'B3': 246.94, 'C4': 261.63, 'C4#': 277.18, 'D4': 293.66, 'D4#': 311.13, 'E4': 329.63, 'F4': 349.23, 'F4#': 369.99, 'G4': 392.0, 'G4#': 415.3, 'A4': 440.0, 'A4#': 466.16, 'B4': 493.88, 'C5': 523.25, 'C5#': 554.37, 'D5': 587.33, 'D5#': 622.25, 'E5': 659.26, 'F5': 698.46, 'F5#': 739.99, 'G5': 783.99, 'G5#': 830.61, 'A5': 880.0, 'A5#': 932.33, 'B5': 987.77, 'C6': 1046.5, 'C6#': 1108.73, 'D6': 1174.66, 'D6#': 1244.51, 'E6': 1318.51, 'F6': 1396.91, 'F6#': 1479.98, 'G6': 1567.98, 'G6#': 1661.22, 'A6': 1760.0, 'A6#': 1864.66, 'B6': 1975.53, 'C7': 2093.0, 'C7#': 2217.46, 'D7': 2349.32, 'D7#': 2489.02, 'E7': 2637.02, 'F7': 2793.83, 'F7#': 2959.96, 'G7': 3135.96, 'G7#': 3322.44, 'A7': 3520.0, 'A7#': 3729.31, 'B7': 3951.07, 'C8': 4186.01, 'C8#': 4434.92, 'D8': 4698.64, 'D8#': 4978.03, 'E8': 5274.04, 'F8': 5587.65, 'F8#': 5919.91, 'G8': 6271.93, 'G8#': 6644.88, 'A8': 7040.0, 'A8#': 7458.62, 'B8': 7902.13, 'Beyond B8': 8000.0}
