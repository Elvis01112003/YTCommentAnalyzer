import pandas as pd
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

def sepposnegcom(comment_file):
    # Check if the file exists
    if not os.path.exists(comment_file):
        raise FileNotFoundError(f"The file '{comment_file}' does not exist.")

    # Reading Dataset
    dataset = pd.read_csv(comment_file, encoding_errors='ignore')

    # Check if the required column 'Comment' exists
    if 'Comment' not in dataset.columns:
        raise ValueError("The dataset does not contain a 'Comment' column.")

    # Sentiment analysis of comments using Vader sentiment analyzer
    analyser = SentimentIntensityAnalyzer()

    def vader_sentiment_result(sent):
        scores = analyser.polarity_scores(sent)
        if scores["neg"] > scores["pos"]:
            return 0
        return 1

    dataset['vader_sentiment'] = dataset['Comment'].apply(lambda x: vader_sentiment_result(x))

    # Separating Positive and Negative Comments
    pos_comments = dataset[dataset['vader_sentiment'] == 1]
    neg_comments = dataset[dataset['vader_sentiment'] == 0]

    # Writing positive and negative comments to CSV files
    positive_comments = pos_comments.to_csv("Positive_Comments.csv", index=False)
    negative_comments = neg_comments.to_csv("Negative_Comments.csv", index=False)

    # Determine total positive and negative comments
    video_positive_comments = str(len(pos_comments)) + ' Comments'
    video_negative_comments = str(len(neg_comments)) + ' Comments'

    # Check if positive and negative CSV files are empty
    if pos_comments.empty:
        video_positive_comments = '0 Comments'
    if neg_comments.empty:
        video_negative_comments = '0 Comments'

    # Return function
    return positive_comments, negative_comments, video_positive_comments, video_negative_comments

