from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
import pandas as pd
from pathlib import Path
import random


# warehouse_local = str(Path("warehouse").resolve())
warehouse_hdfs = "hdfs://localhost:9000/hive/warehouse"


def create_hive_table(spark: SparkSession, table_name: str) -> None:
    # Generate a random table with 3 columns and 100 rows
    table_cols = ["col_1", "col_2", "col_3"]
    table_values = []
    for row_index in range(100):
        table_value = (random.random(), random.random(), random.random())
        table_values.append(table_value)

    # Create a Spark data frame
    df = spark.createDataFrame(data=table_values, schema=table_cols)
    df.show(5)
    df.printSchema()

    # Create a table in the Hive warehouse
    # df.createOrReplaceTempView("df_view") # Only in memory
    # df.createGlobalTempView(table_name) # Only in memory, and shared across multiple sessions
    df.write.saveAsTable(table_name) # Default format is parquet
    spark.catalog.listTables()


def read_hive_table(spark: SparkSession, table_name: str) -> None:
    df = spark.read.parquet(f"{warehouse_hdfs}/{table_name}")
    df.show(5)


def read_from_json(spark: SparkSession, dir_name: str) -> None:
    df = spark.read.json(f"hdfs://localhost:9000/data/{dir_name}")
    df.show(5)


def write_to_json(spark: SparkSession, table_name: str, dir_name: str) -> None:
    df = spark.table(table_name)
    df.repartition(1).write.mode("overwrite").json(f"hdfs://localhost:9000/data/{dir_name}")


def write_to_postgresql(spark: SparkSession, table_name: str) -> None:
    df = spark.table(table_name)
    df.write.format("jdbc").option("url", "jdbc:postgresql://localhost:5432/test_db")\
        .option("driver", "org.postgresql.Driver")\
        .option("dbtable", "test_table")\
        .option("user", "hive")\
        .option("password", "hive").save()


def write_to_hbase(spark: SparkSession, table_name: str) -> None:
    df = spark.table(table_name)


if __name__ == "__main__":
    spark = SparkSession.builder.master("local[*]")\
        .config("spark.jars", "file:///home/shu/Documents/workspace/Spark/jar/postgresql-42.3.0.jar")\
        .config("spark.sql.warehouse.dir", warehouse_hdfs)\
        .getOrCreate()

    table_name = "test_table"
    dir_name = "test_dir"

    # spark.sql(f"ALTER TABLE {table_name} SET TBLPROPERTIES('external'='false');")
    # spark.sql(f"DROP TABLE IF EXISTS {table_name}")

    # Create a Hive table
    # create_hive_table(spark=spark, table_name=table_name)

    # Extract from a Hive Table, and load into a JSON file
    # write_to_hdfs(spark=spark, table_name=table_name, dir_name=dir_name)

    # Read a Hive table
    # read_hive_table(spark=spark, table_name=table_name)

    # Read a JSON file
    read_from_json(spark=spark, dir_name=dir_name)
