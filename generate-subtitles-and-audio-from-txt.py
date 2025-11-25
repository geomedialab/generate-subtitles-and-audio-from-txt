import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from nltk import word_tokenize

import pydub

name  = input('Enter filepath of .txt file: ')
with open(name, 'r', encoding='utf-8') as file:
    data = file.read()
output_name = name.split('.')[0]


def s_to_hms(seconds):
    #print seconds
    m, sec = divmod(seconds, 60)
    h, m = divmod(m, 60)    
    #print str(int(h)) + ":" + str(int(m)) + ":" + str(int(s))
    #return str(int(h)) + ":" + str(int(m)) + ":" + str(int(sec))
    return str(int(h)) + ":" + str(int(m)) + ":" + str(float("{0:.2f}".format(round(sec,2))))

def formalize_timestamp(i):
    if len(i.split(":")[0]) == 1:
        h1 = "0" + i.split(":")[0]
    else:
        h1 = i.split(":")[0]
        
    if len(i.split(":")[1]) == 1:
        m1 = "0" + i.split(":")[1]
    else:
        m1 = i.split(":")[1]
        
    if len(i.split(":")[2].split(".")[0]) == 1:
        s1 = "0" + i.split(":")[2]
    else:
        s1 = i.split(":")[2]

    #ES: add zeros to seconds
    s1 = s1.split(".")
    if len(s1[1]) == 1:
        s1[1] = s1[1] + '00'
    if len(s1[1]) == 2:
        s1[1] = s1[1] + '0'
    s1 = s1[0] + "." + s1[1]
    
    return str(h1 + ":" + m1 + ":" + s1)


sentences = nltk.sent_tokenize(data)
words = nltk.word_tokenize(data)

sentences = [string for string in sentences if string != '']

print("number of sentences: ", len(sentences))
print("number of words: ", len(words))
print("number of seconds (words/3): ", len(words)/3)


#create subtitles
i = 1
seconds_elapsed = 0
with open(output_name+'.srt', 'w', encoding='utf-8') as file:
    for (j,sentence) in enumerate(sentences):
        sentence = sentence.strip()
        #create timestamps
        words = word_tokenize(sentence)
        
        #subtitle units should have 3 words per second (ex. 15 words = 5-second subtitle unit)
        seconds_span = len(words)/3
        hms_start = formalize_timestamp(s_to_hms(seconds_elapsed))
        hms_end = formalize_timestamp(s_to_hms(seconds_elapsed+seconds_span))
        
        file.write('\n')
        file.write(str(i))
        file.write('\n')
        file.write(hms_start)
        file.write(' --> ')
        file.write(hms_end)
        file.write('\n')
        file.write(sentence)
        file.write('\n')
        
        seconds_elapsed+=seconds_span
        i+=1
        



#calculate duration of audio file in milliseconds
audio_duration = int((seconds_elapsed + seconds_span) * 1000)

#generate  blank audio segment with duration
blank_audio = pydub.AudioSegment.silent(duration=audio_duration)

#export blank audio segment to file
blank_audio.export(output_name + '.mp3', format='mp3')