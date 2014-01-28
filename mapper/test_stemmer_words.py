from PorterStemmer import PorterStemmer

def test_stemming(word, stemmer):
	return stemmer.stem(word)

def main():
	stemmer = PorterStemmer()
	list_words = ['endding', 'ending']
	for word in list_words:
		print word + ' ' + test_stemming(word, stemmer)

if __name__ == '__main__':
	main()

