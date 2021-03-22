import numpy as np
import pandas as pd


class MovielensData:
    def __init__(self):
        self.data = None
        self.num_users = 0
        self.num_movies = 0
        self.load_data()

    def load_data(self):
        raw_rating_data = pd.read_csv('../../datasets/movielens/rating.csv')

        user_ids = raw_rating_data['userId'].unique().tolist()
        user2user_encoded = {x: i for i, x in enumerate(user_ids)}
        user_encoded2user = {i: x for i, x in enumerate(user_ids)}

        movie_ids = raw_rating_data['movieId'].unique().tolist()
        movie2moive_encoded = {x: i for i, x in enumerate(movie_ids)}
        movie_encoded2movie = {i: x for i, x in enumerate(movie_ids)}

        raw_rating_data['user'] = raw_rating_data['userId'].map(user2user_encoded)
        raw_rating_data['movie'] = raw_rating_data['movieId'].map(movie2moive_encoded)
        raw_rating_data['rating'] = raw_rating_data['rating'].values.astype(np.float32)

        self.data = raw_rating_data
        self.num_users = len(user2user_encoded)
        self.num_movies = len(movie_encoded2movie)

    def load_train_data(self):
        min_rating = min(self.data['rating'])
        max_rating = max(self.data['rating'])

        data = self.data.sample(frac=1, random_state=42)
        data_x = data[['user', 'movie']].values
        data_y = data['rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values

        train_indices = int(0.9 * data.shape[0])
        return data_x[:train_indices], data_x[train_indices:], data_y[:train_indices], data_y[train_indices:]

    @staticmethod
    def predict(user_id, model, top_k):
        raw_rating_data = pd.read_csv('../../datasets/movielens/rating.csv')
        raw_movie_data = pd.read_csv('../../datasets/movielens/movie.csv')

        user_ids = raw_rating_data['userId'].unique().tolist()
        user2user_encoded = {x: i for i, x in enumerate(user_ids)}
        user_encoded2user = {i: x for i, x in enumerate(user_ids)}

        movie_ids = raw_rating_data['movieId'].unique().tolist()
        movie2moive_encoded = {x: i for i, x in enumerate(movie_ids)}
        movie_encoded2movie = {i: x for i, x in enumerate(movie_ids)}

        movies_watched_by_user = raw_rating_data[raw_rating_data.userId == user_id]
        movies_not_watched = raw_movie_data[
            ~raw_movie_data['movieId'].isin(movies_watched_by_user.movieId.values)
        ]['movieId']
        movies_not_watched = list(
            set(movies_not_watched).intersection(set(movie2moive_encoded.keys()))
        )
        user_encoder = user2user_encoded.get(user_id)
        user_movie_array = np.hstack(
            ([[user_encoder]] * len(movies_not_watched), movies_not_watched)
        )
        top_ratings_indices = model.predict(user_movie_array).flatten().argsort()[-top_k:][::-1]
        recommended_movie_ids = [
            movie_encoded2movie.get(movies_not_watched[x][0]) for x in top_ratings_indices
        ]

        return raw_movie_data[raw_movie_data['movieId'].isin(recommended_movie_ids)]
