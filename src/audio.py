from pydub import AudioSegment

song = AudioSegment.from_mp3("never_gonna_give_you_up.mp3")

# pydub does things in milliseconds
ten_seconds = 10 * 1000

first_10_seconds = song[:ten_seconds]

last_5_seconds = song[-5000:]

## make the beginning louder and the end quieter

# boost volume by 6dB
beginning = first_10_seconds + 6

# reduce volume by 3dB
end = last_5_seconds - 3

