import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load user ratings
ratings_path = 'data/ratings.csv'
ratings = pd.read_csv(ratings_path)

# Load movie titles
movies_path = 'data/movies.csv'
movies = pd.read_csv(movies_path, usecols=['movieId', 'title'])

# Merge ratings with movie titles
data = pd.merge(ratings, movies, on='movieId')

# Build user-item ratings matrix
user_item_matrix = data.pivot_table(index='userId', columns='title', values='rating')

# Compute item-item cosine similarity matrix
item_item_matrix = user_item_matrix.fillna(0).T  # Transpose: movies as rows
item_similarity = cosine_similarity(item_item_matrix)
item_similarity_df = pd.DataFrame(item_similarity, index=item_item_matrix.index, columns=item_item_matrix.index)

def recommend_movies(user_id, user_item_matrix, item_similarity_df, top_n=5, min_rating=4):
    # Get movies rated by the user
    user_ratings = user_item_matrix.loc[user_id].dropna()
    # Only consider movies the user rated >= min_rating
    user_ratings = user_ratings[user_ratings >= min_rating]
    if user_ratings.empty:
        return []
    # Store scores for candidate movies
    scores = pd.Series(dtype=float)
    for movie, rating in user_ratings.items():
        # Get similarity scores for this movie
        similar_scores = item_similarity_df[movie]
        # Weight by user's rating
        scores = scores.add(similar_scores * rating, fill_value=0)
    # Remove movies the user has already rated
    scores = scores.drop(user_ratings.index, errors='ignore')
    # Sort and return top N
    recommended = scores.sort_values(ascending=False).head(top_n)
    return recommended.index.tolist()

if __name__ == '__main__':
    print('Merged data preview:')
    print(data.head())
    print('\nUser-Item Ratings Matrix preview:')
    print(user_item_matrix.head())
    print('\nItem-Item Cosine Similarity Matrix preview:')
    print(item_similarity_df.iloc[:5, :5])
    # Demo: Recommend movies for user 1
    user_id = 1
    recommendations = recommend_movies(user_id, user_item_matrix, item_similarity_df, top_n=5)
    print(f'\nTop 5 movie recommendations for user {user_id}:')
    for i, title in enumerate(recommendations, 1):
        print(f'{i}. {title}') 