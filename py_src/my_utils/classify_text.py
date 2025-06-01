import joblib
from .text_preparation import text_preparation
from pathlib import Path

_model_file_path = Path(__file__).parent.parent / 'models' / 'classifier.joblib'

def train_classifier() -> None:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.model_selection import cross_val_predict
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import Pipeline
    import json

    training_data_file_path = Path(__file__).parent.parent / 'training_data' / 'extracted_data.json'

    try:
        with open(training_data_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Unable to train model: {e}")
        return -1
    prepared_texts = [text_preparation(doc) for doc in data["texts"]]

    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.95, min_df=2)
    model = MultinomialNB()

    pipline = Pipeline([
        ("vectorizer", tfidf_vectorizer),
        ("model", model)
    ])

    pipline.fit(prepared_texts, data["labels"])

    # Навчання
    y_pred = cross_val_predict(pipline, prepared_texts, data["labels"], cv=3)

    try:
        joblib.dump(pipline, _model_file_path)
        print(f"Trained classifier was written to file classifier.joblib")
    except Exception as e:
        print(f"Error while saving classifier {e}")

    # # Результати
    # print("Accuracy:", accuracy_score(data["labels"], y_pred))
    # print("\nClassification Report:\n", classification_report(data["labels"], y_pred))


def classify(text: str) -> str:
    try:
        model = joblib.load(_model_file_path)
        print("Classifier loaded successfully")
    except Exception as e:
        print(f"Unable to load classifier {e}")
        return "Unable to load classifier"

    prepared_text = text_preparation(text)
    prediction = model.predict([prepared_text])
    return str(prediction[0])
