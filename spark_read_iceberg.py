# spark_read_iceberg.py

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("IcebergToTigerGraph")
    .getOrCreate()
)

# Unity Catalog identifiers
CATALOG = "main"
SCHEMA = "commerce"
USERS_TABLE = f"{CATALOG}.{SCHEMA}.users"
PRODUCTS_TABLE = f"{CATALOG}.{SCHEMA}.products"
TRANSACTIONS_TABLE = f"{CATALOG}.{SCHEMA}.transactions"

# Read Iceberg tables via Unity Catalog
users_df = spark.read.table(USERS_TABLE)
products_df = spark.read.table(PRODUCTS_TABLE)
transactions_df = spark.read.table(TRANSACTIONS_TABLE)

users_df.show()
products_df.show()
transactions_df.show()