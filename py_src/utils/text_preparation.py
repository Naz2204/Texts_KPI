import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')

def to_lowercase(text: str) -> str:
    return text.lower()

def remove_punctuation(text: str) -> str:
    return text.translate(str.maketrans('','', string.punctuation))

def remove_whitespaces(text: str) -> str:
    return " ".join(text.split())

def remove_stop_words(text: str) -> list[str]:
    tokenized = word_tokenize(text)
    return [word for word in tokenized if word not in stopwords.words("english")]

def lemmatize(text: str) -> str:
    lemmatizer = WordNetLemmatizer()
    tokenized = word_tokenize(text)
    lemmatized = []

    for word in tokenized:
        lemmatized.append(lemmatizer.lemmatize(word))

    return " ".join(lemmatized)

def text_preparation(text: str):
    lowercased = to_lowercase(text)
    punctuation_removed = remove_punctuation(lowercased)
    whitespaces_removed = remove_whitespaces(punctuation_removed)
    stopwords_removed = remove_stop_words(whitespaces_removed)
    prepared_text = lemmatize(" ".join(stopwords_removed))
    return prepared_text