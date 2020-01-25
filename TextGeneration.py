# Larger LSTM Network to Generate Text for Alice in Wonderland
import numpy
import sys
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

def preprocess(sentence):
	sentence = sentence.lower()
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(sentence)
	filtered_words = filter(lambda token: token not in stopwords.words('english'), tokens)
	return " ".join(filtered_words)



# Read the file and store
text = open("wonderland.txt").read()

text = text.lower()

# Distinct Characters
distinct_chars = sorted(list(set(text)))
no_chars_text = len(text)
no_chars_unique = len(distinct_chars)


# summarize the loaded data
print("Total Characters: ", no_chars_text)
print("Total Vocab: ", no_chars_unique)

# Map char to int in Dictionary
char_int_dict = dict((c, i) for i, c in enumerate(distinct_chars))
int_to_char = dict((i, c) for i, c in enumerate(distinct_chars))

# input to output pairs
sequence_length = 100
dataX = []
dataY = []
for i in range(0, no_chars_text - sequence_length, 1):
	in_sq= text[i:i + sequence_length]
	out_sq = text[i + sequence_length]
	dataX.append([char_int_dict[char] for char in in_sq])
	dataY.append(char_int_dict[out_sq])

#Number of Patterns
no_patterns = len(dataX)
print("Total Patterns: ", no_patterns)

# reshape X and Normalize
X = numpy.reshape(dataX, (no_patterns, sequence_length, 1))
X = X / float(no_chars_unique)

# Hot Encoding
y = np_utils.to_categorical(dataY)


#LSTM
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))

# model = Sequential()
# model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
# model.add(Dropout(0.2))
# model.add(Dense(y.shape[1], activation='softmax'))

# load the network weights
filename = "weights-improvement-50-1.2742-bigger.hdf5"
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')
# pick a random seed
start = numpy.random.randint(0, len(dataX)-1)
pattern = dataX[start]
print("Seed:")
print("\"", ''.join([int_to_char[value] for value in pattern]), "\"")
# generate characters
for i in range(1000):
	x = numpy.reshape(pattern, (1, len(pattern), 1))
	x = x / float(no_chars_unique)
	prediction = model.predict(x, verbose=0)
	index = numpy.argmax(prediction)
	result = int_to_char[index]
	seq_in = [int_to_char[value] for value in pattern]
	sys.stdout.write(result)
	pattern.append(index)
	pattern = pattern[1:len(pattern)]
print("\nDone.")

