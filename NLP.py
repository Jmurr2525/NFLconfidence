import csv
from google.cloud import language_v1

# .... [Your web scraping code here] ...

def analyze_text(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    
    # Example: Extracting sentiment
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    
    # Example: Extracting entities
    entities = client.analyze_entities(document=document).entities
    
    # Return extracted data
    return sentiment, entities

def process_and_write_to_csv(scraped_texts, csv_filename):
    # Define CSV column names
    column_names = ['text', 'sentiment_score', 'sentiment_magnitude', 'entity_name', 'entity_type']
    
    # Open CSV file and writer
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=column_names)
        csv_writer.writeheader()
        
        # Iterate over scraped data
        for text in scraped_texts:
            sentiment, entities = analyze_text(text)
            
            # Example: Writing one row per entity
            for entity in entities:
                csv_writer.writerow({
                    'text': text,
                    'sentiment_score': sentiment.score,
                    'sentiment_magnitude': sentiment.magnitude,
                    'entity_name': entity.name,
                    'entity_type': language_v1.Entity.Type(entity.type_).name
                })

# Example usage
scraped_texts = "result1.txt" # List of text data obtained from web scraping
csv_filename = 'analyzed_data.csv'

process_and_write_to_csv(scraped_texts, csv_filename)
