import os
import numpy as np
import pandas as pd
import librosa
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['music_features']
collection = db['tracks']


def load_files_path():
    directory = 'fma_medium'
# List to store paths of all the wav files
    mp3_files = []
# Walk through all directories and subdirectories
    for root, dirs, files in os.walk(directory):
    # Iterate through all files
        for file in files:
           if file.endswith('.mp3'):
            # Construct the full path to the file and append it to the list
             mp3_files.append(os.path.join(root, file))
    
    return mp3_files


def compute_features(filepath):
    features = {}

    try:
        
        x, sr = librosa.load(filepath, sr=None, mono=True)  # kaiser_fast

        # Compute MFCC
        mfcc = librosa.feature.mfcc(y=x, sr=sr, n_mfcc=20)
        mfcc_stats = {
            'mean': np.mean(mfcc, axis=1).tolist(),
            'std': np.std(mfcc, axis=1).tolist(),
            'skew': np.mean(mfcc, axis=1).tolist(),
            'kurtosis': np.mean(mfcc, axis=1).tolist(),
            'median': np.median(mfcc, axis=1).tolist(),
            'min': np.min(mfcc, axis=1).tolist(),
            'max': np.max(mfcc, axis=1).tolist()
        }
        features['mfcc'] = mfcc_stats

        # Compute Zero Crossing Rate (ZCR)
        zcr = librosa.feature.zero_crossing_rate(x)
        zcr_stats = {
            'mean': np.mean(zcr).tolist(),
            'std': np.std(zcr).tolist(),
            'skew': float('NaN'),
            'kurtosis': float('NaN'),
            'median': np.median(zcr).tolist(),
            'min': np.min(zcr).tolist(),
            'max': np.max(zcr).tolist()
        }
        features['zcr'] = zcr_stats

        # Compute Spectral Centroid
        spectral_centroid = librosa.feature.spectral_centroid(y=x, sr=sr)
        spectral_centroid_stats = {
            'mean': np.mean(spectral_centroid).tolist(),
            'std': np.std(spectral_centroid).tolist(),
            'skew': float('NaN'),
            'kurtosis': float('NaN'),
            'median': np.median(spectral_centroid).tolist(),
            'min': np.min(spectral_centroid).tolist(),
            'max': np.max(spectral_centroid).tolist()
        }
        features['spectral_centroid'] = spectral_centroid_stats

    except Exception as e:
        print('{}: {}'.format(filepath, repr(e)))

    return features

def main():
    mp3_files = load_files_path()

    for file in mp3_files:
        features = compute_features(file)
        track_id = os.path.basename(file).split('.')[0]  # Extract the file name without extension

        collection.insert_one({'_id': track_id, 'features': features})

if __name__ == "__main__":
    main()