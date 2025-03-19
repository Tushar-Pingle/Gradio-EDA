import gradio as gr
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Function to analyze the uploaded file
def analyze_file(file):
    """Reads the uploaded CSV/Excel file and returns key data quality insights."""

    # Read the uploaded file
    if file.name.endswith('.csv'):
        df = pd.read_csv(file.name)
    else:
        df = pd.read_excel(file.name)

    # Summary Statistics
    summary_stats = df.describe(include='all').T
    
    # Missing Values Count (Convert Series to DataFrame with Column Names)
    missing_values = pd.DataFrame({'Column Name': df.columns, 'Missing Count': df.isnull().sum().values})

    # Duplicate Records Count
    duplicate_count = int(df.duplicated().sum())  # Ensure it's an int, not NumPy type

    # Data Types (Convert Series to DataFrame with Column Names)
    data_types = pd.DataFrame({'Column Name': df.columns, 'Data Type': df.dtypes.values})

    # Select only numeric columns for correlation matrix
    numeric_df = df.select_dtypes(include=['number'])
    correlation_matrix = numeric_df.corr()

    # Generate Correlation Heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix")
    corr_plot_path = "correlation_matrix.png"
    plt.savefig(corr_plot_path)
    plt.close()

    # Return properly formatted values
    return summary_stats, missing_values, duplicate_count, data_types, correlation_matrix, corr_plot_path

# Create Gradio interface
iface = gr.Interface(
    fn=analyze_file,
    inputs=gr.File(label="Upload your CSV or Excel file"),
    outputs=[
        gr.Dataframe(label="Summary Statistics"),
        gr.Dataframe(label="Missing Values Count"),  # Now formatted as DataFrame with Column Names
        gr.Number(label="Duplicate Records Count"),  # Ensured it's an int
        gr.Dataframe(label="Data Types"),  # Now formatted as DataFrame with Column Names
        gr.Dataframe(label="Correlation Matrix"),
        gr.Image(label="Correlation Heatmap")
    ],
    title="Instant Data Quality Checker",
    description="Upload a CSV or Excel file to get instant insights on data quality. No coding required!"
)

# Launch Gradio app with share mode enabled
iface.launch(share=True)
