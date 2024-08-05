import phase2_phase3 as news
import streamlit as st
import sqlite3
import pandas as pd
import subprocess
import os
import newsspider101 as ns
from pathlib import Path
from transformers import TFAutoModelForSeq2SeqLM, AutoTokenizer
import io

menu = ["HOME", "SEARCH"]
choice = st.sidebar.selectbox("Menu", menu)

st.sidebar.title("About")
st.sidebar.info(
    """
     This app informs users about the hottest trending topics in their country and provides sentiment analysis and concise summaries.Users can access the original articles as well.
    GitHub: [What'sTheHotTopicInTown?](https://github.com/kelvin-ahiakpor/Whats.The.Hot.Topic.In.Town)
    """
)

if choice ==  "HOME":
    # Main title
    st.title("Welcome to TrendWatch!")

    # Catchy writeup
    st.markdown("""
    ### Experience The Future of News! 
    Your go-to app for discovering the hottest trending topics in your country. Our cutting-edge technology ensures you’re always in the loop with what’s happening around you.

    **Why Choose TrendWatch?**

    - **Instant Updates**: Get the latest trending topics as they happen, scraped in real-time using the powerful Scrapy library.
    - **Deep Insights**: Understand the public mood with our advanced sentiment analysis powered by the state-of-the-art Distill-BERT model.
    - **Quick Reads**: No time to read long articles? Our Bert2BertMK model generates concise summaries, so you get the gist in no time.
    - **Stay Informed**: Dive deeper into topics that interest you with direct links to the full articles.

    **Stay Ahead of The Curve**

    With TrendWatch, you’ll never miss out on the trends that matter. Whether it’s breaking news, viral topics, or the latest buzz, we’ve got you covered. Our sleek and user-friendly interface ensures you get all the information you need at a glance.

    Stay up to date, more details on our community will be provided soon.
    """)

    # Contact information
    st.markdown("""
    **Contact Us:**
    - Emmanuel Acquaye: [emmanuel.acquaye@ashesi.edu.gh](mailto:emmanuel.acquaye@ashesi.edu.gh)
    - Kelvin Ahiakpor: [kelvin.ahiakpor@ashesi.edu.gh](mailto:kelvin.ahiakpor@ashesi.edu.gh)
    - **Student IDs**: 10112026, 47822026
    - **GitHub**: [WHAT'S THE HOT TOPIC IN TOWN?](https://github.com/kelvin-ahiakpor/Whats.The.Hot.Topic.In.Town)
    """)

    # Start Searching Now button
    if st.button('Start Searching Now'):
        st.session_state.page = 'search'
        
if choice == "SEARCH":
    import re

    def reassemble_file(chunk_prefix, output_file_path, input_dir='model'):
        chunk_files = sorted([f for f in os.listdir(input_dir) if f.startswith(chunk_prefix)])
        with open(output_file_path, 'wb') as output_file:
            for chunk_file_name in chunk_files:
                with open(os.path.join(input_dir, chunk_file_name), 'rb') as chunk_file:
                    output_file.write(chunk_file.read())

    # Function to load the model from the combined bytes
    def load_model():
        output_file_path = './bert2bertMK/model.safetensors'  # Path for the reassembled model
        chunk_prefix = 'model.safetensors_chunk_'
        reassemble_file(chunk_prefix, output_file_path, input_dir='./bert2bertMK/model')
    
        # Load the model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained('./bert2bertMK')
        model = TFAutoModelForSeq2SeqLM.from_pretrained('./bert2bertMK')
    
        return model, tokenizer


    # Example usage
    output_file_path = './bert2bertMK/reassembled_model.safetensors'  # Path for the reassembled model
    chunk_prefix = 'model.safetensors_chunk_'


    # Main title
    st.title("Search for Trending Topics")


    # Additional functionalities can be added here

    # Run this app with `streamlit run search.py`

    with st.expander("HOW TO USE?"):
        st.markdown(
            """
            **INSTRUCTIONS:**
            - Type in the African Country Of choice and click the Get Trending News Button.
            - The topics are then displayed to you with their summaries and sentiments
            
            **Contact Information:**
            - Email: emmanuel.acquaye@ashesi.edu.gh, kelvin.ahiakpor@ashesi.edu.gh
            - Student ID: 10112026,
            
            - GitHub: [WHAT'S THE HOT TRENDING TOPIC IN TOWN](https://github.com/kelvin-ahiakpor/Whats.The.Hot.Topic.In.Town)
            """
        )

    top_articles = None

    def run_scrapy_script(country):
        '''result = subprocess.run(["python", "Hot.Topic.In.Town/RunSpider.py", country], capture_output=True, text=True)
        return result.stdout'''
        spider = ns.TrendsNewsSpider(country=country)
        spider.start_requests()
        spider.closed()
    


    st.subheader("FIND THE TOP TRENDS OF AFRICAN COUNTRIES")
    country = st.text_input("Enter Country For News")
    scrape_button = st.button("Get Trending News")

    if scrape_button and country:
        output = run_scrapy_script(country)
        st.success("Scraping completed!")
        

        conn = sqlite3.connect('newsData.db')
        newsdata = news.load_and_clean_data(conn)
        top_terms = news.get_top_terms(newsdata)
        top_articles = news.calculate_relevance(newsdata, top_terms)
        model, tokenizer = load_model()

        # Function to summarize an article
        def summarize_article(article_text):
            inputs = tokenizer.encode("summarize: " + article_text, return_tensors="tf", max_length=512, truncation=True)
            summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, 
                                        early_stopping=True)
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True,do_sample=True)
            return summary

                
        if top_articles is not None and not top_articles.empty:
            st.subheader("TOP 10 TRENDING TOPICS")
            
            # Ensure that column name matches the dataframe
            article_titles = top_articles['TITLE'].tolist()
            #selected_article = st.radio("Select an article to analyze", article_titles)
            
            for i in range(len(article_titles)):
                st.subheader(str(i+1) + ". " + article_titles[i])
                article_content = top_articles[top_articles['TITLE'] == article_titles[i]]['BODY'].values[0]
                summary = summarize_article(article_content)
                st.write(summary)
                st.write()
                link = top_articles[top_articles['TITLE'] == article_titles[i]]['URL'].values[0]
                sentiment = news.analyze_sentiment(article_content)
                if sentiment =="POSITIVE":
                    st.write("Sentiment Analysis:  😊 ",sentiment)
                else:
                    st.write("Sentiment Analysis: 😡 ", sentiment)
                    
                st.write( "Link To Article: ", link)
                
