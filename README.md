# Laptop Data Analysis and Categorization Project
![image alt](https://github.com/Sanele-Zondo/data_projects/blob/136932d65b4741f69cfdb77aaa4eb52653ed4e39/cover.gif)
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

   
   3. ***Identify Missing Values***
      ```python
        raw_data.info()

   4. ***Understand the distinct values in each column***
      ```python
        for i in raw_data.columns:
        print(f'{i}:{raw_data[i].nunique()}')
   
5. **Correcting Errors**:
   
      i.**Remove Whitespaces on column: Names**:

   ```python
      raw_data['Names']=raw_data['Names'].str.strip()
      ```
   
      ii.**Fix Names that contains '...'**:
   ```python
        #Data containing '...'
        data_with_dots=raw_data[raw_data['Names'].str.contains('...',regex=False)]
        
        data_with_dots['Names']=data_with_dots['Descriptions'].str.split(',',expand=True)[0]
       
        #Data Not Containing '...'
         data_without_dots=raw_data[~raw_data['Names'].str.contains('...',regex=False)]
        #Combine Data
        raw_data=pd.concat([data_with_dots,data_without_dots],axis=0).sort_index(ascending=True)
        raw_data
      ```
      
      iii.**Remove dollar sign($) to help us with changing data type**:
   ```python
         raw_data['Prices']=raw_data['Prices'].str.replace('$','').str.strip()
         raw_data.rename(columns={'Prices':'Prices_$'},inplace=True)
         raw_data
      ```
7. **Remove rows with missing or irrelevant data**: 
     ```python
      raw_data.drop_duplicates(keep='first')
     ```
   
8. **Standardize Columns**:
      
      i. **Ensuring consistent values**
      ```python
            raw_data['Names']=raw_data['Names'].str.title()
            raw_data
      ```
      ii. **Fix Data Types**
      ```python
           data_types={
            'Names': str
            ,'Prices_$':float
            ,'Descriptions':str
           }
           raw_data=raw_data.astype(data_types)
           print(raw_data.dtypes)
      ```
   8. **Handle outliers**
       ```python
        Q1= raw_data['Prices_$'].quantile(0.25)
        Q3= raw_data['Prices_$'].quantile(0.75)
        
        IQR= Q3-Q1
        lower_bound=Q1-1.5*IQR
        upper_bound=Q3+1.5*IQR
        upper_bound
        outliers=raw_data[(raw_data['Prices_$']<lower_bound)|(raw_data['Prices_$']>upper_bound)]
        outliers
      ```
       ![image alt](https://github.com/Sanele-Zondo/data_projects/blob/45fbf7b35d014de32659f6b9658ff4dc3da42cad/outliers.png)
---
#### After Data Cleaning
   ![image alt]()
## 4. Feature Engineering
### Regex Operations
   - **Regular Expressions** were used to extract relevant details from the "Descriptions" column. The extracted details include:
     - **Screen_Size**
     - **Processor**
     - **Ram**
     - **Storage**
     - **Graphics_Card**
     - **Operating_System**
     ```python
        def search_text(text):
       pattern=re.compile(r'''
                           ([\d]*"[^,]*|[\d]+[\.][\d]+"[^,]*)
                           [\,\s]*
                          ([^,]+)
                          [\,\s]*
                          ([\d]{1,2}GB[^,]*)
                          [\,\s]*
                          ([\d]{2,}GB[^,]*|[\d]{1,2}TB[^,]*)
                          [\,\s]*
                          ([\d]*GB[^,]*|GTX[^,]*|Radeon[^,]*|NVIDIA[^,]*|GeForce[^,]*|Intel[^,]*)?
                          [\,\s]*
                          (DOS[^,]*?|Win[^,]*|Linux[^,]*?|Iris[^,]*?|Endless OS[^,]*?|No OS[^,]*?|FreeDOS[^,]*?)?'''
                          , re.VERBOSE
                         )
       match=pattern.search(text)
       if match:
           screen_size=match.group(1)
           processor=match.group(2)
           ram=match.group(3)
           storage=match.group(4)
           graphics_card=match.group(5)
           operating_system=match.group(6)
           data={
               'Screen_Size':screen_size
               ,'Processor':processor
               ,'Ram':ram
               ,'Storage':storage
               ,'Graphics_Card':graphics_card
               ,'Operating_System':operating_system
               
           }
       
           return data
       else:
           return None
           
      data_dictionary=raw_data['Descriptions'].apply(lambda x :search_text(x))
      
      #Convert Dictionary to DataFrame
      data=pd.DataFrame(data_dictionary.tolist())
      #Add The Columns To the Original Data
      data=pd.concat([raw_data,data],axis=1)
      #Replace Missing Values
      list_of_missing_values=['',None,np.nan]
      data=data.replace(list_of_missing_values,'Not Specified')
      #data[data['Descriptions']==None]
      #Select Necessary Columns
      data=data[['Names','Prices_$','Screen_Size','Processor','Ram','Storage','Graphics_Card','Operating_System','Ratings','Reviews']]
      data
   

   *These extracted features were used for categorizing the laptops and applying further analysis.
## 5. Categorize Data into Work, Gaming and Education:
   ```python
      def Graphics_Card_Checker(text):
          if text != 'Not Specified' and text !='3GB' and text !='4GB':
              return 'Yes'
          else:
              return 'No'
      def checker(price,Screen_Size,ram,graphics_card):
          try:
              if price <= 500 and ram<5 and Screen_Size <= 14:
                  return 'Education'
              elif price > 500 and ram >=8 and graphics_card !='Not Specified' and Screen_Size > 14:
                  return 'Gaming'
              else:
                  return 'Work'
          except Exception as e:
              print(f'Error:{e}')
              return 'Unknown'
         data['ram_checker']=data['Ram'].str.extract(r'(.*)(?=GB)',expand=False).astype(float) 
         data['price_checker']=data['Prices_$']
         #Extract the Screen Size as float
         data['screen_size_checker']=data['Screen_Size'].str.extract(r'(.*)(?=")',expand=False).astype(float)
         #Check if it has graphic card
         data['Graphics_Card_checker']=data['Graphics_Card'].apply(lambda x: Graphics_Card_Checker(x))
         
         #Categorize data
         data['Category']=data.apply(lambda x: checker(x['price_checker'],x['screen_size_checker'],x['ram_checker'],x['Graphics_Card']),axis=1)
         
         data_cleaned=data[['Names','Prices_$','Screen_Size','Processor','Ram','Storage','Graphics_Card','Operating_System','Ratings','Reviews','Category']]
         #Display Data
         data_cleaned
```
![image alt]()
## 6. Applying Discounts
*15% sales
```python
   laptops_clearance_sale=data_cleaned.query("Operating_System in ['Windows 8.1', 'Win7 Pro 64bit', 'Window 8.1 Pro']")
   sale=laptops_clearance_sale['Prices_$'].apply(lambda x: x-x*0.15)
   laptops_clearance_sale.insert(2,'Discounted_Price_$',round(sale,2))
   laptops_clearance_sale
```
*10% sales
```python
   laptops_sale=data_cleaned.query("Operating_System not in ['Windows 8.1', 'Win7 Pro 64bit', 'Window 8.1 Pro'] ")
   sale=laptops_sale['Prices_$'].apply(lambda x: x-x*0.10)
   laptops_sale.insert(2,'Discounted_Price_$',round(sale,2))
   laptops_sale
```
-Combine Data:
```python
   data_cleaned=pd.concat([laptops_clearance_sale,laptops_sale],ignore_index=True)
   data_cleaned
```
![image alt]()
---

## 7. Model Building
*Details about the categorization model and machine learning techniques used will be added here.*
```python
   #Prepare Data[Feature(X) and Target(y)]
   X=data_cleaned_model[['ram_checker','price_checker','screen_size_checker','Graphics_Card_checker']]
   y=data_cleaned_model['Category']
   
   #Split data into train and test:70-30 irrespectively
   X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,train_size=0.8,random_state=42)
   
   #Build a model
   tree=DecisionTreeClassifier()
   
   #Train Model
   tree.fit(X_train,y_train)
   
   #Make Predictions
   y_pred=tree.predict(X_test)
   
   #Evaluate The Model
   accuracy=accuracy_score(y_test,y_pred)
   print(f'Model Accuracy:\n{accuracy*100}%')
   #Visualize The Model
   plt.subplots(figsize=(15,10))
   plot_tree(tree,filled=True,feature_names=['ram_checker','price_checker','screen_size_checker','Graphics_Card_checker'],class_names=['Education','Work','Gaming'])
   plt.show()
```
![image alt]()
---

## 8. Data Visualization
*Details about data visualization and insights will be added here.*
```python
   group=data_cleaned.groupby('Ratings').agg({'Names':'count'})
   
   x=group.index.values #Category
   y=group.values.flatten()#Total in each Category
   
   #Create a Figure
   fig, ax = plt.subplots(2,2,figsize=(10,6))
   fig.suptitle('Dashboard',fontsize=15,fontweight=1)
   
   #Bar Plot
   color=['cornflowerblue','midnightblue','lavender','lightBlue']
   ax[0,0].barh(x,y,color=color,align='edge')
   #Labels
   ax[0,0].set_title('Distribution of Laptops Across Ratings', color='k',fontsize=None,loc='center')
   ax[0,0].set_ylabel('ratings',color='k',fontsize=8)
   ax[0,0].set_xlabel('Number Of Laptops',color='k',fontsize=8)
   lis=range(1,5,1)
   ax[0,0].set_yticks(lis, [x for x in lis])
   
   #Table
   ax[0,1].axis('Off')
   ax[0,1].table(colLabels=category_data.columns,cellText=category_data.values,loc='center',fontsize=15)
   ax[0,1].set_title('Prices Before vs Prices After Discount and Percentage Change',fontsize=8)
   
   #Pie
   xc=sum_by_col(data_cleaned,'Category','Prices_$')
   color=['lightblue','cornflowerblue','lavender']
   ax[1,0].pie(xc['Prices_$'],labels=xc.index,colors=color,autopct="%1.1f%%",startangle=270)
   #Labes
   ax[1,0].set_title("Price Distribution across Categories",color='k',fontsize=10)
   
   #Box And Whisckers
   ax[1,1].boxplot(data_cleaned['Discounted_Price_$'],vert=False, patch_artist=True,notch=True)
   ax[1,1].set_title("Identify Outliers After Price Changes",color='k',fontsize=10)
   
   #Display
   plt.tight_layout()
   plt.savefig('ratings.png')
   plt.show()


```
![image alt](https://github.com/Sanele-Zondo/data_projects/blob/304db48d3b2d7a6a7b02499fdddd482337910813/dashboard.png)

---

## 9. Data Storage
```python
## 5. Export Data (Excel And SQL)
# SQL
   db_parameters =
{
   Database credentials
}
   try:
       connect = sql.connect(**db_parameters)
       cursor  = connect.cursor()
       
       create_table =''' Create Table If Not Exists laptops_data(
           Id int Primary Key
           ,Name varchar
           ,Prices_$ float
           ,Discounted_Price_$ float
           ,Screen_Size varchar
           ,Processor varchar
           ,Ram varchar
           ,Storage varchar
           ,Graphics_Card varchar
           ,Operating_System varchar
           ,Ratings int
           ,Reviews int
           ,Category varchar
           
       )
       '''
       #Create Table in PostGres
       cursor.execute(create_table)
       #commit Changes
       connect.commit()
       #Clear the existing table before inserting
       cursor.execute('Truncate Table laptops_data')
       #Insert data
       insert_query="""INSERT INTO laptops_data VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
       
       for index, row in data_cleaned.iterrows():
           cursor.execute(insert_query,[index
                                        ,row['Names']
                                        ,row['Prices_$']
                                        ,row['Discounted_Price_$']
                                        ,row['Screen_Size']
                                        ,row['Processor']
                                        ,row['Ram']
                                        ,row['Storage']
                                        ,row['Graphics_Card']
                                        ,row['Operating_System']
                                        ,row['Ratings']
                                        ,row['Reviews']
                                        ,row['Category']
                                       ])
       #commit Changes
       connect.commit()
       
   except Exception as e:
       print(f'Error:{e}')
   finally:
       if connect:
           connect.close()
       if  cursor:
           cursor.close()
```
---

## 9. Descriptive Analytics
Understanding the Data

```python
   # 1.Total Number of Laptops
   def count(df):
       return df.count()
   print(f'There are {count(data_cleaned['Names'])} Laptops')
```

There are 117 Laptops
```python
   # 2.Potential Revenue
   def sum_total(df):
       return df.sum()
   print(f'Potential Revenue: ${sum_total(data_cleaned['Prices_$']).round(2)}')
   ```

Potential Revenue: $106399.08
```python
   #3.Distribution by Operating System
   def groupby_count(df,col,values):
       return df.groupby(col).agg({values:'count'}).sort_values(by=values,ascending=True)
   groupby_count(data_cleaned,'Operating_System','Names')
   ```
![image alt]()

```python
   # 4.Distribution by Category
   groupby_count(data_cleaned,'Category','Names')
```
![image alt]()
---
## 10. Business Questions (Analytical & Performance Evaluation)
Revenue and Category Contribution:
```python
   # 1. What is the total potential revenue for each category?
   def sum_by_col(df,col,values):
       return df.groupby(col).agg({values:'sum'}).sort_values(by=values,ascending=True)
   sum_by_col(data_cleaned,'Category','Prices_$')
```
![image alt]()
```python
   # 2. Which category contributes the most and least to overall potential revenue?
   print('From Above anaysis:\nContributes Least to potential revenue-Education Category\nContributes High to potential revenue-Work Category')
```
From Above anaysis:

Contributes Least to potential revenue-Education Category

Contributes High to potential revenue-Work Category
### Rating Analysis
```python
   # 1.What is the average rating for each category?
   def ave_by_col(df,col,values):
       return df.groupby(col).agg({values:'mean'}).sort_values(by=values,ascending=True)
   ave_by_col(data_cleaned,'Category','Ratings')
```
```python
   # 2 What is a maximum rating?
   print(f'Maximum Rating: {data_cleaned['Ratings'].max()}')
```
Maximum Rating: 4
```python
   # 4.Which specific laptops in each category have the highest and lowest ratings?
   data_cleaned.query('`Ratings`==1').groupby(['Category','Names']).min()
   data_cleaned.query('`Ratings`==4').groupby(['Category','Names']).max()
```
![image alt]()
![image alt]()
### Revenue Optimization (Pricing Strategy)

Impact of Discounts and Price Changes:
```python
# 1. What is the total revenue after applying all discounts and price increases?
print(f'Potential Revenue After Price Changes : ${sum_total(data_cleaned['Discounted_Price_$'])}')
```
Potential Revenue After Price Changes : $95128.70000000001
```python
# 2. How does the total revenue after price changes compare to the original revenue?
before_price_changes=sum_total(data_cleaned['Prices_$']).round(2)
after_price_changes=sum_total(data_cleaned['Discounted_Price_$']).round(2)
print(f'Potential Revenue Before Price Changes : $ {before_price_changes}')
print(f'Potential Revenue After Price Changes : $ {after_price_changes}')
change_in_price=before_price_changes-after_price_changes
print(f'Change In Price:$ {change_in_price.round(2)}')
```
Potential Revenue Before Price Changes : $ 106399.08

Potential Revenue After Price Changes : $ 95128.7

Change In Price:$ 11270.38
### Price Change Implications:
```python
#1. What are the implications of the price changes on overall revenue?
print(f'Potential Revenue Decreased By:$ {change_in_price.round(2)}')
```
Potential Revenue Decreased By:$ 11270.38



```python
#2.Changes in Price By Category?
category_before=sum_by_col(data_cleaned,'Category','Prices_$')
category_after=sum_by_col(data_cleaned,'Category','Discounted_Price_$')
#Join tables
category_data=pd.merge(category_before,category_after,on='Category',how='inner')
category_data
#Get Change in Price
category_data['Change_%']=((category_data['Discounted_Price_$']-category_data['Prices_$'])/category_data['Prices_$']*100).round(2)
category_data.insert(0,'Category',category_data.index)
```

## 9. Challenges and Solutions
*Details about challenges faced and solutions implemented during the project will be added here.*
