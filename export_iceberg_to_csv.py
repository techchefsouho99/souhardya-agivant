from pyspark.sql import SparkSession

# Databricks-compatible Spark Session
spark = (
    SparkSession.builder
    .appName("Iceberg-S3Tables-Export-To-CSV")
    .config(
        "spark.sql.extensions",
        "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
    )

    # AWS S3 Tables (Iceberg REST catalog)
    .config("spark.sql.catalog.s3tables", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.s3tables.type", "rest")
    .config(
        "spark.sql.catalog.s3tables.uri",
        "https://s3tables.eu-north-1.amazonaws.com"
    )
    .config(
        "spark.sql.catalog.s3tables.warehouse",
        "s3tables://agivant-s3-table-bucket"
    )

    # AWS IO + region
    .config(
        "spark.sql.catalog.s3tables.io-impl",
        "org.apache.iceberg.aws.s3.S3FileIO"
    )
    .config(
        "spark.sql.catalog.s3tables.client.region",
        "eu-north-1"
    )
    .getOrCreate()
)

print("=== Catalogs ===")
spark.sql("SHOW CATALOGS").show(truncate=False)

print("=== Namespaces ===")
spark.sql("SHOW NAMESPACES IN s3tables").show(truncate=False)

print("=== Tables ===")
spark.sql("""
SHOW TABLES IN s3tables.agivant_s3_namespace_2
""").show(truncate=False)

# Read Iceberg Tables from s3 bucket
users_df = spark.sql("""
SELECT *
FROM s3tables.agivant_s3_namespace_2.users
""")

products_df = spark.sql("""
SELECT *
FROM s3tables.agivant_s3_namespace_2.products
""")

transactions_df = spark.sql("""
SELECT *
FROM s3tables.agivant_s3_namespace_2.transactions
""")

# Sanity check
print("=== Products Sample ===")
products_df.show(10, truncate=False)

# Write CSVs to S3 (EXPORT ZONE)
EXPORT_BASE = "s3://agivant-export/csv"

(
    users_df
    .coalesce(1)                    # optional: fewer files
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(f"{EXPORT_BASE}/users")
)

(
    products_df
    .coalesce(1)
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(f"{EXPORT_BASE}/products")
)

(
    transactions_df
    .coalesce(1)
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(f"{EXPORT_BASE}/transactions")
)

print("✅ Iceberg tables exported to CSV successfully")

spark.stop()
