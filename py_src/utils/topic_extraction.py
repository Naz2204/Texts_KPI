import numpy as np
from text_preparation import text_preparation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA

# TODO користувач має мати можливість самостійно обрати кількість класів, яка буде згенерована
def find_topic(text: str, number_of_words: int = 4, number_of_topics: int = 1):

    prepared_text = text_preparation(text)
    tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_df=0.95, min_df=2)
    count_data = tfidf_vectorizer.fit_transform([prepared_text])

    lda = LDA(n_components=number_of_topics, n_jobs=-1)
    lda.fit(count_data)

    words = tfidf_vectorizer.get_feature_names_out()

    topics = [[words[i] for i in topic.argsort()[:-number_of_words - 1:-1]] for (topic_idx, topic) in
              enumerate(lda.components_)]
    topics = np.array(topics).ravel()

    return topics

if __name__ == '__main__':

    article = "Apple's latest smart watches can resume being sold in the US after the tech company filed an emergency appeal with authorities.\
    Sales of the Series 9 and Ultra 2 watches had been halted in the US over a patent row.\
    The US's trade body had barred imports and sales of Apple watches with technology for reading blood-oxygen level.\
    Device maker Masimo had accused Apple of poaching its staff and technology. \
    It comes after the White House declined to overturn a ban on sales and imports of the Series 9 and Ultra 2 watches which came into effect this week.\
    Apple had said it strongly disagrees with the ruling.\
    The iPhone maker made an emergency request to the US Court of Appeals, which proved successful in getting the ban lifted."

    print(find_topic(article))