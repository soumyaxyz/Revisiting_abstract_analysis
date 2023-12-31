import os
import re
import numpy as np
from fuzzywuzzy import fuzz
from itertools import chain
from sklearn.metrics import accuracy_score


from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

chat = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL)

def categorize_sentences(abstract):
    
    if abstract != "":
        template="""Label EACH sentence of the following abstract as either 'Background' 'Technique' or 'Observation' and display output for each sentence as "Observation: ......(sentence) etc etc" . Each sentence starts on a new line so label each of them and the sentences should NOT be changed or broken and the number of sentences in output should be NOT MORE OR LESS THAN THEY ARE. DO NOT club the sentences together under a catgerory, label each seperately AND display the output in the SAME ORDER OF SENTENCES AS THEY APPEAR."""
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)

        human_template=abstract
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        response = chat(chat_prompt.format_prompt().to_messages())
        categorized_sentences = response.content.strip().split('\n\n')
        output = ""
        for idx, sentence in enumerate(categorized_sentences):

            output+=f"{sentence}\n"
        
        return(output)
    
    else:
        return("")


categories = []

def get_abstract(input_folder, output_folder):

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename.replace(".txt", "_output.txt"))
            
            with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
                abstract_number = None
                abstract_link = None
                abstract_title = None
                categories_per_abstract = []

                abstract = ""
                for line in input_file:
                    line = line.strip()
                    
                    if line.startswith("###"):
                        abstract_link = line.replace("###", "").strip()
                        output_file.write(f"### {abstract_link}\n")

                    elif line.startswith("##"):
                        abstract_title = line.replace("##", "").strip()
                        output_file.write(f"## {abstract_title}\n\n")

                    elif line.startswith("#"):
                        categorized_abstract = categorize_sentences(abstract)
                        output_file.write(categorized_abstract)
                        output_file.write("\n\n")
                        abstract_number = line.replace("#", "").strip()
                        output_file.write(f"# {abstract_number}\n")
                        
                        if categories_per_abstract:
                            categories.append(categories_per_abstract)
                        
                        abstract = ""
                        categories_per_abstract = []

                    elif line=="\n":
                        output_file.write("\n\n")

                    elif line.startswith("0"):
                        line = line.replace("0", "")
                        line = line.strip()
                        abstract+=line + f"\n"
                        categories_per_abstract.append("0")
                    
                    elif line.startswith("1"):
                        line = line.replace("1", "")
                        line = line.strip()
                        abstract+=line + f"\n"
                        categories_per_abstract.append("1")

                    elif line.startswith("2"):
                        line = line.replace("2", "")
                        line = line.strip()
                        abstract+=line + f"\n"
                        categories_per_abstract.append("2")

                categorized_abstract = categorize_sentences(abstract)
                output_file.write(categorized_abstract)
                output_file.write("\n\n")
                categories.append(categories_per_abstract)


input_folder = "/Users/aayush/Desktop/ODU/GRA/Revisiting_abstract_analysis/input_folder" # Enter the location of the folder where txt files are stored
output_folder = "/Users/aayush/Desktop/ODU/GRA/Revisiting_abstract_analysis/output_folder" # Enter the location of the folder where output should be stored

if os.path.exists(output_folder):
    folder_contents = os.listdir(output_folder)
    folder_has_files = len(folder_contents) > 0

    if folder_has_files == False:
        get_abstract(input_folder, output_folder)
    else:
        for filename in os.listdir(input_folder):
            if filename.endswith(".txt"):
                input_file_path = os.path.join(input_folder, filename)
                
                with open(input_file_path, 'r') as input_file:

                    categories_per_abstract = []

                    abstract = ""
                    for line in input_file:
                        line = line.strip()
                        
                        if line.startswith("###"):
                            continue

                        elif line.startswith("##"):
                            continue

                        elif line.startswith("#"):
                            if categories_per_abstract:
                                categories.append(categories_per_abstract)
                            
                            categories_per_abstract = []

                        elif line=="\n":
                            continue

                        elif line.startswith("0"):
                            categories_per_abstract.append("0")
                        
                        elif line.startswith("1"):
                            categories_per_abstract.append("1")

                        elif line.startswith("2"):
                            categories_per_abstract.append("2")

                    categories.append(categories_per_abstract)


output_categories = []

def fuzzy_match_score(line1, line2):
    return fuzz.ratio(line1, line2)


def output(output_folder):

    for filename in os.listdir(output_folder):
        if filename.endswith(".txt"):
            output_file_path = os.path.join(output_folder, filename)
            
            
            with open("/Users/aayush/Desktop/ODU/GRA/Revisiting_abstract_analysis/input_folder/arxiv_test.txt", "r") as file1, open(output_file_path, "r") as file2:
                content1 = file1.read()
                content2 = file2.read()

            modified_contents1 = content1.replace("\n\n\n", "\n\n")
            modified_contents2 = content2.replace("\n\n\n", "\n\n")

            with open('/Users/aayush/Desktop/ODU/GRA/Revisiting_abstract_analysis/input_folder/arxiv_test.txt', 'w') as file1, open(output_file_path, "w") as file2:
                file1.write(modified_contents1)
                file2.write(modified_contents2)

            with open("/Users/aayush/Desktop/ODU/GRA/Revisiting_abstract_analysis/input_folder/arxiv_test.txt", "r") as file1, open(output_file_path, "r") as file2:
                content1 = file1.readlines()
                content2 = file2.readlines()

            output_per_abstract = []
            index1, index2 = 0, 0

            while index1 < len(content1) and index2 < len(content2):
                line1 = content1[index1]
                line1 = line1.strip()
                line = content2[index2]
                line = line.strip()

                score = fuzzy_match_score(line1, line)

                if score >= 60:
                    if line.startswith("###"):
                        pass

                    elif line.startswith("##"):
                        pass

                    elif line.startswith("#"):
                        if output_per_abstract:
                            output_categories.append(output_per_abstract)
                        
                        output_per_abstract = []

                    elif line=="\n":
                        pass

                    elif line.startswith("Background"):
                        output_per_abstract.append('0')
                    
                    elif line.startswith("Technique"):
                        output_per_abstract.append('1')

                    elif line.startswith("Observation"):
                        output_per_abstract.append('2')
                    index1 += 1
                    index2 += 1

                else:
                    index2 += 1

            output_categories.append(output_per_abstract)

def similarity(input_list, output_list):

    input_flat = []
    output_flat = []

    input_flat = list(chain.from_iterable(input_list))
    output_flat = list(chain.from_iterable(output_list))

    similarity_percentage = accuracy_score(input_flat, output_flat) * 100
    return similarity_percentage

output(output_folder)

accuracy = similarity(categories, output_categories)

print("Similarity Percentage:", accuracy)
