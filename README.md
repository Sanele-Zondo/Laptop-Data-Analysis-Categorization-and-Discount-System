# Laptop Data Analysis and Categorization Project

## Table of Contents
1. [Introduction](#introduction)
2. [Data Collection](#data-collection)
3. [Data Cleaning and Exploration](#data-cleaning-and-exploration)
4. [Feature Engineering](#feature-engineering)
5. [Applying Discounts](#applying-discounts)
6. [Model Building](#model-building)
7. [Data Visualization](#data-visualization)
8. [Data Storage](#data-storage)
9. [Challenges and Solutions](#challenges-and-solutions)

---

## 1. Introduction

### Project Overview
This project involves scraping laptop data from a website, cleaning and transforming it, categorizing laptops into work, gaming, and education categories, applying discounts based on certain criteria, and building a model to automate the categorization. The project concludes by visualizing the data and saving it into an SQL database for further analysis.

### Objective
The main objective is to automate the process of extracting, cleaning, categorizing, and analyzing laptop data, applying discounts where applicable, and visualizing insights. The data will then be stored in a structured format in an SQL database.

### Step-by-Step Guide
- Scrape the laptop data from the website
- Clean and preprocess the data (handle missing values, format data types)
- Extract relevant features and categories using regex
- Apply the machine learning model to categorize laptops
- Build a discounting system for each category (work, gaming, education)
- Visualize the categorized data and the price distribution with Matplotlib
- Push the cleaned and transformed data to SQL

### Tools

| Tool          | Purpose                                     |
|---------------|---------------------------------------------|
| Python        | Scraping, cleaning, model building, and visualization |
| BeautifulSoup | Web scraping and HTML parsing               |
| SQL           | Data storage and querying                   |
| Matplotlib    | Data visualization                          |
| Scikit-learn  | Building the categorization model           |

---

## 2. Data Collection

### Source
Data is scraped from an e-commerce website: [Webscraper Test Site](https://webscraper.io/test-sites), listing laptops with detailed specifications, prices, and other features.

---


## 3. Data Cleaning and Exploration

### Observations Before Cleaning and Transforming
- **Incomplete Specifications**: Some laptop data may have missing or incomplete specifications.
- **Product Descriptions**: Certain product descriptions may require regex extraction for proper categorization.
- **Outliers or Invalid Price Entries**: The price column may contain outliers or invalid entries that need to be addressed.

### Preprocessing Steps
### Loading and Viewing Data
1. **Import Libraries**:
   
   ```python
      import pandas as pd
      import numpy as np
      import re
      import psycopg2 as sql
      import matplotlib.pyplot as plt
      
      from sklearn.model_selection import train_test_split
      from sklearn.tree import DecisionTreeClassifier
      from sklearn.tree import plot_tree
      from sklearn.metrics import accuracy_score
   
2. **Loading Data**:
   ```python
   read_csv = pd.read_csv('data.csv')
   raw_data=pd.DataFrame(read_csv)

3. **Viewing Data**:
   ```python
   raw_data.head(10)


4. **Data Quality Checks**:

   1. **Number of rows and columns**
   
   ```python
     print(f'(Rows,Columns)-->{raw_data.shape}')

   2. **Data Checks**
   ```python
     raw_data.dtypes

   
   iii. ***Identify Missing Values***
   ```python
     raw_data.info()

   iv. ***Understand the distinct values in each column***
   ```python
     for i in raw_data.columns:
        print(f'{i}:{raw_data[i].nunique()}')
   
4. ***Correcting Errors***:
   -***Remove Whitespaces on column: Names***
   ```python
   raw_data['Names']=raw_data['Names'].str.strip()
   
   -***Fix Names that contains '...'***:
   ```python
     #Data containing '...'
  data_with_dots=raw_data[raw_data['Names'].str.contains('...',regex=False)]
  
  data_with_dots['Names']=data_with_dots['Descriptions'].str.split(',',expand=True)[0]
  #x=data_with_dots['Names'].str.contains('...',regex=False)
  #Data Not Containing '...'
  data_without_dots=raw_data[~raw_data['Names'].str.contains('...',regex=False)]
  #Combine Data
  raw_data=pd.concat([data_with_dots,data_without_dots],axis=0).sort_index(ascending=True)
  raw_data
   -***Remove dollar sign($) to help us with changing data type***:
   ```python
   raw_data['Prices']=raw_data['Prices'].str.replace('$','').str.strip()
  raw_data.rename(columns={'Prices':'Prices_$'},inplace=True)
  raw_data

5. **Remove Rows with Missing or Irrelevant Data**: 
   - Any rows with missing values or duplicate laptop entries were removed to ensure clean and accurate data.

6. **Standardize Columns**:
   i. ***Ensuring consistent values***
   ```python
     raw_data['Names']=raw_data['Names'].str.title()
   raw_data
   ii. *** Fix Data Types***
   ```python
     data_types={
      'Names': str
      ,'Prices_$':float
      ,'Descriptions':str
  }
  raw_data=raw_data.astype(data_types)
  print(raw_data.dtypes)

7. *Handle outliers
 ```python
  Q1= raw_data['Prices_$'].quantile(0.25)
  Q3= raw_data['Prices_$'].quantile(0.75)
  
  IQR= Q3-Q1
  lower_bound=Q1-1.5*IQR
  upper_bound=Q3+1.5*IQR
  upper_bound
  outliers=raw_data[(raw_data['Prices_$']<lower_bound)|(raw_data['Prices_$']>upper_bound)]
  outliers

### Regex Operations
- **Regular Expressions** were used to extract relevant details from the "Descriptions" column. The extracted details include:
  - **Screen_Size**
  - **Processor**
  - **Ram**
  - **Storage**
  - **Graphics_Card**
  - **Operating_System**

These extracted features were used for categorizing the laptops and applying further analysis.

---

## 4. Feature Engineering
*Details about feature extraction and engineering steps will be added here.*

---

## 5. Applying Discounts
*Details about the discounting system will be added here.*

---

## 6. Model Building
*Details about the categorization model and machine learning techniques used will be added here.*

---

## 7. Data Visualization
*Details about data visualization and insights will be added here.*

---

## 8. Data Storage
*Details about how data is stored in SQL and structured queries will be added here.*

---

## 9. Challenges and Solutions
*Details about challenges faced and solutions implemented during the project will be added here.*

