from LeIA import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import panel as pn
import nltk
import spacy
from nltk.corpus import stopwords
nltk.download('stopwords')
nlp = spacy.load("pt_core_news_sm")

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)

    compound_score = sentiment_score['compound']
    
    if compound_score >= 0.05:
        return 'Positiva'
    elif compound_score <= -0.05:
        return 'Negativa'
    else:
        return 'Neutra'

def preprocess_sentence(text):
    doc = nlp(text)
    tokens = [token.text for token in doc if token.text.lower() not in stopwords.words('portuguese')]
    tokens = [token for token in tokens if token.isalpha()]    
    tokens = [token.lower() for token in tokens]  
    cleaned_text = ' '.join(tokens)
    return cleaned_text

def generate_wordcloud(all_avals, column):
    all_sentences = []
    for aval in all_avals:
        all_sentences.append(aval[column])
    all_sentences = [preprocess_sentence(sentence) for sentence in all_sentences]
    wordcloud_text = ' '.join(all_sentences)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(wordcloud_text)
    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    wordcloud_pane = pn.pane.Matplotlib(plt.gcf(), tight=True)
    return wordcloud_pane