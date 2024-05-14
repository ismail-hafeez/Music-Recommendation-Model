from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import ArrayType, DoubleType
from scipy.spatial.distance import cosine
import numpy as np
import pymongo
from kafka import KafkaConsumer
import json
import csv
from pyspark.sql import SparkSession
from ETL import compute_features
from pyspark.sql.functions import col

# Kafka configuration
bootstrap_servers = ['localhost:9092']
topic = 'user_interactions'  # Kafka topic containing user interactions

# Create Kafka consumer
consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

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

# Select the features column and the MFCC subfields
df_selected = df.select("_id", "features.mfcc.mean")

# Convert the mfcc mean array to a list
df_list = df_selected.withColumn("mfcc_mean_list", col("mean").cast("array<double>")).drop("mean")

# Collect the DataFrame and convert it to a list
track_features = df_list.collect()

# Define a function to compute cosine similarity
def compute_cosine_similarity(vector1, vector2):
    return 1 - cosine(vector1, vector2)

def find_query_mfcc(id):
    for entry in track_features:
        if(entry["_id"]== query_id):
            return entry["mfcc_mean_list"]

# Process the Kafka stream
for message in consumer:
    # Extract the list of IDs from the Kafka message
    id_list = message.value
    
    # Iterate through each ID in the list
    for id_value in id_list:
        # Convert the ID to a string if necessary
        query_id = str(id_value) if not isinstance(id_value, str) else id_value

        # Find the MFCC features corresponding to the ID
        query_mfcc = np.array(find_query_mfcc(query_id))

        # If MFCC features are found, compute similarities
        if query_mfcc is not None:
            # Initialize an empty list to store track IDs and cosine similarities
            similarities = []

            # Iterate through all entries in track_features
            for entry in track_features:
                track_id = entry["_id"]
                mean_mfcc_list = np.array(entry["mfcc_mean_list"])
                
                # Compute cosine similarity between query MFCC and current mean MFCC list
                if query_mfcc.ndim == 1 and mean_mfcc_list.ndim == 1:
                    similarity = compute_cosine_similarity(query_mfcc, mean_mfcc_list)
                    # Append track ID and cosine similarity to the list
                    similarities.append((track_id, similarity))

            # Sort the similarities list based on cosine similarity in descending order
            similarities.sort(key=lambda x: x[1], reverse=True)

            # Print or write the top similar tracks to a CSV file
            top_similar_tracks = similarities[1:6]
            print(f"Top 2 Similar Tracks for {query_id}: {top_similar_tracks}")

            # Write the top similar tracks to a CSV file
            with open('show_rec.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for track_id, similarity in top_similar_tracks:
                    writer.writerow([track_id])


#spark.stop()
