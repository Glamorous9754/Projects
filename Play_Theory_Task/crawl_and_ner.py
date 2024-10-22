import itertools
import threading
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import json
import gzip
import sys
import pandas as pd
from datasets import Dataset
from transformers import pipeline
import torch
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# Function to display a spinner during the crawling process.
def spinning_cursor():
    """Generates a spinning cursor animation."""
    while True:
        for cursor in '|/-\\':
            yield cursor

# Spinner in a separate thread while crawling.
def spinner_task():
    """Runs a spinner animation while pages are being crawled."""
    spinner = spinning_cursor()
    while not crawl_done:
        sys.stdout.write(f'\rCrawling Page {page_number}... {next(spinner)}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write(f'\rCrawling completed! Total pages crawled: {page_number}\n')

# Function to fetch articles from a specific page.
def fetch_articles_from_page(url):
    """Fetches articles from a given URL and extracts relevant data."""
    articles = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for article in soup.find_all('li', class_='wp-block-post'):
        headline_elem = article.find('a', class_='loop-card__title-link')
        excerpt_elem = article.find('div', class_='loop-card__content')
        author_elem = article.find('a', class_='loop-card__author')
        date_elem = article.find('time')
        url_elem = headline_elem['href'] if headline_elem else None

        if headline_elem and excerpt_elem and author_elem and date_elem:
            headline = headline_elem.get_text(strip=True)
            excerpt = excerpt_elem.get_text(strip=True)
            author = author_elem.get_text(strip=True)
            date = date_elem['datetime']

            article_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')

            if article_date >= date_threshold:
                articles.append({
                    'date': date,
                    'headline': headline,
                    'excerpt': excerpt,
                    'author': author,
                    'url': url_elem
                })
            else:
                return articles, False
    return articles, True

# Function to crawl articles for the last year with spinner and page count.
def crawl_techcrunch_articles_one_year():
    """Crawls TechCrunch articles from the past year with spinner animation."""
    global page_number, crawl_done
    base_url = 'https://techcrunch.com/latest/'
    articles = []
    next_url = base_url
    continue_crawling = True
    page_number = 1
    crawl_done = False

    spinner_thread = threading.Thread(target=spinner_task)
    spinner_thread.start()

    while continue_crawling:
        page_articles, continue_crawling = fetch_articles_from_page(next_url)
        articles.extend(page_articles)

        if continue_crawling:
            response = requests.get(next_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            next_button = soup.find('a', class_='wp-block-query-pagination-next')
            if next_button:
                next_url = next_button['href']
            else:
                break

        page_number += 1

    crawl_done = True
    spinner_thread.join()

    return articles

# Date threshold for articles from the last year
date_threshold = datetime.now(timezone.utc) - timedelta(days=365)

# Start the crawling process
start_time_crawl = time.time()

articles = crawl_techcrunch_articles_one_year()

end_time_crawl = time.time()

# Save crawled articles in a gzipped JSON file
output_file = 'techcrunch_articles_last_year.json.gz'
with gzip.open(output_file, 'wt', encoding='utf-8') as f:
    json.dump(articles, f, indent=4)

print(f'Successfully crawled {len(articles)} articles and saved to {output_file}')
print(f'Crawling time: {end_time_crawl - start_time_crawl:.2f} seconds')

# Convert the articles to a DataFrame and then to a Dataset object
df = pd.DataFrame(articles)
dataset = Dataset.from_pandas(df)

# Function to extract Named Entities using NER pipeline.
def extract_ner_batch(batch):
    """Processes NER extraction in batches for headlines."""
    headlines = batch['headline']
    ner_results = ner_pipeline(headlines, batch_size=8)

    extracted_entities = []
    for idx, result in enumerate(ner_results):
        # Collect entities and types
        entities = [{"entity": ent["word"], "type": ent["entity_group"]} for ent in result]
        # Format each headline with entities
        extracted_entities.append({
            "headline": batch['headline'][idx],
            "entities": entities
        })

    return {'extracted_entities': extracted_entities}

# Check for GPU availability and set device accordingly
device = 0 if torch.cuda.is_available() else -1

# Initialize the NER pipeline
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english",
                        aggregation_strategy="simple", device=device)

# Start the NER extraction process
start_time_ner = time.time()

# Apply NER extraction on the dataset using batch processing
ner_dataset = dataset.map(extract_ner_batch, batched=True, batch_size=8)

end_time_ner = time.time()

# Flatten the NER extracted entities and save to a JSON file
extracted_data = []
for item in ner_dataset["extracted_entities"]:
    extracted_data.extend(item)

output_file_ner = 'headline_ner_extracted.json'
with open(output_file_ner, 'w', encoding='utf-8') as f:
    json.dump(extracted_data, f, indent=4)

print(f'Successfully extracted NER and saved to {output_file_ner}')
print(f'NER extraction time: {end_time_ner - start_time_ner:.2f} seconds')

# Total time taken for crawling and NER extraction
total_time = (end_time_crawl - start_time_crawl) + (end_time_ner - start_time_ner)
print(f'Total processing time: {total_time:.2f} seconds')
