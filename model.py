import annoy 
import numpy as np
from scipy.spatial.distance import cosine
import librosa
from ETL import compute_features
import pandas as pd

# Function to convert DataFrame to NumPy array
def dataframe_to_np_array(df):
    # Extracting features from the DataFrame
    features_dict = df.to_dict(orient='records')[0]['features']
    
    # Concatenating MFCC features
    mfcc_vector = np.concatenate([
        features_dict["mfcc"]["mean"],
        features_dict["mfcc"]["std"],
        features_dict["mfcc"]["skew"],
        features_dict["mfcc"]["kurtosis"],
        features_dict["mfcc"]["median"],
        features_dict["mfcc"]["min"],
        features_dict["mfcc"]["max"]
    ])
    
    # Creating ZCR vector
    zcr_vector = np.array([
        features_dict["zcr"]["mean"],
        features_dict["zcr"]["std"],
        features_dict["zcr"]["median"],
        features_dict["zcr"]["min"],
        features_dict["zcr"]["max"]
    ])
    
    # Creating spectral centroid vector
    spectral_centroid_vector = np.array([
        features_dict["spectral_centroid"]["mean"],
        features_dict["spectral_centroid"]["std"],
        features_dict["spectral_centroid"]["median"],
        features_dict["spectral_centroid"]["min"],
        features_dict["spectral_centroid"]["max"]
    ])
    
    # Combine all feature vectors into a single vector
    combined_vector = np.concatenate([mfcc_vector, zcr_vector, spectral_centroid_vector])
    
    return combined_vector

# Convert provided DataFrame to NumPy array
provided_features_df = pd.read_pickle("features.pkl")
provided_features_vector = dataframe_to_np_array(provided_features_df)

# Function to create and return the Locality-Sensitive Hashing (LSH) hash table using the AnnoyIndex class
def create_annoy_index(features, n_trees):
    index = annoy.AnnoyIndex(len(features), "angular")
    index.add_item(0, features)  # Add a single item for the combined feature vector
    index.build(n_trees)
    return index

# Create AnnoyIndex object
annoy_index = create_annoy_index(provided_features_vector, 100)

# Function to get nearest neighbors
def get_nearest_neighbours(new_audio_features, annoy_index, n_neighbours):
    nearest_neighbours = annoy_index.get_nns_by_vector(new_audio_features, n_neighbours)
    return nearest_neighbours

# Function to get best match
def get_best_match(new_audio_features, annoy_index):
    nearest_neighbours = get_nearest_neighbours(new_audio_features, annoy_index, 1)
    return nearest_neighbours[0]

# Path to the new audio file
test_filepath = 'fma_medium/001/001014.mp3'
test_data = compute_features(test_filepath)

# Convert test data to NumPy array
test_features_vector = dataframe_to_np_array(test_data)

# Get best match
best_match_index = get_best_match(test_features_vector, annoy_index)
print("Best Match Index:", best_match_index)

# Get nearest neighbors and print distances
nearest_neighbours = get_nearest_neighbours(test_features_vector, annoy_index, 5)
print("Nearest Neighbors:", nearest_neighbours)
