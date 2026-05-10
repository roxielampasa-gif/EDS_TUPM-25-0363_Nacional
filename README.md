# EDS Engineering Data Systems Pipeline 
**Project ID:** EDS_TUPM-25-0363  
**Academic Year:** 2026  
**Engineering Pillar:** Pillar 10 - Vibration & Noise Control / Materials Science  

## 📌 Project Overview
This repository contains a modular Python-based data analytics pipeline designed to ingest, clean, and analyze engineering datasets. The system is built using Object-Oriented Programming (OOP) principles and provides automated statistical analysis and visualizations in compliance with the 2026 Final Project requirements.

## 🛠️ System Architecture
The pipeline is structured into four primary phases:
1. **Data Ingestion:** Robust loading of CSV data with built-in error handling.
2. **Preprocessing:** Automated removal of null values and duplicates, plus a unique programmatic filter.
3. **Analytics:** Mathematical processing using NumPy to determine Mean, Variance, and Standard Deviation.
4. **Visualization:** Generation of 3 static plots (Matplotlib/Seaborn) and 2 animated plots (Plotly).

## 🚀 Getting Started

### Prerequisites
Ensure you have Python 3.14+ installed. You will need the following libraries:
```bash
pip install pandas numpy matplotlib seaborn plotly