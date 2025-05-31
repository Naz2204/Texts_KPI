from text_preparation import text_preparation
import numpy as np
import joblib

def cluster_documents_and_generate_tags_lda(documents: list[str], num_clusters: int = 5, num_tags_per_cluster: int = 4):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import LatentDirichletAllocation as LDA

    prepared_documents = [text_preparation(doc) for doc in documents]

    # max_df та min_df допомагають відфільтрувати занадто часті/рідкісні слова
    tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_df=0.95, min_df=2)
    tfidf_data = tfidf_vectorizer.fit_transform(prepared_documents)

    lda_model = LDA(n_components=num_clusters, n_jobs=-1, random_state=42)
    lda_model.fit(tfidf_data)

    words = tfidf_vectorizer.get_feature_names_out()
    cluster_tags = {}
    for topic_idx, topic_weights in enumerate(lda_model.components_):
        top_words_indices = topic_weights.argsort()[:-num_tags_per_cluster - 1:-1]
        tags = [words[i] for i in top_words_indices]
        cluster_tags[topic_idx] = tags

    doc_topic_distribution = lda_model.transform(tfidf_data)
    doc_clusters = np.argmax(doc_topic_distribution, axis=1).tolist()

    results_to_save = {
        "lda_model": lda_model,
        "vectorizer": tfidf_vectorizer,
        "cluster_tags": cluster_tags,
        "num_clusters": num_clusters,
        "num_tags_per_cluster": num_tags_per_cluster
    }
    try:
        joblib.dump(results_to_save, "../models/clusterize_and_autotag.joblib")
        print(f"Trained clusterizer was successfully written to file clusterize_and_autotag.joblib")
    except Exception as e:
        print(f"Error while saving a clusterizer: {e}")

    return cluster_tags, doc_clusters


def assign_new_document_lda(text: str):

    prepared_new_doc = text_preparation(text)

    try:
        model = joblib.load("../models/clusterize_and_autotag.joblib")
        print("LDA model was successfully loaded")
    except Exception as e:
        print(f"Unable to load LDA model {e}")
        return "Unable to assign tags"

    new_doc_vector = model["vectorizer"].transform([prepared_new_doc])

    topic_distribution = model["lda_model"].transform(new_doc_vector)
    predicted_cluster = np.argmax(topic_distribution[0])
    print(f"Розподіл за темами LDA: {topic_distribution[0]}")
    print(f"Передбачений LDA кластер: {predicted_cluster}")

    assigned_tags = model["cluster_tags"].get(predicted_cluster, ["Unknown tags"])

    return predicted_cluster, assigned_tags

