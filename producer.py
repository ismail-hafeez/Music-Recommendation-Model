from kafka import KafkaProducer
import json
import pandas as pd
from time import sleep

# Kafka broker address
bootstrap_servers = ['localhost:9092']

# Create a Kafka producer instance
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Define the topic to which messages will be sent
topic = 'user_interactions'

file_path = "/home/hdoop/Desktop/project/WebPage/audio_data.csv"

# Initial read of the CSV file
df = pd.read_csv(file_path)
id_list = list(df['ID'])

# Send the initial message to the Kafka topic
producer.send(topic, value=id_list)
print('Initial list sent to Kafka:', id_list)

# Start monitoring the CSV file for changes
while True:
    # Sleep for a short interval before checking for changes
    sleep(2)
    
    # Read the CSV file
    new_df = pd.read_csv(file_path)
    
    # Check if the data has changed
    if not new_df.equals(df):
        # Update the DataFrame and get the new list of IDs
        df = new_df
        id_list = list(df['ID'])
        
        # Send the updated message to the Kafka topic
        producer.send(topic, value=id_list)
        print('Updated list sent to Kafka:', id_list)

        # Flush the producer to ensure all messages are sent
        producer.flush()

# Close the producer
# producer.close()

