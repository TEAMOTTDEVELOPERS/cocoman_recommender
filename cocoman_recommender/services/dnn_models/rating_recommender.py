import keras
import tensorflow as tf
from keras.layers import Embedding
from keras.activations import sigmoid
from keras.losses import BinaryCrossentropy
from keras.optimizers import Adam

from cocoman_recommender.services.data.movielens import MovielensData


class CollaborativeFilteringModel(keras.Model):
    def __init__(self, num_users, num_movies, embedding_size, **kwargs):
        super(CollaborativeFilteringModel, self).__init__(**kwargs)
        self.user_embedding = Embedding(
            num_users,
            embedding_size,
            embeddings_initializer='he_normal',
            embeddings_regularizer=keras.regularizers.l2(1e-6),
        )
        self.user_bias = Embedding(num_users, 1)
        self.movie_embedding = Embedding(
            num_movies,
            embedding_size,
            embeddings_initializer='he_normal',
            embeddings_regularizer=keras.regularizers.l2(1e-6),
        )
        self.movie_bias = Embedding(num_movies, 1)

    def call(self, inputs, **kwargs):
        user_vec = self.user_embedding(inputs[:, 0])
        user_bias = self.user_bias(inputs[:, 0])
        movie_vec = self.movie_embedding(inputs[:, 1])
        movie_bias = self.movie_bias(inputs[:, 1])
        dot_prod = tf.tensordot(user_vec, movie_vec, 2)

        x = dot_prod + user_bias + movie_bias

        return sigmoid(x)


class RatingRecommender:
    def __int__(self):
        self.model = None

    def compile(self, num_users, num_movies, embedding_size):
        model = CollaborativeFilteringModel(num_users, num_movies, embedding_size)
        model.compile(
            loss=BinaryCrossentropy(),
            optimizer=Adam(lr=0.001),
        )
        self.model = model

    def train(self, x_train, y_train, x_val, y_val):
        return self.model.fit(
            x=x_train,
            y=y_train,
            batch_size=64,
            epochs=5,
            verbose=1,
            validation_data=(x_val, y_val),
        )


if __name__ == "__main__":
    movielens = MovielensData()

    x_train, x_val, y_train, y_val = movielens.load_train_data()

    model = RatingRecommender()
    model.compile(movielens.num_users, movielens.num_movies, 50)
    model.train(x_train, y_train, x_val, y_val)

    movielens.predict('20', model.model, 20)
