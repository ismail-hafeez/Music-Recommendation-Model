# Import necessary packages
import pymongo
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import col
from pyspark.ml.feature import MinHashLSH


# Make connection to MongoDB
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")

# MongoDB Details
input_uri = "mongodb://127.0.0.1/music_features.tracks"

# Create SparkSession
spark = SparkSession.builder \
    .appName("MyApp") \
    .config("spark.mongodb.input.uri", input_uri) \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:2.4.2") \
    .getOrCreate()

# Load data from MongoDB collection "tracks"
df = spark.read.format('com.mongodb.spark.sql.DefaultSource').load()

# Show schema of the DataFrame
df.printSchema()


# Show first few rows of the DataFrame
df.show(truncate = False)

# Stop SparkSession
spark.stop()
