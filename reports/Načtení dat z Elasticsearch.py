import streamlit as st
import pandas as pd
import numpy as np
np.float_ = np.float64
import matplotlib.pyplot as plt
from elasticsearch import Elasticsearch


# Connect to Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Function to retrieve data from Elasticsearch
def get_data_from_elasticsearch(index, query):
    response = es.search(index=index, body=query, size=1000)  # Increase size if needed
    hits = response['hits']['hits']
    data = [hit['_source'] for hit in hits]
    return pd.DataFrame(data)

option = st.selectbox(
    "Zvolte typ statistiky",
    ("Počet zpracovaných Broadcasts", "Počet dotazů a nalezených zaznamů produkčního prostředí", "Statistika otisků")
)

st.write("Statistika:", option)

if option == "Počet zpracovaných Broadcasts":
    # Define your Elasticsearch query
    query = {
        "query": {
            "match_all": {}
        }
    }
    index = "broadcasts_index"  # Adjust the index name as needed

    # Retrieve data
    df = get_data_from_elasticsearch(index, query)
    # Assuming df has columns 'x' and 'y1'
    fig, ax = plt.subplots()
    ax.plot(df['x'], df['y1'], label='Proměnná 1')
    ax.set_xlabel('Čas')
    ax.set_ylabel('Hondota [-]')
    ax.set_title('Graf první statistiky')
    ax.legend()
    plt.grid()
    st.pyplot(fig)

if option == "Počet dotazů a nalezených zaznamů produkčního prostředí":
    # Define your Elasticsearch query
    query = {
        "query": {
            "match_all": {}
        }
    }
    index = "queries_index"  # Adjust the index name as needed

    # Retrieve data
    df = get_data_from_elasticsearch(index, query)

    # Assuming df has columns 'x' and 'y2'
    fig, ax = plt.subplots()
    ax.plot(df['x'], df['y2'], label='Proměnná 2')
    ax.set_xlabel('Čas')
    ax.set_ylabel('Hondota [-]')
    ax.set_title('Graf druhé statistiky')
    ax.legend()
    plt.grid()
    st.pyplot(fig)



# Assume get_data_from_elasticsearch is defined and imports are correct

if option == "Statistika otisků":
    # Define your Elasticsearch query
    query = {
        "query": {
            "match_all": {}
        }
    }
    index = "prints_index"  # Adjust the index name as needed

    # Retrieve data
    df = get_data_from_elasticsearch(index, query)
    st.write(df)

    # Ensure the 'x' column is datetime type
    if not pd.api.types.is_datetime64_any_dtype(df['x']):
        df['x'] = pd.to_datetime(df['x'])

    # Extract dates and categories
    dates = df['x']
    categories = [
        '8023.02 Interně duplicitní prst',
        'Duplicitní otisk s již existujícím',
        '8022.02 Velmi nízká kvalita otisku',
        '8024.02 Nevalidní sejmutí otisku',
        'AFIS operace O.K.'
    ]

    # Extract data for the bar chart
    data = df[categories].values

    # Define colors
    colors = ['red', 'magenta', 'lime', 'orange', 'blue']

    # Create a stacked bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    # Bottom values for stacking
    bottom_values = np.zeros(len(dates))

    # Plot each category
    for i, category in enumerate(categories):
        ax.bar(dates, data[:, i], bottom=bottom_values, color=colors[i], label=category)
        bottom_values += data[:, i]

    # Add legend
    ax.legend(title='Výsledek vložení')

    # Add labels and title
    ax.set_xlabel('Den')
    ax.set_ylabel('Počet')
    ax.set_title('Národní otisky vkládané do CS')
    ax.grid(axis='y')
    # Rotate x-tick labels
    plt.xticks(rotation=45)

    # Display the plot
    plt.tight_layout()
    
    st.pyplot(fig)

    # Provide a dropdown to select the row to display as JSON
    selected_date = st.selectbox("Vyberte datum řádku, který bude zobrazen v JSON struktuře", df['x'].dt.strftime('%Y-%m-%d'))

    # Convert the selected row to JSON object
    selected_row = df[df['x'].dt.strftime('%Y-%m-%d') == selected_date]
    json_data = selected_row.to_dict(orient='records')

    # Display JSON object
    st.json(json_data)
