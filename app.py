import streamlit as st
import pandas as pd
from recommender import data, user_item_matrix, item_similarity_df, recommend_movies

st.title('Movie Recommendation System')
st.write('Search for movies, rate them, and get personalized recommendations!')

# Get all movie titles
all_movies = sorted(user_item_matrix.columns.tolist())

# Let user search and select movies to rate
selected_movies = st.multiselect('Search and select movies you have watched:', all_movies)

user_ratings = {}
if selected_movies:
    st.write('Rate the selected movies (1-5):')
    for movie in selected_movies:
        rating = st.slider(f'Rating for "{movie}"', 1, 5, 3)
        user_ratings[movie] = rating

if st.button('Get Recommendations'):
    if not user_ratings:
        st.warning('Please select and rate at least one movie!')
    else:
        # Create a temporary user-item matrix with the user's ratings
        temp_user_item = user_item_matrix.copy()
        temp_user_id = -1  # Use a dummy user ID
        temp_user_item.loc[temp_user_id] = [user_ratings.get(m, None) for m in temp_user_item.columns]
        recommendations = recommend_movies(temp_user_id, temp_user_item, item_similarity_df, top_n=5, min_rating=1)
        if recommendations:
            st.subheader('Top 5 Movie Recommendations:')
            for i, title in enumerate(recommendations, 1):
                st.write(f'{i}. {title}')
        else:
            st.write('No recommendations available. Try rating more movies!') 