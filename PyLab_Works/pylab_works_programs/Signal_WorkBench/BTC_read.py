import wave

filename = 'D:/Data_Python/btc/t.wav'

wav = wave.open( filename,'r')
amount = 14*256*35
data = []

for frame in wav.readframes(amount):
  data.append(ord(frame)*5.0/256.0)
wav.close()

DISPLAY = data