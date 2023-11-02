from LeIA import SentimentIntensityAnalyzer

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