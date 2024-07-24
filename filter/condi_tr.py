import numpy as np
np.float_ = np.float64
import streamlit as st
import pandas as pd
from streamlit_condition_tree import condition_tree
from streamlit_condition_tree import condition_tree, config_from_dataframe


@st.cache_data
def load_data():
    df = pd.read_csv(
        'https://drive.google.com/uc?id=1phaHg9objxK2MwaZmSUZAKQ8kVqlgng4&export=download',
        index_col=0,
        parse_dates=['Date of birth'],
        date_format='%Y-%m-%d')
    df['Age'] = ((pd.Timestamp.today() - df['Date of birth']).dt.days / 365).astype(int)
    df['Sex'] = pd.Categorical(df['Sex'])
    df['Likes tomatoes'] = np.random.randint(2, size=df.shape[0]).astype(bool)
    return df

df = load_data()

st.write(df)

# Basic field configuration from dataframe
config = config_from_dataframe(df)

# Condition tree
query_string = condition_tree(
  config,
  always_show_buttons=True,
  placeholder="Vytvořte logiku rozhodovacího stromu"
)

# Filtered dataframe
df = df.query(query_string)
st.dataframe(df)
