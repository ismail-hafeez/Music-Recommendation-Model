# Music-Recommendation-Model

Tools Used
1. Apache Spark
2. Apache Kafka
3. MongoDB
4. Pyspark
5. Flask
6. Ubuntu

Overview

This project aims to develop a music recommendation system utilizing the Free Music Archive (FMA) dataset. The system is designed to provide personalized music recommendations to users based on their preferences and listening history.
Dataset

The FMA dataset comprises 106,574 tracks, each lasting 30 seconds, spanning 161 genres. Additionally, the FMA metadata dataset provides track details such as title, artist, genres, tags, and play counts for all tracks. The dataset is stored in MongoDB for scalability and accessibility.
ETL Pipeline

The Extract, Transform, Load (ETL) pipeline is implemented in Python to process the dataset. Feature extraction techniques such as Mel-Frequency Cepstral Coefficients (MFCC), spectral centroid, and zero-crossing rate are applied to convert audio files into numerical and vector formats. Normalization, standardization, and dimensionality reduction techniques are explored to enhance the accuracy of the recommendation model.
Music Recommendation Model

Apache Spark is utilized to train the music recommendation model. Both collaborative filtering and Approximate Nearest Neighbors (ANN) algorithms are evaluated for recommendation accuracy. Hyperparameter tuning is performed to optimize model performance. Evaluation metrics are used to assess the effectiveness of the recommendation model.
Deployment

The recommendation model is deployed onto a web application using Flask framework. Apache Kafka is employed to generate music recommendations in real-time based on user activity and historical playback data. The web application features an interactive interface for users to explore music recommendations tailored to their preferences.
Reporting

A comprehensive report detailing the methodology and findings of the music recommendation system is provided. The report evaluates the effectiveness and implementation of the recommendation system, highlighting key insights and performance metrics.

For more details, please refer to the documentation and codebase in the GitHub repository.
Contributors

    John Doe
    Jane Smith

License

This project is licensed under the MIT License - see the LICENSE file for details.
