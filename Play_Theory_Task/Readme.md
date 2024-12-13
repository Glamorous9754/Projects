# TechCrunch Article Crawler with NER Extraction

This script crawls TechCrunch articles from the past year, extracts Named Entities (NER) from the headlines, and saves the results to a file.

## Requirements

Ensure you have Python 3.x installed and use the `requirements.txt` file to install the necessary packages.

## Setup

1. Install the required packages:

```
pip install -r requirements.txt

```
2. Run the script:

```
python crawl_and_ner.py

```
## Output Files

* techcrunch_articles_last_year.json.gz: Compressed JSON file with the crawled articles.
* headline_ner_extracted.json: JSON file with extracted NER results from the headlines.

## Benchmark

The script will also output time taken for crawling and NER processing.
