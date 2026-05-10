import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

class EngineeringPipeline:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.df_cleaned = None
        
        # Ensure output directory exists (Requirement IX)
        if not os.path.exists("outputs"):
            os.makedirs("outputs")

    # 1. Data Ingestion (Requirement IV)
    def load_data(self):
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"File not found: {self.file_path}")
            self.df = pd.read_csv(self.file_path)
            print(f"✅ Data Ingested: {self.df.shape[0]} rows loaded.")
            return True
        except Exception as e:
            print(f"❌ Ingestion Error: {e}")
            return False

    # 2. Data Cleaning & Unique Filter (Requirement III & V)
    def clean_and_filter(self):
        print("🛠️ Starting Data Pipeline: Cleaning & Filtering...")
        # Unique Filter Logic (Requirement III)
        # We filter for materials with Melting Point > 1500 to ensure a unique data slice
        self.df_cleaned = self.df[self.df['Melting Point (°C)'] > 1500].copy()
        
        # Automated Cleaning (Requirement V)
        self.df_cleaned.drop_duplicates(inplace=True)
        self.df_cleaned.dropna(inplace=True)
        
        print(f"✅ Cleaning Complete. Unique Records: {len(self.df_cleaned)}")
        self.df_cleaned.to_csv("data/dataset_cleaned.csv", index=False)

    # 3. Engineering Analytics with NumPy (Requirement IV & VI)
    def perform_analysis(self):
        print("📈 Computing Engineering Metrics...")
        # Using NumPy for mandatory statistics
        data = self.df_cleaned['Melting Point (°C)'].values
        
        stats = {
            "Mean": np.mean(data),
            "Median": np.median(data),
            "Std Dev": np.std(data),
            "Variance": np.var(data),
            "Max": np.max(data),
            "Min": np.min(data)
        }
        
        for k, v in stats.items():
            print(f"{k}: {v:.2f}")
        return stats

    # 4. Visualization & Animation (Requirement VII)
    def generate_outputs(self):
        print("🎨 Generating Static and Animated Visuals...")
        df = self.df_cleaned
        
        # --- STATIC PLOTS (3) ---
        # 1. Histogram (Distribution)
        plt.figure(figsize=(8, 5))
        sns.histplot(df['Melting Point (°C)'], kde=True, color='teal')
        plt.title('Engineering Distribution: Melting Point')
        plt.savefig('outputs/static_histogram.png')
        plt.close()

        # 2. Boxplot (Outliers)
        plt.figure(figsize=(8, 5))
        sns.boxplot(x=df['Melting Point (°C)'], color='orange')
        plt.title('Structural Stability Outlier Detection')
        plt.savefig('outputs/static_boxplot.png')
        plt.close()

        # 3. Scatter Plot (Correlation)
        plt.figure(figsize=(8, 5))
        sns.scatterplot(data=df, x='Density (g/cm³)', y='Thermal Conductivity (W/m·K)')
        plt.title('Property Correlation: Density vs Conductivity')
        plt.savefig('outputs/static_scatter.png')
        plt.close()

        # --- ANIMATED PLOTS (2) ---
        # 1. Animated Distribution (Changing Distribution)
        fig1 = px.histogram(df, x="Melting Point (°C)", animation_frame="Symmetry",
                           title="Phonon Stability: Distribution Shift by Symmetry")
        fig1.write_html("outputs/animated_distribution.html")

        # 2. Animated Time/Sequence Trend
        # Creating a dummy 'Time' sequence for the trend requirement
        df['Sequence'] = np.arange(len(df))
        fig2 = px.scatter(df, x="Sequence", y="Thermal Conductivity (W/m·K)", 
                         animation_frame="Symmetry", color="Symmetry",
                         title="Thermal Trend Analysis Over Material Sequence")
        fig2.write_html("outputs/animated_trend.html")
        
        print("✅ All outputs saved to /outputs folder.")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Initialize pipeline
    pipeline = EngineeringPipeline("data/dataset_original.csv")
    
    if pipeline.load_data():
        pipeline.clean_and_filter()
        pipeline.perform_analysis()
        pipeline.generate_outputs()
        print("\n🚀 PROJECT COMPLETE. Upload the /outputs folder and main.py to GitHub.")
        from PIL import Image

def save_as_gif(self):
    print("🎬 Converting frames to GIF...")
    frames = []
    # This assumes you have multiple images saved or you can loop through a variable
    # For a quick "Animated Trend" GIF, let's use your static plots as frames
    image_files = ['outputs/static_histogram.png', 'outputs/static_boxplot.png', 'outputs/static_scatter.png']
    
    for f in image_files:
        if os.path.exists(f):
            new_frame = Image.open(f)
            frames.append(new_frame)
    
    if frames:
        frames[0].save('outputs/animated_report.gif',
                       format='GIF',
                       append_images=frames[1:],
                       save_all=True,
                       duration=1000, # 1 second per frame
                       loop=0)
        print("✅ GIF created: outputs/animated_report.gif")