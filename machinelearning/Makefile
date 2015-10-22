
#include ../../hadoop.mk

include spark.config.mk

WAREHOUSE=/Users/kamanashisroy/jantarmantar/sandbox/opt/data/spark/warehouse
SPARK_HOME=/Users/kamanashisroy/jantarmantar/sandbox/opt/spark-1.5.1-bin-hadoop2.6
SPARK=$(SPARK_HOME)/bin/spark-submit
#SPARK_FLAGS=--packages com.databricks:spark-csv_2.11:1.2.0
SOURCES=$(wildcard src/spark*.py)

all:run


help:setenv
	$(SPARK) --help

shell:setenv
	$(SPARK)

run:setenv
	echo $(SOURCES)
	$(SPARK) $(SPARK_FLAGS) $(SOURCES)

spark:setenv
	$(SPARK_HOME)/bin/pyspark

word_matrix:
	python src/word_matrix.py


setenv:
	export SPARK_HOME=$(SPARK_HOME)

