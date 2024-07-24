import numpy as np
np.float_ = np.float64

from elasticsearch.helpers import bulk, BulkIndexError
from elasticsearch import Elasticsearch
import pandas as pd

# Connect to Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Function to delete an index
def delete_index(index):
    if es.indices.exists(index=index):
        es.indices.delete(index=index)
        print(f"Deleted index: {index}")

# Function to create test data
def create_test_data(index, num_records=100):
    x = np.arange(0, num_records)
    y1 = np.random.randn(num_records).cumsum()
    y2 = np.random.randn(num_records).cumsum()
    y3 = np.random.randn(num_records).cumsum()
    
    # Create a DataFrame
    df = pd.DataFrame({
        'x': x,
        'y1': y1,
        'y2': y2,
        'y3': y3
    })

    # Convert DataFrame to Elasticsearch bulk format
    records = df.to_dict(orient='records')
    actions = [
        {
            "_index": index,
            "_source": record
        }
        for record in records
    ]

    # Insert data into Elasticsearch with specified headers
    bulk(es, actions, headers={'Content-Type': 'application/json'})

# Function to create fixed length test data
def create_fixed_length_test_data(index):
    dates = ['13.5.2024', '14.5.2024', '16.5.2024', '17.5.2024', '18.5.2024', '19.5.2024']
    categories = [
        '8023.02 Interně duplicitní prst',
        'Duplicitní otisk s již existujícím',
        '8022.02 Velmi nízká kvalita otisku',
        '8024.02 Nevalidní sejmutí otisku',
        'AFIS operace O.K.'
    ]
    np.random.seed(42)
    data = np.random.randint(0, 50, size=(len(dates), len(categories)))

    # Convert data to a DataFrame
    records = []
    for i, date in enumerate(dates):
        record = {'x': date}
        for j, category in enumerate(categories):
            record[category] = data[i, j]
        records.append(record)

    df = pd.DataFrame(records)

    # Convert DataFrame to Elasticsearch bulk format
    actions = [
        {
            "_index": index,
            "_source": record
        }
        for record in df.to_dict(orient='records')
    ]

    # Insert data into Elasticsearch with specified headers
    bulk(es, actions, headers={'Content-Type': 'application/json'})

# Delete existing indices
delete_index('broadcasts_index')
delete_index('queries_index')
delete_index('prints_index')

# Create test data in three different indices
create_test_data('broadcasts_index')
create_test_data('queries_index')
create_fixed_length_test_data('prints_index')

print("Test data created in Elasticsearch")
