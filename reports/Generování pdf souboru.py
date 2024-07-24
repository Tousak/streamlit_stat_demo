from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_pdf(data, plot_path, pdf_path):
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []

    # Add title
    styles = getSampleStyleSheet()
    title = Paragraph("Sample PDF Report", styles['Title'])
    elements.append(title)

    # Add DataFrame content with borders
    table_data = [data.columns.tolist()] + data.values.tolist()
    table = Table(table_data)

    # Add table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)

    # Add plot image
    img = Image(plot_path, width=450, height=250)
    elements.append(img)

    doc.build(elements)

# Streamlit app
st.title("Test generování PDF souboru")

# Sample DataFrame
if "df" not in st.session_state:
    data = {
        'x': pd.date_range(start='2021-01-01', periods=10, freq='D'),
        'Category1': np.random.randint(0, 10, 10),
        'Category2': np.random.randint(0, 10, 10),
        'Category3': np.random.randint(0, 10, 10)
    }
    st.session_state.df = pd.DataFrame(data)

df = st.session_state.df

# Display DataFrame
st.write(df)

# Save the plot to a file and display it
plot_path = 'plot.png'

# Create a simple plot and save it locally
fig, ax = plt.subplots(figsize=(10, 5))  # Increase figure size
ax.plot(df['x'], df['Category1'], label='Category1')
ax.plot(df['x'], df['Category2'], label='Category2')
ax.plot(df['x'], df['Category3'], label='Category3')
ax.legend()
ax.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()  # Use tight layout to prevent overlap
plt.savefig(plot_path)

# Display the plot in Streamlit
st.pyplot(fig)

# Input for the PDF file name
pdf_file_name = st.text_input("Vložte jméno pdf souboru:", "report")

# Generate PDF
if st.button('Generujte PDF soubor'):
    # Generate the full PDF path with the user-specified name
    pdf_path = f'{pdf_file_name}.pdf'
    generate_pdf(df, plot_path, pdf_path)

    # Directly download the generated PDF
    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()
    
    # Clean up
    os.remove(plot_path)
    os.remove(pdf_path)

    # Trigger file download without showing another button
    st.download_button(label="Stáhněte PDF soubor", data=pdf_data, file_name=pdf_path, mime="application/pdf", key='download_button', on_click=lambda: st.session_state.pop('download_button', None))
