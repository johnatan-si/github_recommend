from pyspark import SQLContext
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.feature import IDF

sc = SQLContext()

# Load documents (one per line).
# sc = SparkContext()
#documents = sc.textFile("...").map(lambda line: line.split(" "))

documents = sc.read.format("com.databricks.spark.csv").option("header", "false").load("training/bigdata_desc_.csv").map(lambda row: row[1])

print(documents)

hashingTF = HashingTF()
tf = hashingTF.transform(documents)

# ... continue from the previous example
tf.cache()
idf = IDF().fit(tf)
tfidf = idf.transform(tf)

print(tfidf)

