import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time
from PIL import Image

class EngineeringPipeline:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.df_cleaned = None
        if not os.path.exists("outputs"):
            os.makedirs("outputs")

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

    def clean_and_filter(self):
        print("🛠️ Starting Data Pipeline: Cleaning & Filtering...")
        self.df_cleaned = self.df[self.df['Melting Point (°C)'] > 1500].copy()
        self.df_cleaned.drop_duplicates(inplace=True)
        self.df_cleaned.dropna(inplace=True)
        if not os.path.exists("data"): os.makedirs("data")
        self.df_cleaned.to_csv("data/dataset_cleaned.csv", index=False)
        print(f"✅ Cleaning Complete.")

    def perform_analysis(self):
        print("📈 Computing Engineering Metrics...")
        data = self.df_cleaned['Melting Point (°C)'].values
        return {"Mean": np.mean(data), "Median": np.median(data)}

    def generate_outputs(self):
        print("🎨 Converting HTML-style animations into GIF format...")
        df = self.df_cleaned
        
        # --- 1. GENERATE 3 REQUIRED STATIC CHARTS ---
        plt.figure(figsize=(8, 5))
        sns.histplot(df['Melting Point (°C)'], kde=True, color='teal')
        plt.title('Engineering Distribution: Melting Point')
        plt.savefig('outputs/static_histogram.png')
        plt.close()

        plt.figure(figsize=(8, 5))
        sns.boxplot(x=df['Melting Point (°C)'], color='orange')
        plt.title('Structural Stability Outlier Detection')
        plt.savefig('outputs/static_boxplot.png')
        plt.close()

        plt.figure(figsize=(8, 5))
        sns.scatterplot(data=df, x='Density (g/cm³)', y='Thermal Conductivity (W/m·K)')
        plt.title('Property Correlation: Density vs Conductivity')
        plt.savefig('outputs/static_scatter.png')
        plt.close()

        # --- 2. CREATE ANIMATED DISTRIBUTION GIF ---
        dist_frames = []
        for sym in df['Symmetry'].unique():
            subset = df[df['Symmetry'] == sym]
            plt.figure(figsize=(10, 6))
            sns.histplot(subset['Melting Point (°C)'], kde=True, color='teal')
            plt.title(f'Thermal Expansion Distribution (Symmetry: {sym})')
            plt.xlim(df['Melting Point (°C)'].min() - 100, df['Melting Point (°C)'].max() + 100)
            
            # FIX: Replace "/" in filename to prevent "Folder Not Found" error
            safe_name = str(sym).replace("/", "_")
            frame_path = f'outputs/temp_dist_{safe_name}.png'
            
            plt.savefig(frame_path)
            dist_frames.append(Image.open(frame_path))
            plt.close()

        dist_frames[0].save('outputs/animated_distribution.gif', save_all=True, 
                            append_images=dist_frames[1:], duration=800, loop=0)

        # --- 3. CREATE ANIMATED TREND GIF ---
        trend_frames = []
        df_sorted = df.sort_values('Melting Point (°C)') # Sort for smoother trend
        df_sorted['Sequence'] = np.arange(len(df_sorted))
        
        step = max(1, len(df_sorted) // 10)
        for i in range(step, len(df_sorted) + 1, step):
            subset = df_sorted.iloc[:i]
            plt.figure(figsize=(10, 6))
            plt.plot(subset['Sequence'], subset['Thermal Conductivity (W/m·K)'], marker='o', color='orange')
            plt.title('Thermal Trend Analysis (Convergence)')
            plt.xlim(0, len(df_sorted))
            plt.ylim(df['Thermal Conductivity (W/m·K)'].min(), df['Thermal Conductivity (W/m·K)'].max())
            
            frame_path = f'outputs/temp_trend_{i}.png'
            plt.savefig(frame_path)
            trend_frames.append(Image.open(frame_path))
            plt.close()

        trend_frames[0].save('outputs/animated_trend.gif', save_all=True, 
                             append_images=trend_frames[1:], duration=400, loop=0)

        # Cleanup temp frames
        for f in os.listdir('outputs'):
            if f.startswith('temp_'):
                os.remove(os.path.join('outputs', f))
        
        print("✅ Success! PNGs and GIFs created in /outputs.")

if __name__ == "__main__":
    pipeline = EngineeringPipeline("data/dataset_original.csv")
    if pipeline.load_data():
        pipeline.clean_and_filter()
        pipeline.perform_analysis()
        pipeline.generate_outputs()