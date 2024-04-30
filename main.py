from flask import Flask, render_template, request
import pyfile_web_scraping
import sentiment_analysis_youtube_comments
import mail_sending_to_user_with_attached_csv_files
import delete_files_after_mail
import pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/scrap', methods=['POST'])
def scrap_comments():
    try:
        url = request.form.get('youtube url')
        emailto = request.form.get('user mail id')

        file_and_detail = pyfile_web_scraping.scrapfyt(url)
        sentiment = sentiment_analysis_youtube_comments.sepposnegcom("Full Comments.csv")
        mail_sending_to_user_with_attached_csv_files.mailsend(emailto)

        list_file_and_detail = list(file_and_detail)
        list_sentiment = list(sentiment)
        print(list_file_and_detail)
        video_title, video_owner, video_comment_with_replies, video_comment_without_replies = list_file_and_detail[1:]
        pos_comments_csv, neg_comments_csv, video_positive_comments, video_negative_comments = list_sentiment

        # Check if positive and negative CSV files exist
        if os.path.exists('Positive Comments.csv'):
            pos_comments_csv = pd.read_csv('Positive Comments.csv')['Comment'].tolist()
        if os.path.exists('Negative Comments.csv'):
            neg_comments_csv = pd.read_csv('Negative Comments.csv')['Comment'].tolist()

        delete_files_after_mail.file_delete()

        after_complete_message = "Your file is ready and sent to your mail id"

        return render_template("index.html", after_complete_message=after_complete_message,
                               title=video_title, owner=video_owner, comment_w_replies=video_comment_with_replies,
                               comment_wo_replies=video_comment_without_replies,
                               positive_comment=video_positive_comments, negative_comment=video_negative_comments,
                               pos_comments=pos_comments_csv, neg_comments=neg_comments_csv)
    except Exception as e:
        # Log the error message
        print(f"An error occurred: {e}")
        # Return an error page or message to the user
        return render_template("error.html", error_message=str(e))

if __name__ == "__main__":
    app.run()
