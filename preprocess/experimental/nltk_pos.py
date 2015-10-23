from nltk import pos_tag
from nltk.tokenize import word_tokenize 

s = "This is a simple sentence"
# nltk.download() the requred package is asked
tokens = word_tokenize(s) 
tokens_pos = pos_tag(tokens)

# keep only the nouns
trimmed_tokens = filter ( lambda x:x[1] == "NN", tokens_pos)

#print(trimmed_tokens)
for x in trimmed_tokens :
	print(x[0])
