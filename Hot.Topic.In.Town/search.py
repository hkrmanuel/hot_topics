import phase2_phase3 as news
import streamlit as st
import sqlite3
import pandas as pd
import subprocess
import os
from pathlib import Path
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import io

def load_parts(prefix, src):
    src = Path(src)
    combined = b""
    parts = []

    # Iterate through all files in the source directory
    for file in src.glob(f"{prefix}*"):
        parts.append(file)
    
    # Sort parts by their numeric suffix
    parts.sort(key=lambda part: int(part.stem.split("_")[-1]))

    # Combine all parts into one byte object
    for part in parts:
        with open(part, "rb") as f:
            combined += f.read()

    return combined

# Function to load the model from the combined bytes
def load_model():
    combined_data = load_parts("model.safetensors_chunk_", "./bert2bertMK/model")
    
    # Assuming you need to load the model from the combined data
    # Replace this with your actual model loading code

    # Save the combined data to a temporary file
    temp_file = 'temp_model.safetensors'
    with open(temp_file, 'wb') as f:
        f.write(combined_data)

    # Load the model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained('./bert2bertMK')
    model = AutoModelForSeq2SeqLM.from_pretrained('./bert2bertMK')

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
        - Web Scraping: Efficiently gathers the latest trending topics using the Scrapy library.
        - Sentiment Analysis: Analyzes the sentiment of each topic using the advanced Distill-BERT model.
        - Summarization: Generates clear and concise summaries with the Bert2BertMK model.
        
        **Contact Information:**
        - Email: emmanuel.acquaye@ashesi.edu.gh, kelvin.ahiakpor@ashesi.edu.gh
        - Student ID: 10112026,
        
        - GitHub: [example](https://github.com/example)
        """
    )

top_articles = None

def run_scrapy_script(country):
    result = subprocess.run(["python", "newsspider\RunSpider.py", country], capture_output=True, text=True)
    return result.stdout


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
        inputs = tokenizer.encode("summarize: " + article_text, return_tensors="pt", max_length=512, truncation=True)
        summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, 
                                    early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True,do_sample=True)
        return summary

    '''# Streamlit UI
    st.title("Text Summarization")

    input_text = st.text_area("Enter text to summarize:")
    if st.button("Summarize"):
        if input_text:
            summary = summarize_article(input_text)
            st.write("Summary:")
            st.write(summary)
        else:
            st.write("Please enter some text.")'''
            
    if top_articles is not None and not top_articles.empty:
        st.subheader("TOP 10 ARTICLES")
        
        # Ensure that column name matches the dataframe
        article_titles = top_articles['TITLE'].tolist()
        selected_article = st.radio("Select an article to analyze", article_titles)
        
        if selected_article:
            # Display the selected article title
            st.write("Selected Article:", selected_article)
            
            # Get the content of the selected article
            article_content = top_articles[top_articles['TITLE'] == selected_article]['BODY'].values[0]
            
            # Analyze sentiment of the selected article content
            sentiment = news.analyze_sentiment(article_content)
            
            # Display the sentiment analysis result
            st.write("Sentiment Analysis:", sentiment)
            summary = summarize_article(article_content)
            
    else:
        st.write("No articles available to display.")
