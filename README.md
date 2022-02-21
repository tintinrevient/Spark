# Spark

## Overview

### Components

`RDD` (Resilient Distributed Dataset) is the main element of the `Spark API`:
* RDD allows you to work with a `distributed` collection the same way you would work with any `local`, non-distributed one;
* RDD provides an elaborate API, which allows you to work with a collection in a `functional` style;
* RDD is `resilient` because it is capable of rebuilding datasets in case of `node failures`;
* RDD is `immutable` (read-only), data transformation always yields a new RDD instance.

<p float="left">
   <img src="pix/components.png" width=700 />
</p>

Given the task of analyzing how many errors of type OutOfMemoryError have happened during the last two weeks.

1. Start the `Spark shell` and establish a connection to the `Spark cluster`:
```bash
spark-shell
```

2. Load the log file from HDFS:
```scala
val lines = sc.textFile("hdfs://path/to/the/file")
```

3. Filter the collection and `cache` it, which tells Spark to leave that RDD in memory across jobs:
```scala
val oomLines = lines.filter(l => l.contains("OutOfMemoryError")).cache()
```

4. Count the collection:
```scala
val result = oomLines.count()
```

<p float="left">
   <img src="pix/rdd.png" width=700 />
</p>

Spark can run on top of the following cluster:
* Hadoop's YARN;
* Spark standalone cluster;
* Apache `Mesos`, which is an advanced distributed system's kernel bringing distributed resource abstractions that can `scale to tens of thousands of nodes` with full fault tolerance.

### Ecosystem

* `Spark Streaming` can replace `Apache Storm`;
* `Spark MLlib` can replace `Apache Mahout`;
* `Spark GraphX` can replace `Apache Giraph`;
* `Spark Core` and `Spark SQL` can replace `Apache Pig`, `Apache Sqoop` and `Apache Hive`;
* `Spark` is for `OLAP`, whereas `HBase` is a ditributed and scalable database for `OLTP`.

<p float="left">
   <img src="pix/spark.png" width=700 />
</p>


## Installation

### Spark standalone cluster

1. Download the Spark binary from [this link](https://spark.apache.org/downloads.html):
```bash
tar -xvzf spark-3.2.1-bin-hadoop3.2.tgz
sudo mv spark-3.2.1-bin-hadoop3.2 /usr/local/spark
```

2. Update `.bashrc`:
```bash
export SPARK_HOME=/usr/local/spark
export PATH=$PATH:$SPARK_HOME/bin
```

3. Start the `Spark shell`:
```bash
spark-shell
```

## Word Count

1. Prepare the local file `docs` as below:
```bash
Mary had a little lamb
its fleece was white as snow
and everywhere that Mary went
the lamb was sure to go
```

2. Execute the following statements in the Spark shell:
```scala
scala> val docs = sc.textFile("hdfs://localhost:9000/docs")
scala> val docs = sc.textFile("file:///home/shu/docs")
scala> val docs = sc.textFile("docs")
docs: org.apache.spark.rdd.RDD[String] = docs MapPartitionsRDD[1] at textFile

scala> val counts = docs.flatMap(line => line.split(" ")).map(word => (word,1)).reduceByKey(_+_)
counts: org.apache.spark.rdd.RDD[(String, Int)] = ShuffledRDD[4] at reduceByKey

counts.collect()
```

3. The result is as below:
```
res0: Array[(String, Int)] = Array((went,1), (its,1), (fleece,1), (as,1), (everywhere,1), (go,1), (lamb,2), (little,1), (white,1), (was,2), (had,1), (a,1), (that,1), (to,1), (sure,1), (Mary,2), (and,1), (snow,1), (the,1))
```

## References
* https://spark.apache.org/docs/latest/sql-data-sources-text.html
