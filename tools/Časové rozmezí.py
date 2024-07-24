import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Define and display the bold, centered, and sized text
st.markdown(
    "<h1 style='text-align: center; font-weight: bold; font-size: 16px;'>Zpráva o průběhu provozu - Technická podpora aplikace NS-SIS II</h1>",
    unsafe_allow_html=True
)
st.write('**Statistiky NS-SIS II za období od 13.05.2024 do 19.05.2024.**')
st.write('**Počet zpracovaných Broadcasts**')
st.write('Hodnota v grafu odpovídá součtu zpracovaných Broadcast (tj. CUD z centra potvrzených ze strany NS) v součtu za hodinu')

# Generate some example data
np.random.seed(0)
dates = pd.date_range('2024-01-13', periods=200, freq='h')
data = np.random.poisson(lam=2000, size=200)
data[::20] = np.random.poisson(lam=15000, size=10)  # Simulate peaks

# Create a DataFrame
df = pd.DataFrame({'Date': dates, 'Value': data})

# User inputs for start and end date
st.write("### Vyberte časové rozmezí")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input('Začatek časového rozmezí', value=pd.to_datetime('2024-01-13'))
with col2:
    end_date = st.date_input('Konec časového rozmezí', value=pd.to_datetime('2024-01-21'))

start_datetime = pd.to_datetime(f"{start_date} 00:00:00")
end_datetime = pd.to_datetime(f"{end_date} 23:59:59")

# Filter the DataFrame based on the input range
df_filtered = df[(df['Date'] >= start_datetime) & (df['Date'] <= end_datetime)]

# Plot the filtered data using Plotly
fig = px.line(df_filtered, x='Date', y='Value', labels={'Date': 'Hodina provedení záznamu', 'Value': 'Počet zpracovaných Broadcasts'}, title='Počet zpracovaných Broadcasts v čase')
fig.update_layout(xaxis_tickformat='%d.%m.%Y %H:%M', xaxis_tickangle=-45)

# Show the plot in Streamlit
st.plotly_chart(fig)

st.write('**Graf 1 Produkční systém - počet zpracovaných Broadcasts**')
st.write('Celkově bylo za sledované období přijato a zpracováno 626 968, zaznamenané maximum je 16 240 Broadcasts za hodinu. Celkový počet Broadcasts s reportovanou chybou byl 670, tj. 0,11%.')
st.write('**Počet dotazů a nalezených záznamů produkčního prostředí.**')
st.write('Hodnoty v grafu ukazují počty dotazů (včetně rozpadu komplexních dotazů) v součtu za hodinu.')

