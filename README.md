# Abstract Analysis with Generative AI

## Overview

This project is designed to automate the analysis of scientific research abstracts using generative AI. It leverages the OpenAI API and the Langchain library to categorize sentences within research abstracts into one of three categories: 'Background,' 'Technique,' or 'Observation.'

## Project Structure

The project directory is organized as follows:

analysis.py: The main script for abstract analysis and categorization.
input_folder/: Folder containing input research abstracts (text files).
output_folder/: Folder where the categorized abstracts obtained from the OpenAI API will be saved.

## Results

The project will provide AI-generated categorizations for the research abstracts. The accuracy indicates how well the API's output aligns with the expected categories. You can review and analyze the results in the output text files by comparing it with the input files