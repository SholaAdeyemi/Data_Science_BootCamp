import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import csv
import logging


class SalesData: #Initiate the class function with 'SalesData'
    def __init__(self,file_path):
        """initiate the file path of the data in csv format"""
        self.file_path=file_path
        logging.basicConfig(filename=file_path,level=logging.DEBUG,format='')#con
        try:
            self.df=pd.read_csv(file_path) #read the data in the file path
            print("File Read Successfully\n")
            self.df['Date']=pd.to_datetime(self.df['Date']) #Change the date COlumn to datetime format
            
    #Handling and tracking Errors that can occur while reading the file    
        except FileNotFoundError:
            logging.error(f"Error: The file '{file_path}' Not Found")
            return None
        except pd.errors.EmptyDataError:
            logging.error("Error: The File is empty")
            return None
        except pd.errors.ParserErrors:
            logging.error("Error:There is an issue parsing the file")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occur: {e}")
            return None
        
        
    """Information About the Dataset"""
    def basic_info(self):
        print("\nGeneral Information")
        print(self.df.info()) # Gives General Information
        print("\nMissing Values:")
        print(self.df.isnull().sum()) #Gives all missing values in each column 
        print("\nSummary Statistics:")
        print(self.df.describe(include='all'))#Gives an Overview of the basic descriptive staticstics
        print(f"\nNumber of duplicate rows: {self.df.duplicated().sum()}") # Shows if there are duplicated rows in the data
              
     #To find Pattern in the data       
    def univariate_analysis(self):
        """Analyze one variable at a time"""
        print("\nNumerical Column Histogram")
        self.df.hist(bins=10,figsize=(15,10))
        plt.show()
        
        #Categorical Column
        categorical_columns=self.df.select_dtypes(include=['object']).columns
        for column in categorical_columns:
            plt.figure(figsize=(10,6))
            sns.set(style='darkgrid')
            #Give the top 15 products in the each categorical data
            sns.countplot(y=column,data=self.df,order=self.df[column].value_counts().sort_values().tail(15).index)
            plt.title(f"Distribution of {column}")
            plt.xlabel('Count')
            plt.ylabel(column)
            plt.show()
                     
    
    
    def correlation_matrix(self):
        """To examine the relationship between the price and the Quantity"""
        plt.figure(figsize=(12,8))
        sns.heatmap(self.df.corr(numeric_only=True), annot=True, cmap='viridis',vmin=-2,vmax=2,center=0)
        plt.title("Correlation Matrix")
        plt.show
          
    def boxplot_analysis(self):
        """To View Outliers"""
        numerical_columns=self.df.select_dtypes(include=[np.number]).columns
        for column in numerical_columns:
            plt.figure(figsize=(12,6))
            sns.boxplot(x=self.df[column])
            plt.title(f"Boxplot for {column}")
            plt.show()
            
         
    def sales_by_category(self):
        """Analyze total sales by category."""
        self.df['Total_Sales'] = self.df['Quantity'] * self.df['Price']
        total_sales_per_category = self.df.groupby('Category')['Total_Sales'].sum().sort_values(ascending=False)
        print("\nTotal Sales per Category:\n",total_sales_per_category)
       
    
    #Highest product Sold
    def sales_by_item(self):
        """Generate total sales by item."""
        self.df['Total_Sales'] = self.df['Quantity'] * self.df['Price'] 
        total_sales_per_item = self.df.groupby('ProductID')['Total_Sales'].sum().sort_values(ascending=False) 
        print("\nTotal Sales per Item:\n",total_sales_per_item.head(15))
               
    def sales_trend(self):
        """Analyze the sales trend over time."""
        self.df['Total_Sales'] = self.df['Quantity'] * self.df['Price']
        sales_trend = self.df.groupby(self.df['Date'].dt.to_period("M"))['Total_Sales'].sum()
        plt.figure(figsize=(12, 6))
        sales_trend.plot()
        plt.title("Sales Trend Over Time")
        plt.xlabel("Month")
        plt.ylabel("Total Sales")
        plt.show()
        
    def sales_by_year_month(self):
        """Analyze sales by year and month."""
        self.df['Year'] = self.df['Date'].dt.year
        self.df['Month'] = self.df['Date'].dt.month

        # Yearly Sales
        self.df['Total_Sales'] = self.df['Quantity'] * self.df['Price']
        yearly_sales = self.df.groupby('Year')['Total_Sales'].sum()
        print("\nYearly Sales:")
        print(yearly_sales)

        # Monthly Sales across years
        monthly_sales = self.df.groupby(['Year', 'Month'])['Total_Sales'].sum().unstack()
        plt.figure(figsize=(22, 16))
        sns.heatmap(monthly_sales, annot=True, fmt='.2f', cmap='viridis',square=True,linewidths=.10)
        plt.title("Monthly Sales by Year")
        plt.xlabel("Month")
        plt.ylabel("Year")
        plt.show()
    
    def high_quantity_sales(self, threshold=10):
        """Filter and display sales with quantity above a threshold."""
        high_quantity_sales = self.df[self.df['Quantity'] > threshold] #Filter records where Quantity > threshold
        print(f"\nHigh Quantity Sales (Quanity > {threshold}):")
        print(high_quantity_sales.head())

    def high_value_sales(self,threshold=9000):
        """Generate a List of Sales Record Greater than a Particular Value"""
        self.df['Total_Sales'] = self.df['Quantity'] * self.df['Price']    # Calculate Total Sales
        return [row for Total_Sales, row in self.df.iterrows() if row['Total_Sales'] > threshold] #Filter records where Total_Sales > threshold
        
        