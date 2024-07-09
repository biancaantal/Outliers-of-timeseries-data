import pandas as pd
import os
import random
import numpy as np
from datetime import datetime


folder_path ="C:/Users/Bii/Documents/LSEG Technical Exercise/(TC1)(TC2) stock_price_data_files"
no_of_input_files = 2
exclude_files_with_word = "outliers"


# Function returns  30 consecutive data points starting from a random timestamp within the file.
def return_consecutive_data_points(df):
    
    #Ensure the data is sorted in the dataframe
    df.sort_values(by='Timestamp')
    
    # Select a random starting data point ensuring that the random timestamp is not in the last 29 data points  
    start_data_point = random.randint(0, len(df) - 30)
    print(f"Random start data point in df = {start_data_point}, so csv row number = {start_data_point + 1}")
    print(f"Random start timestamp = {df.iloc[start_data_point][1]}")
    
    # Return the 30 data points starting from the random timestamp
    return df.iloc[start_data_point:start_data_point + 30]


# Function to identify the outliers in the file
def identify_outliers(df):
    
    mean_StockPrice = df['StockPriceValue'].mean().round(2)
    std_StockPrice = df['StockPriceValue'].std().round(2)
    print(f"mean_StockPrice = {mean_StockPrice}")
    print(f"std_StockPrice = {std_StockPrice}")
    
    # Identiy outliers: Any datapoint that is over 2 standard deviations beyond the mean of the 30 sampled data points    
    min_threshold = (mean_StockPrice - 2 * std_StockPrice).round(2)
    max_threshold = (mean_StockPrice + 2 * std_StockPrice).round(2)         
    outliers = df[ (df['StockPriceValue'] < min_threshold) | (df['StockPriceValue'] > max_threshold )].copy()
    print(f"Outliers are data points outside the range [ {min_threshold}, {max_threshold} ]")
    
    # Check if there are outliers and based on this create the other columns in the output
    outliers_len = len(outliers)
    
    if outliers_len > 0:
        outliers.loc[:, 'Mean30points'] = mean_StockPrice
        outliers.loc[:, 'StockPriceValueMinusMean'] = outliers['StockPriceValue'] - mean_StockPrice
        outliers.loc[:, '%DeviationFromThreshold']  = np.where(outliers['StockPriceValue'] > max_threshold,
                                                               
                                                               (outliers['StockPriceValue'] - max_threshold) / max_threshold * 100,
                                                               
                                                               (outliers['StockPriceValue'] - min_threshold) / min_threshold * 100
                                                               )  
        # Round the new columns to 2 decimals
        outliers['Mean30points'] = outliers['Mean30points'].round(2)
        outliers['StockPriceValueMinusMean'] = outliers['StockPriceValueMinusMean'].round(2)
        outliers['%DeviationFromThreshold'] = outliers['%DeviationFromThreshold'].round(2)

                                         
        return outliers 
            

    
# Main - Iterate through the files in the specified folder and extract the outliers in csv files
for subdir, dirs, files in os.walk(folder_path):
    
    # Check the number of csv files only in the subfolders
    if subdir != folder_path:
        if len(files) == 0:
            print(f"No file in the folder {subdir}")
        else:
            # Iterate through the files in each subfolder
            count_files_in_folder = 0 
            
            for file in files:
                try:
           
                    if count_files_in_folder < no_of_input_files:                    
                        full_file_name = os.path.join(subdir, file)
                        
                        # Files that contain the "outliers" word won't be processed since they are only outputs
                        if exclude_files_with_word not in file:
                            
                            # Load the csv into a dataframe and check the number of data points in it
                            print(f"FILE - {full_file_name}")
                            
                            df = pd.read_csv(full_file_name, header=None)
                            if len(df) < 30:                           
                                print("File doesn't have enough data points. The requirement is minimum 30.\n")
                            else:
                                # Rename the dataframe columns
                                df = df.rename(columns={0:'StockId',
                                                        1:'Timestamp',
                                                        2:'StockPriceValue'})
                        
                                # Ensure datatype is correct for each column
                                df['StockId'] = df['StockId'].astype(str)
                                df['Timestamp'] = df['Timestamp'].str.strip()
                                df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d-%m-%Y', dayfirst = True, errors='raise')
                                df['StockPriceValue'] = df['StockPriceValue'].astype(float)
                        
                    
                                # Extract the 30 data points and identify the outliers
                                extracted_data_points = return_consecutive_data_points(df)
                                output_outliers = identify_outliers(extracted_data_points)
        
                                # Check if the file has outliers and export them into csv files 
                                if output_outliers is None or len(output_outliers) == 0:
                                    print("No outliers for the file.\n")
                            
                                else:
                                    #Outlier file name contains the datetime when it has been created
                                    get_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
                                    output_filename = os.path.splitext(file)[0] + f'_outliers_{get_datetime}.csv'                            
                                    output_path = os.path.join(subdir, output_filename)
                                    output_outliers.to_csv(output_path, index=False)
                                    count_files_in_folder = count_files_in_folder + 1
                                    print(f"Outliers processed into the file {output_path}.\n")                            
    
                except FileNotFoundError as e:
                    print(f"Path/File not found: {e}\n")
                    continue                            
                except pd.errors.EmptyDataError as e:
                    print(f"File is empty {full_file_name}: {e}\n")
                    continue                         
                except pd.errors.ParserError as e:
                    print(f"CSV file has invalid format {full_file_name}: {e}\n")
                    continue
                except ValueError as e:
                    print(f"Value error {full_file_name}: {e}\n")
                    continue        
                except Exception as e:
                    print(f"Unexpected error {full_file_name}: {e}\n")
                    continue
    
                   



        
        