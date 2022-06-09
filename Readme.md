# Over 12 Thousand Movies search engine 

---
# What is recommendation system?

Recommender systems are the systems that are designed to recommend things to the user based on many different factors.  It finds out the match between user and item and imputes the similarities between users and items for recommendation

## Types of recommendation system
1) Collaborative Filtering
Collaborative filtering (CF) is one of the oldest recommendation techniques that match users with similar interests to personalized items, people, feed, etc. 
2) Content-based Filtering
The second most popular recommendation system, content-based filtering takes items bought as input data to recommend similar items. Recommendations are specific to every user under content-based filtering, therefore, can scale to a large user base

---
# Approach

- We have used two csv files one of which contains the data of Netflix and other contains TMDB data, In total we have data of **12,590 movies**. Both files are merged on the basis of their overview or description 
- Then we used TF-IDF(Term Frequency — Inverted Document Frequency) vectorizer from sklearn library

- The next step after calculating the TF-IDF matrix is to multiply the matrices. Multiplying matrices provides an interesting measure called the **Cosine Similarity**. The cosine similarity is a simple similarity measurement that ranges between 0 and 1. A value of 1 indicates identical elements and a value of 0 indicates completely different elements.

- Used **RapidFuzz** library to search movie name effectively
- Used TMDB api to fetch image poster using movie name
---
## FRONT-END
Front-end part is designed with Tkinter

![imageinfo](./Screenshot%202022-06-09%20235448.png)


!['Results'](./Screenshot%202022-06-09%20235645.png)

---
Thanks