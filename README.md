

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

TODO show the csv file contents.


#### Preprocessing
For the ease of processing the data is kept in seperate file while downloading. The bigdata_desc_.csv file contains the description for further processing. And the bigdata_info_.csv file contains the project information.

#### Methodology
The recommender system can be of different types. Namely,

- Content based recommender system
- Colaborative recommender system

Here we used the content based recommender system. Because it does not need user data. Initially we do not have any user data to use colaborative recommender system. Again we may use knowledge based data to build hibrid supervised recommender. 

Algorithm
---------------

We experimented with `bag of words` or the `document term matrix` algorithms. In investigated the `parts of speech` library for natural language processing.

Finally we used the word similarity detection algorithm provided by spark. It uses tf-idf weighting and k-nearest neighbour algorithms for similarity detection.


TODO specify sources

Running
--------------

