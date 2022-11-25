import spacy
nlp = spacy.load('en_core_web_lg')
import requests
from bs4 import BeautifulSoup
import pandas as pd
api = "AIzaSyBSxT_nl6cW9eCJARZVQVopGKF0vFyKpV0"

cse_id = "e7cd7f36cb1a04cf6"

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/Users/danny/Desktop/Jupyters/API things/Google API/natural-language.json'
from google.cloud import language_v1
client = language_v1.LanguageServiceClient()



#function takes a url as an argument and returns plain text. Will usually be passed to another function
#for more analysis
def get_home_page_text(site):

    stopwords = ['get','ourselves', 'hers','us','there','you','for','that','as','between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

    blacklist = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head', 
    'input',
    'script',
    'style',
    'input'
    ]
    ban_chars = ['|','/','&', "–"]

    url = site
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    page = requests.get(url,headers=headers)
    soup = BeautifulSoup(page.content, "html.parser").text
    news = soup.replace("\n", " ").replace("\t"," ")

    #output = news.split(" ")
    return news

#çonnects to google Natural Language API and performs sentiment analysis
#return a string fragment with a score and magnitude
def show_sentiment_scores(input_text):

    document = language_v1.Document(
        content=input_text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    #print("Text: {}".format(text))
    print(f'sentiment analysis for: {input_text}')
    print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))


#function that gives a dataframe with sentiment scores and magnitude as
#an output
def url_to_df(url):
    '''
    Creates a dataframe from a sentiment analysis compiled from each snetence on a page of content
    Columns returned are "Text","Score" and Magnitude
    '''

    stored = get_home_page_text(url)

    analysed_text = []
    sentiment_score = []
    sentiment_magnitude = []

    doc = nlp(stored)

    kept = []
    for sentence in doc.sents:
        kept.append(sentence.text)
    k=[]
    for i in kept:
        j = i.replace('   ','').replace("\n", " ")
        k.append(j)
    k

    for item in k:
        document = language_v1.Document(
        content=item, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment

        analysed_text.append(item)
        sentiment_score.append(sentiment.score)
        sentiment_magnitude.append(sentiment.magnitude)


    df = pd.DataFrame(list(zip(analysed_text,sentiment_score,sentiment_magnitude)),columns=["Text", "Score", "Magnitude"])
    return df

data = url_to_df("https://www.topchefknives.co.uk")
print(data)