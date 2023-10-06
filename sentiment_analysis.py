import nltk
import os
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag
import pandas as pd
import os
from dotenv import load_dotenv

if not load_dotenv(): # This condition will exit the program if there is no .env file
    print("Could not load .env file or it is empty. Please check if it exists and is readable.")
    exit(1)

# loading environmental variables
input = os.environ.get("Input_file_path")
Extracted_files = os.environ.get("Extracted_files")
output = os.environ.get("output_file_path")
stopwords_folder_path = os.environ.get("Stop_words_folder")
Positive_words_file = os.environ.get("Positive_words_file")
Negative_words_file = os.environ.get("Negative_words_file")

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

# Creating empty variables to store the results of sentiment analysis
URL_ID = []
Movie_Name = []
URL = []
Positive_score = []
negative_score = []
Polarity_score = []
Subjective_score = []
Avg_sentence_length = []
percentage_of_comp_words = []
f_index = []
Avg_words_per_sent = []
Comp_word_count = []
syllable_per_wrd = []
PRN = []
avg_wrd_len = []

# Function to perform the sentiment analysis.
def sentiment_analysis(filepath):
    excel_data = pd.read_excel(filepath)
    data_frame = pd.DataFrame(excel_data)
    print(data_frame)

    # Iterrating Rows in the excel file
    for index, row in data_frame.iterrows():
        print(row['Movie_name'])

        # Reading the extracted files.
        file = open(f"{Extracted_files}/{row['Movie_name']}.txt","r", encoding="utf-8")
        global data_raw_1
        global data_raw
        data_raw = ""
        data_raw_1 = (file.read()).upper()

        #removing punctiations.
        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        for ele in data_raw_1:
            if ele in punc:
                data_raw = data_raw_1.replace(ele, "")

        #creating word tokens.
        data = word_tokenize(data_raw)

        #cleaning Stop words.
        stw_path = stopwords_folder_path
        stw = ""
        for filename in os.listdir(stw_path):
            f = os.path.join(stw_path, filename)
            file = open(f,"r")
            st_words = file.read()
            stw += st_words.upper()
        stw = word_tokenize(stw)
        clean_data = []
        removed_words = []
        for word in data:
            if word not in stw:
                clean_data.append(word)
            else:
                removed_words.append(word)

        # Reading the positive words and conterting them to tokens.
        file = open(Positive_words_file)
        pos_words = word_tokenize((file.read()).upper())
        
        # Reading the negative words and conterting them to tokens. 
        file = open(Negative_words_file)
        neg_words = word_tokenize((file.read()).upper())

        # calculating positive and negative score.
        pos_score = 0
        neg_score = 0
        for word in clean_data:
            if word in pos_words:
                pos_score += 1
            elif word in neg_words:
                neg_score += 1

        # calculating the polarity and subjective score.
        polarity_score = (pos_score - neg_score)/((pos_score + neg_score) + 0.000001)
        subjective_score = (pos_score + neg_score)/((len(clean_data))+ 0.000001)

        # finding complex words (where the word that contain more than 2 vowels are considered as complex words).
        vowels = ["A","E","I","O","U"]
        complex_words = []
        total_syllables = 0
        for word in clean_data:
            syllable = 0
            word_f = word
            clean_word = False
            if word[-2: ] == "ES" or word[-2: ] == "ED":
                word = word[:(len(word)-2)]
                clean_word = True
            for character in word:
                if character in vowels:
                    syllable += 1
                    total_syllables += 1
            if syllable > 2 and clean_word == False:
                complex_words.append(word)
            elif syllable > 2 and clean_word == True:
                complex_words.append(word_f)

        # finding the number of sentences.
        no_of_sentence = len(sent_tokenize(data_raw_1))
        no_of_words= len(clean_data)

        # finding the average sentence length.
        avg_sentence_length = no_of_words / no_of_sentence

        # finding percentage of complex words.
        Percentage_of_Complex_words = len(complex_words)/len(clean_data)

        # finding the fog index.
        fog_index = 0.4 * (avg_sentence_length + Percentage_of_Complex_words)

        # finding syllable per word.
        syllable_per_word = total_syllables / len(clean_data)

        # finding total characters.
        total_chars = 0
        for word in clean_data:
            for character in word:
                total_chars += 1
        
        # finding the average length of word.
        avg_word_length = total_chars/len(clean_data)

        # finding the count of pronouns.
        p_pronouns = pos_tag(data)
        prp_count = 0
        for tuple in p_pronouns:
            if tuple[1] == 'PRP':
                prp_count += 1
        
        # appending the values into the variables.
        URL_ID.append(row['URL_ID'])
        Movie_Name.append(row['Movie_name'])
        URL.append(row['URL'])
        print('positive score : ', pos_score)
        Positive_score.append(pos_score)
        print("negative score : ", neg_score)
        negative_score.append(neg_score)
        print("polarity score : ", polarity_score)
        Polarity_score.append(polarity_score)
        print("subjective score : ", subjective_score)
        Subjective_score.append(subjective_score)
        print("fog index : ", fog_index)
        f_index.append(fog_index)
        print("Percentage_of_Complex_words : ", Percentage_of_Complex_words)
        percentage_of_comp_words.append(Percentage_of_Complex_words)
        print("average sentence length : ", avg_sentence_length)
        Avg_sentence_length.append(avg_sentence_length)
        Avg_words_per_sent.append(avg_sentence_length)
        print("complex word count : ", len(complex_words))
        Comp_word_count.append(len(complex_words))
        print("syllable per word : ", round(syllable_per_word))
        syllable_per_wrd.append(syllable_per_word)
        print("average word length : ", avg_word_length)
        avg_wrd_len.append(avg_word_length)
        print("personal pronoun count : ", prp_count)
        PRN.append(prp_count)

# calling the function.
sentiment_analysis(input)

# creating a dictionary so that we can use it to create a excel file.
dict = {'URL_ID': URL_ID ,
        'Movie_Name' : Movie_Name,
        'URL' : URL,
        'POSITIVE SCORE' : Positive_score,
        'Negative SCORE' : negative_score,
        'POLARITY SCORE' : Polarity_score,
        'SUBJECTIVE SCORE' : Subjective_score,
        'AVG SENTENCE LENGTH' : Avg_sentence_length,
        'PERCENTAGE OF COMPLEX WORDS' : percentage_of_comp_words,
        'FOG INDEX' : f_index,
        'AVG NUMBER OF WORDS PER SENTENCE' : Avg_words_per_sent,
        'COMPLEX WORD COUNT' : Comp_word_count,
        'SYLLABLE PER WORD' : syllable_per_wrd,
        'PERSONAL PRONOUN' : PRN,
        'AVERAGE WORD LENGTH' : avg_wrd_len}

# Changing the dictionary into Data dataframe which is more organised than a dictionary.
df = pd.DataFrame(dict)
print(df)

# creating the output excel file that contains the results of the sentiment analysis.
df.to_excel(output,index= False)
