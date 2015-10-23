

Recommender system for github projects
======================================

Project description
---------------------------

The project is a recommender system. It recommends software projects. The recommendation is done based on the similarity of the project descriptions. So the system recommends the matching projects based on a given project.


#### Data collection

##### Data source
The project-data is collected from github.

##### Collected data
Data is collected in csv forms. The are kept in bigdata_info_.csv and bigdata_desc_.csv file. The python code in [collect_data/src] is responsible for downloading data from github.

The following command will collect some data.

```
$> cd collect_data;make
```

Data is saved in directories based on date and time. For example, the collected data may be in,

```
$> head -n 5 15_10_22_19_48/bigdata_keys.txt 
2325298
156018
36502
14807173
1357796
```

The file above are the project ids. The following are the descriptions.

```
$> head -n 5 15_10_22_19_48/bigdata_documents_cat.txt 
Linux kernel source tree
Redis is an in-memory database that persists on disk. The data model is key-value, but many different kind of values are supported: Strings, Lists, Sets, Sorted Sets, Hashes, HyperLogLogs, Bitmaps.
Git Source Code Mirror - This is a publish-only repository and all pull requests are ignored. Please follow Documentation/SubmittingPatches procedure for any of your improvements.
How to Make a Computer Operating System in C++
Emscripten: An LLVM-to-JavaScript Compiler
```

#### Preprocessing
For the ease of processing the data is kept in seperate file while downloading. The bigdata_desc_.csv file contains the description for further processing. And the bigdata_info_.csv file contains the project information.

#### Methodology
The recommender system can be of different types. Namely,

- Content based recommender system
- Colaborative recommender system

Here we used the content based recommender system. Because it does not need user data. Initially we do not have any user data to use colaborative recommender system. Again we may use knowledge based data to build hibrid supervised recommender. 

#### Tools

We used spark to process data.

#### Algorithm

We experimented with `bag of words` or the `document term matrix` algorithms. In investigated the `parts of speech` library for natural language processing.

Finally we used the word similarity detection algorithm provided by spark. It uses tf-idf weighting for similarity detection.

##### Step 1: Loading files

At first we copy the collected data in `machinelearning` directory.

```
cp -rf collect_data/15_10_22_19_48 machinelearning/training
```

The Spark automatically loads the file into distributed RDD objects.

```

# Load documents (one per line).
sc = SparkContext()
documents = sc.textFile("training/bigdata_documents_cat.txt").map(lambda line: line.split(" "))

```

##### Step 2: Find the tf-idf transform

Spark mllib library has TF and IDF implementation.

```
hashingTF = HashingTF()
tf = hashingTF.transform(documents)

# ... continue from the previous example
tf.cache()
idf = IDF().fit(tf)
tfidf = idf.transform(tf)
```

##### Step 3: Find similarity

Now that we have the transform, we can calculate dot matrix product with the target to find the similarity.

```
def similarity(x):
	return givenDocumentMatrix.dot(x)

```
In the above function the `givenDocumentMatrix` is the chosen github project. We compare with all the others like the following,

```
sim = tfidf.map(similarity).collect()
```

We create indexed similarity rdd object for future processing.

```
indexedsim = sim.zipWithIndex().map(lambda keyval: (keyval[1],keyval[0]))
```

And we trim the similarity by some minimum value (here 0.00001)

```
# remove that did not have similarity
trimmedsimilarity = indexedsim.filter(lambda keyval:keyval[1] > 0.00001)
```

##### Step 4: Find recommendation

Now we load the project ids.

```
keys = sc.textFile("training/bigdata_keys.txt")
indexedkeys = keys.zipWithIndex().map(lambda keyval: (keyval[1],keyval[0]))
```

And we join the similarity table with our project id table

```
joined = indexedkeys.join(trimmedsimilarity)
recommendations = joined.values().keys()
print(recommendations.collect())
```

And we are done.


#### Running

The `src/spark_tf_idf.py` file can executed on spark using the execfile() method like `execfile('src/spark_tf_idf')`. Here are some output.

```
>>> indexedsim.collect()
[(0, 25.270868004336236), (1, 0.0), (2, 0.0), (3, 0.0), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0), (9, 0.0), (10, 0.0), (11, 0.0), (12, 0.0), (13, 0.0), (14, 0.0), (15, 0.0), (16, 0.0), (17, 0.0), (18, 0.0), (19, 0.0), (20, 0.0), (21, 5.3018981104783993), (22, 0.0), (23, 0.0), (24, 0.0), (25, 5.3018981104783993), (26, 0.0), (27, 0.0), (28, 0.0)]
>>> trimmedsimilarity = indexedsim.filter(lambda keyval:keyval[1] > 0.00001)
>>> trimmedsimilarity.collect()
[(0, 25.270868004336236), (21, 5.3018981104783993), (25, 5.3018981104783993)]
>>> indexedkeys.collect()
[(0, u'2325298'), (1, u'156018'), (2, u'36502'), (3, u'14807173'), (4, u'1357796'), (5, u'10894716'), (6, u'2810455'), (7, u'1903522'), (8, u'3774328'), (9, u'5101141'), (10, u'901662'), (11, u'692798'), (12, u'23029617'), (13, u'912896'), (14, u'4279682'), (15, u'15634981'), (16, u'20999018'), (17, u'3516624'), (18, u'2990192'), (19, u'37950166'), (20, u'23515024'), (21, u'184981'), (22, u'34676773'), (23, u'11715753'), (24, u'26133979'), (25, u'13862381'), (26, u'27860738'), (27, u'14816993'), (28, u'1543431')]
>>> joined = indexedkeys.join(trimmedsimilarity)
>>> joined.collect()
[(0, (u'2325298', 25.270868004336236)), (21, (u'184981', 5.3018981104783993)), (25, (u'13862381', 5.3018981104783993))]
>>> joined.values().keys().collect()
[u'2325298', u'184981', u'13862381']
```

So the recommendations are, 2325298, 184981 and 13862381 .

#### Future

Here are recommendation is done by similarity in only the description. The README.md is better chiose to find similarity. Again they should be preprocessed to find only important words, (for example, nouns). There is an example code to do that [here](preprocess/experimental/nltk_pos.py).




