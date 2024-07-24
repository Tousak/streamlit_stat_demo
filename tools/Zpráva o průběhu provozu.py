from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Define and display the bold, centered, and sized text
st.markdown(
    "<h1 style='text-align: center; font-weight: bold; font-size: 16px;'>Zpráva o průběhu provozu - Technická podpora aplikace NS-SIS II</h1>",
    unsafe_allow_html=True
)
st.write('**Statistiky NS-SIS II za období od 13.05.2024 do 19.05.2024.**')

# Sections to show
sections = st.multiselect(
    'Zvolte jaké statistiky mají být zobrazeny',
    ['Počet zpracovaných Broadcasts', 'Počet dotazů a nalezených záznamů', 'Statistika otisků']
)

########################## BROADCAST #####################
if 'Počet zpracovaných Broadcasts' in sections:
    st.write('**Počet zpracovaných Broadcasts**')
    st.write('Hodnota v grafu odpovídá součtu zpracovaných Broadcast (tj. CUD z centra potvrzených ze strany NS) v součtu za hodinu')

    # Generate some example data
    np.random.seed(0)
    dates = pd.date_range('20240113', periods=200, freq='h')
    data = np.random.poisson(lam=2000, size=200)
    data[::20] = np.random.poisson(lam=15000, size=10)  # Simulate peaks

    # Create a DataFrame
    df = pd.DataFrame({'Date': dates, 'Value': data})

    # Plot the data
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df['Date'], df['Value'])
    ax.set_xticks(df['Date'][::10])
    ax.set_xticklabels(df['Date'][::10], rotation=45, ha='right')
    ax.grid(True)
    ax.set_xlabel('Hodina provedení záznamu')

    # Show the plot in Streamlit
    st.pyplot(fig)
    st.write('**Graf 1 Produkční systém - počet zpracovaných Broadcasts**')
    st.write('Celkově bylo za sledované období přijato a zpracováno 626 968, zaznamenané maximum je 16 240 Broadcasts za hodinu. Celkový počet Broadcasts s reportovanou chybou byl 670, tj. 0,11%.')

##################### Počet dotazů a nalezených záznamů #####################
if 'Počet dotazů a nalezených záznamů' in sections:
    st.write('**Počet dotazů a nalezených záznamů produkčního prostředí.**')
    st.write('Hodnoty v grafu ukazují počty dotazů (včetně rozpadu komplexních dotazů) v součtu za hodinu.')
    # Generate some example data
    np.random.seed(0)
    dates = pd.date_range('20240113', periods=200, freq='h')
    data = np.random.poisson(lam=2000, size=200)
    data[::20] = np.random.poisson(lam=15000, size=10)  # Simulate peaks
    data2 = data * 0.2
    # Create a DataFrame
    df2 = pd.DataFrame({'Date': dates, 'Value1': data, 'Value2': data2})

    # Plot the data
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df2['Date'], df2['Value1'], 'b', label='Počet dotazů')
    ax.plot(df2['Date'], df2['Value2'], 'r', label='Počet nalezených záznamů')
    ax.set_xticks(df2['Date'][::10])
    ax.set_xticklabels(df2['Date'][::10], rotation=45, ha='right')
    ax.grid(True)
    ax.set_xlabel('Hodina provedení záznamu')
    leg = ax.legend(loc="upper right")
    # Show the plot in Streamlit
    st.pyplot(fig)

    st.write('**Graf 2 Produkční systém - počet dotazů a nalezených záznamů**')
    st.write('Za sledované období bylo položeno 2 523 dotazů a nalezeno 5 525 záznamů.')
    st.write('Zaznamenané hodinové maximum je 152 položených dotazů ze dne 14.05.2024 09:00 hod.')
    st.write('Zaznamenané hodinové maximum je 717 nalezených záznamů ze dne 17.05.2024 14:00 hod')
    st.write('Počet dotazů, které měly odpověď ve formě chybového hlášení za uvedené období, byl 66, tj. 2,62%.')

############## Statistika otisků ###########################################
if 'Statistika otisků' in sections:
    st.write('**Statistika zpracování odeslaných národních požadavků s přiloženým otiskem do CS-AFIS za období od 13.05.2024 do 19.05.2024.**')
    st.write('**Do CS-AFIS bylo z rozhraní SIB odesláno celkem 337 požadavků s přiloženým otiskem.**')

    st.markdown("""
    **Z toho bylo:**
    - 277 operací provedeno bez chyb
    - 0 dočasně odložených operací v CS-AFIS
    - 0 otisků s nízkou kvalitou
    - 0 otisků, u kterých byla zjištěna duplicita prstu v rámci DKT
    - 0 otisků, u kterých byla zjištěno nevalidní sejmutí
    - 0 operací, při kterých byla překročena očekávaná maximální doba pro zpracování
    - 6 otisků, u kterých byla zjištěna duplicita s cizím záznamem
    - 0 s jinou chybou.
    """)

    # Generate random data
    np.random.seed(42)
    dates = pd.date_range(start='2024-05-13', end='2024-05-19')
    categories = ['AFIS operace O.K.', '8024.02 Nevalidní sejmutí otisku', 
                '8022.02 Velmi nízká kvalita otisku', 'Duplicitní otisk s již existujícím', 
                '8023.02 Interně duplicitní prst']

    data = {category: np.random.randint(0, 20, size=len(dates)) for category in categories}
    df = pd.DataFrame(data, index=dates)

    # Plot the data
    fig, ax = plt.subplots(figsize=(10, 6))

    bottom = np.zeros(len(dates))
    for category in categories:
        ax.bar(df.index, df[category], bottom=bottom, label=category)
        bottom += df[category]

    ax.set_title('Národní otisky vkládané do CS')
    ax.set_xlabel('Den')
    ax.set_ylabel('Počet')
    ax.legend(title='Výsledek vložení', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_xticks(df.index)
    ax.set_xticklabels(df.index.strftime('%d.%m.%Y'), rotation=45, ha='right')
    ax.grid(axis='y')

    # Show the plot in Streamlit
    st.pyplot(fig)
