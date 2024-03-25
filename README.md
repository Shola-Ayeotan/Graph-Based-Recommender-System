
# Graph-Based Recommendation System for an eCommerce Platform

## Overview
This project developed a Graph-based recommendation system for an eCommerce platform, leveraging user purchase and search history to recommend products. By transforming user interaction data into graph embeddings and using ANN-FAISS model, the system aimed to enhance product discoverability and user experience.

## Data Overview
The dataset comprised user interactions on the eCommerce website, spanning 9 attributes. This was ransformed into a graph format for analysis and modeling.

## Technology Stack
- **Programming Language:** Python
- **Libraries:** pandas, DuckDB, numpy, pecanpy, gensim, plotly, UMAP, ANN, FAISS
- **File Management:** Parquet files for efficient data storage
- **Database Management:** SQL for data querying

## Approach

### 1. Problem Understanding
Researched the requirements for creating a recommendation system that uses graph theory to suggest products based on historical user data.

### 2. Data Preparation
Extracted relevant data from the provided dataset and optimised it for the analysis.

### 3. Deepwalk and Node2vec Model Training
- **Libraries Used:** pandas, numpy, pecanpy, gensim
- **Main Steps:**
  - Performed graph random walks to generate sequences for embeddings.
  - Trained the Deepwalk and Node2Vec models using the gensim library.

### 4. Result Analysis and Visualization
- **Libraries Used:** pandas, numpy, umap, plotly
- **Main Steps:**
  - Categorized products into hierarchical levels for detailed analysis.
  - Applied UMAP for dimensionality reduction of embeddings to visualize data clusters.
  - Used Plotly for interactive 2D and 3D visualization of product clusters.

### 5. Embedding Vector Search with FAISS
- **Libraries Used:** FAISS, pandas, numpy
- **Main Steps:**
  - Initialized the FAISS library for efficient similarity search.
  - Used FAISS to find similar products based on embedding proximity.
  - Generated product recommendations for users based on similarity scores.

## Folder Structure
- **Model:** Stores the trained Deepwalk and Node2Vec models.
- **Notebooks:** Contains Jupyter notebooks used in the project:
  1. Data Optimisation
  2. Data Exploration and Data Analysis
  3. Deepwalk and Node2Vec Model Training
  4. Graph Construction
  5. Result Analysis
  6. Embedding Vector Search and Recommendation with FAISS
- **Scripts:** Python scripts are available for reproducibility and automation.
- **requirements.txt:** Lists all necessary libraries with versions. Install these requirements to ensure compatibility.

## Installation
To set up the environment for this project, install the dependencies listed in `requirements.txt` using the following command:
```sh
pip install -r requirements.txt
```

## Usage
Navigate through the notebooks in the provided order to understand the workflow. Each notebook is self-contained with comments and instructions for ease of use.

## Acknowledgments
- The pecanpy and gensim libraries for providing efficient implementations of node embeddings.
- The FAISS library by Facebook AI for enabling high-performance similarity search.
- The UMAP library for intuitive dimensionality reduction and data visualization techniques.
