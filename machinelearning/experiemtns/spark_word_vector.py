from pyspark import SparkContext
from pyspark.mllib.feature import Word2Vec


sc = SparkContext()

inp = sc.textFile("training/given.txt").map(lambda line: line.split(" "))

model = Word2Vec().fit(inp)

vec = model.transform("The")
print vec

#synonyms = model.findSynonyms('The', 40)
#print [s[0] for s in synonyms]



