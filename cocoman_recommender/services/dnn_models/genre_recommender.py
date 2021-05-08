import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class GenreRecommender:
    def __init__(self, corpus):
        self.tf_vectorizer = TfidfVectorizer(min_df=1, sublinear_tf=True)
        self.vectors = self.tf_vectorizer.fit_transform(corpus)

    def recommend(self, query, top_k=20):
        query_vec = self.tf_vectorizer.transform([query])
        cosine_sim = cosine_similarity(self.vectors, query_vec).flatten()
        recommend_indices = np.argsort(cosine_sim, axis=0)[-top_k - 1: -1]
        return recommend_indices
