import numpy as np
from .text_preparation import text_preparation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA

def find_topic(text: str, number_of_words: int = 4, number_of_topics: int = 1) -> list[str]:
    prepared_text = text_preparation(text)
    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    count_data = tfidf_vectorizer.fit_transform([prepared_text])

    lda = LDA(n_components=number_of_topics, n_jobs=-1)
    lda.fit(count_data)

    words = tfidf_vectorizer.get_feature_names_out()

    topics = [[words[i] for i in topic.argsort()[:-number_of_words - 1:-1]] for (topic_idx, topic) in
              enumerate(lda.components_)]
    topics = np.array(topics).ravel()

    return topics.tolist()