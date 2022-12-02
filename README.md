# IMDB Movies: feature analysis & rating prediction

**Table of Content**
- [IMDB Movies: feature analysis \& rating prediction](#imdb-movies-feature-analysis--rating-prediction)
  - [Required Installations](#required-installations)
  - [Project Motivation](#project-motivation)
  - [Methodology](#methodology)
  - [Data Source](#data-source)
  - [File Description](#file-description)
  - [Medium Blog Post](#medium-blog-post)
  - [Reference](#reference)
  - [Licensing, Authors, Acknowledgements, etc.](#licensing-authors-acknowledgements-etc)

## Required Installations
 - NumPy
 - Pandas
 - [Scikit-learn 1.1.3](https://scikit-learn.org/stable/)
 - [Natural Language Toolkit (NLTK)](https://www.nltk.org/)
 - [Gensim (for LDA)](https://radimrehurek.com/gensim/index.html)
 - [Linux/Ubuntu or MacOS with g++ and Java (Autophrase required)](https://github.com/shangjingbo1226/AutoPhrase)
 - [BERT-based Sentence Transformers](https://www.sbert.net/docs/hugging_face.html)
 - [SHAP](https://shap.readthedocs.io/en/latest/)
 
No additional installations beyond the Anaconda distribution of Python and Jupyter notebooks.

## Project Motivation
Movies are like condiments in our life, we can live without them but it would be more enjoyable if we had them. Generally, there are over 3000 movies released over the world per year and the production company will be profitable if a movie gets popular. However, it is not easy to produce a popular movie. In the current movie market, the highest profit of a movie is around $2 billion while the lowest can go down to $0.1 million. Even though the average profit of a movie is around $14 million, there are still more than 70% of movies were losing money according to Entertainment Industry Economics(Vogel).  This implies that there is a huge room for movie production companies to improve the profit. What makes a movie have a high box office? The celebrities, director, or the production company? With the data of past movies, we are trying to identify the important features that build up a popular movie and predict the rating of the upcoming movie.

## Methodology
With the question in mind, we started to gather the information we need to solve the problem. `IMDB`, one of the largest online databases for the media industry, is our main data source for this project and `Wikipedia` as a supplement data for names of directors, actors, writers, and production companies. We defined movies with 10,000 votes and had a rating of 5.0+ as popular movies. 

For feature engineering, we not only tokenize orignal text for NLP processing (`TF-IDF` & `LDA`) but also use `AutoPhrase` Method to extract keywords from semantic perspectives. For baseline model, we select explicit factors like meaningful keywords and other detailed info about films, and we try adding more latent factors (like TF-IDF value, LDA Similarity and Doc2Vec) to improve our regressors' predictive performance.

Since popular movies are usually associated with high ratings and box-office, we decide to set ratings as our `y` and other possible important features(details in following) as `x`. We first use TF-IDF, LDA, and Doc2Vec to extract useful information as new features for the descriptive information we scrapped from Wikipedia. Then we fit them into OLS & Linear Regression as our baseline model to see how these important explicit factors influence the film rating. The next step is to compare and select models and feature sets. We choose the two lowest MSE & MAE as our final models and feature sets which are Gradient Boosting and Random Forest as regress, and  (Basis + LDA),(Basis + LDA+TF-IDF) as feature sets. The last step is to tune the models to generate the best parameters. After finding the optimal parameters for the models, we use SHAP values to illustrate the results of our finding.

## Data Source
There are two main Data Source, we need to scrap it from webpages:

1. [Most Popular Feature Films in IMDb](https://www.imdb.com/search/keyword/?ref_=kw_ref_rt_vt&mode=detail&page=1&title_type=movie&user_rating=3.0%2C&num_votes=10000%2C&sort=moviemeter,asc)
    - DataType: Rank-list Webpage data, different films have different webpage (hyperlink)
    - Sample size: 200+ pages, and 50 films on each page (totally 10,194 films)
    - Common Feature:
        - Tag: Feature Film
        - IMDb Rating Range: From 3.0 to 10.0
        - Number of Votes: >= 10,000
    - Scrapping Solution: Self-defined function to scrap detailed info for each film (by `BeautifulSoup`)
2. [Wikipedia](#https://www.wikipedia.org/)
    - Why use it?
        - Scrapping the text according to description for film's actor, director, writer etc. as extra knowledge
    - Scrapping Solution: Wiki api and `BeautifulSoup` to scrap the first part text by different entities

Then we merge wiki text data with film's detailed info together, and `film_with_allinfo.pkl` [partly cleaned for categorial and numeric vars] is the final output.

## File Description

**AutoPhrase**    

| - actor_text    
| |- AutoPhrase.txt    
| |- AutoPhrase_multi-words.txt    
| |- AutoPhrase_single-word.txt    
| |- segmentation.model    

| - director_text    
| |- AutoPhrase.txt    
| |- AutoPhrase_multi-words.txt    
| |- AutoPhrase_single-word.txt    
| |- segmentation.model     

| - production_text    
| |- AutoPhrase.txt    
| |- AutoPhrase_multi-words.txt    
| |- AutoPhrase_single-word.txt    
| |- segmentation.model     

| - writer_text    
| |- AutoPhrase.txt    
| |- AutoPhrase_multi-words.txt    
| |- AutoPhrase_single-word.txt    
| |- segmentation.model     

| - wiki_autophrase.csv# Extract all autophrase text from txt to csv    

**data**    

|- film_with_all_info.pkl # Original Data with Partial Clean    
|- baseline_feature.pkl # Feature Set Used for Baseline    
|- summary_lda_score.pkl # LDA Similarity Score    

**script**   

|- IMDb-scrapping-function.py # Web Scrapping Pipeline for IMDb     
|- Wiki_code.ipynb # Web Scrapping for Wikipedia     
|- cat&num_var_clean.py # Cleaning for Categorical & Numeric Vars     
|- Modelling.py # Whole Modelling Script     

**README.md**    

**540 Project Final Presentation.pdf**    

## Medium Blog Post
The blog post is still pending to post.

## Reference
1. Jingbo Shang, Jialu Liu, Meng Jiang, Xiang Ren, Clare R Voss, Jiawei Han, "Automated Phrase Mining from Massive Text Corpora", accepted by IEEE Transactions on Knowledge and Data Engineering, Feb. 2018.
2. Jialu Liu*, Jingbo Shang*, Chi Wang, Xiang Ren and Jiawei Han, "Mining Quality Phrases from Massive Text Corpora”, Proc. of 2015 ACM SIGMOD Int. Conf. on Management of Data (SIGMOD'15), Melbourne, Australia, May 2015. (* equally contributed, slides)
3. [Hugging-Face Sentence Transformer](https://huggingface.co/sentence-transformers/nli-roberta-large)
4. [Evaluate Topic Models: Latent Dirichlet Allocation (LDA) - Medium](https://towardsdatascience.com/evaluate-topic-model-in-python-latent-dirichlet-allocation-lda-7d57484bb5d0)
5. [Using LDA Topic Models as a Classification Model Input - Medium](https://towardsdatascience.com/unsupervised-nlp-topic-models-as-a-supervised-learning-input-cf8ee9e5cf28)
6. [Using SHAP Values to Explain How Your Machine Learning Model Works - Medium](https://towardsdatascience.com/using-shap-values-to-explain-how-your-machine-learning-model-works-732b3f40e137)

## Licensing, Authors, Acknowledgements, etc.

**Author:**
- Pengfei (Humphrey) Hu
- XiaoXuan (Nico) Lu
- Kexian (Carmen) Chen
- Junzhuo (Nero) Gu
- Siewying (Catherine) Gong

I acknowledge the transformer provided by `AutoPhrase` and `Sentences Transformer of Hugging-face`.