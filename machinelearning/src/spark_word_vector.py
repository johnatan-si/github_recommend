from pyspark import SparkContext
from pyspark import SQLContext
from pyspark.mllib.feature import Word2Vec

sc = SparkContext()


#documents = sqlContext.read.format("com.databricks.spark.csv").option("header", "false").load("training/bigdata_desc_.csv")
val input = sc.textFile("text8").map(line => line.split(",").toSeq)

print(documents)

word2vec = Word2Vec()
model = word2vec.fit(documents)

synonyms = model.findSynonyms('linux', 40)

for word, cosine_distance in synonyms:
    print "{}: {}".format(word, cosine_distance)

