from pyspark import SparkContext
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.feature import IDF


# Load documents (one per line).
sc = SparkContext()
documents = sc.textFile("training/given.txt").map(lambda line: line.split(" "))

hashingTF = HashingTF()
tf = hashingTF.transform(documents)

# ... continue from the previous example
tf.cache()
idf = IDF().fit(tf)
tfidf = idf.transform(tf)

# save the matrix
#tfidf.saveAsSequenceFile("training/matrix.txt")
documents = tfidf.collect()

givenIndex = 0
givenDocumentMatrix = documents[givenIndex]

def similarity(x):
	return givenDocumentMatrix.dot(x)

sim = tfidf.map(similarity).collect()
print sim
