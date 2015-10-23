from pyspark import SparkContext
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.feature import IDF


# Load documents (one per line).
sc = SparkContext()
documents = sc.textFile("training/bigdata_documents_cat.txt").map(lambda line: line.split(" "))

hashingTF = HashingTF()
tf = hashingTF.transform(documents)

# ... continue from the previous example
tf.cache()
idf = IDF().fit(tf)
tfidf = idf.transform(tf)

# save the matrix
#tfidf.saveAsSequenceFile("training/matrix.txt")
tfidfmatrix = tfidf.collect()

count = str(tfidf.count())

givenIndex = 0
givenDocumentMatrix = tfidfmatrix[givenIndex]

def similarity(x):
	return givenDocumentMatrix.dot(x)

sim = tfidf.map(similarity)
indexedsim = sim.zipWithIndex().map(lambda keyval: (keyval[1],keyval[0]))

keys = sc.textFile("training/bigdata_keys.txt")
indexedkeys = keys.zipWithIndex().map(lambda keyval: (keyval[1],keyval[0]))

# remove that did not have similarity
trimmedsimilarity = indexedsim.filter(lambda keyval:keyval[1] > 0.00001)

joined = indexedkeys.join(trimmedsimilarity)

recommendations = joined.values().keys()

print(recommendations.collect())

