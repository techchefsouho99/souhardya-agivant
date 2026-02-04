from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("S3-Tables-Iceberg-Debug")
    .config(
        "spark.sql.extensions",
        "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
    )

    # AWS S3 Tables = REST catalog
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

    # AWS auth / IO
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

print("\n=== Catalogs ===")
spark.sql("SHOW CATALOGS").show(truncate=False)

print("\n=== Namespaces ===")
spark.sql("SHOW NAMESPACES IN s3tables").show(truncate=False)

print("\n=== Tables ===")
spark.sql("""
SHOW TABLES IN s3tables.agivant_s3_namespace_2
""").show(truncate=False)

print("\n=== Products sample ===")
df = spark.sql("""
SELECT *
FROM s3tables.agivant_s3_namespace_2.products
LIMIT 20
""")

df.show(truncate=False)

spark.stop()
