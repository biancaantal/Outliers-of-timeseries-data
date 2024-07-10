# Outliers-of-timeseries-data
Identify outliers of timeseries data (Stock price)


## Objective
The objective of the application is to spot possible errors or "outliers" in the price data provided for different global "Exchanges".

## About
The solution has been implemented in python and as specified in the requirements, it utilises 2 functions:
* 1st function that, for each file provided, returns exactly 30 consecutive data points starting from a random timestamp within the file. Which means the timestamp cannot be from the last 29 data points.
* 2nd function that gets the output from 1st one as a feed and returns the list of outliers.

The application has 2 parameters as inputs: 
* the folder path of the unzipped file "(TC1)(TC2) stock_price_data_files.zip"
* the recommended number of files to be sampled for each Stock Exchange.

The output files are stored in the same folder as the input files and for this reason only the files that don't contain the word "outlier" are processed and checked for outliers. 
The output file names contain the datetime when they have been generated in order to not overwrite the files if the application is run multiple times.

For each file are displayed the results of the main steps to be able to reconcile how the outliers have been identified.
![image](https://github.com/biancaantal/Outliers-of-timeseries-data/assets/175165288/ee3356a9-f46f-4ab7-8b7f-3b135466e128)


Checks performed along the development:
* all data from csv file is loaded into data frame.
* the solution handles folders that don't contain any file.
* the solution doesn't process the outliers for files with less than 30 data points.
* the solution handles empty files.
* columns have an appropriate datatype.
* check all calculations and the correct identification of outliers

## Prerequistes
* Python
* Git

## Set up and run the application
* Place the file "(TC1)(TC2) stock_price_data_files.zip" into a preferable folder and unzip it.

* Open Command Prompt and ensure git and python are installed

* Change the directory to a preferable path where to download the repository from GitHub
i.e.: **cd C:\Users\Bii\Documents\B- Test - Repository**

* Clone the repository by using the following command:
**git clone https://github.com/biancaantal/Outliers-of-timeseries-data.git**

* Change the directory to the cloned repository:
**cd Outliers-of-timeseries-data**

* Create a virtual environment to manage dependencies:
**python -m venv venv**

* Activate the virtual environment:
**venv\Scripts\activate**

* Manually install the libraries if they are not already installed (a "requirements.txt" document can be added in GitHub as future improvement)
**pip install pandas**

* Run the main script by specifying the 2 parameters: the location of the unzipped file and the recommended number of files to be sampled for each Stock Exchange:
**python main.py "C:/Users/Bii/Documents/LSEG Technical Exercise/(TC1)(TC2) stock_price_data_files" 2**

## Possible improvements
* add a "requirements.txt" document in GitHub to install the libraries
* possible to process the files directly from the .zip file, without being necessary to manually unzip it
* create visualisations to display the outliers of each file
