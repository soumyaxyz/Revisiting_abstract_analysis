import os
import re

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



input_folder = "/Users/aayush/Desktop/ODU/GRA/abstractAnalysis/arxiv_final/test"
output_folder = "/Users/aayush/Desktop/ODU/GRA/abstractAnalysis/arxiv_final/test_output"

get_abstract(input_folder, output_folder)

output_categories = []

def output(output_folder):

    for filename in os.listdir(output_folder):
        if filename.endswith(".txt"):
            output_file_path = os.path.join(output_folder, filename)
            
            with open(output_file_path, 'r') as output_file:

                output_per_abstract = []
                for line in output_file:
                    line = line.strip()

                    if line.startswith("###"):
                        continue

                    elif line.startswith("##"):
                        continue

                    elif line.startswith("#"):
                        if output_per_abstract:
                            output_categories.append(output_per_abstract)
                        
                        output_per_abstract = []

                    elif line=="\n":
                        continue

                    elif line.startswith("Background"):
                        output_per_abstract.append('0')
                    
                    elif line.startswith("Technique"):
                        output_per_abstract.append('1')


                    elif line.startswith("Observation"):
                        output_per_abstract.append('2')

                
                output_categories.append(output_per_abstract)

def similarity(input_list, output_list):

    if len(input_list) != len(output_list) or len(input_list[0]) != len(output_list[0]):
        return 0

    total_elements = len(input_list) * len(input_list[0])
    matching_elements = sum(1 for i in range(len(input_list))
                             for j in range(len(input_list[0]))
                             if input_list[i][j] == output_list[i][j])

    similarity_percentage = (matching_elements / total_elements) * 100
    
    return similarity_percentage

output(output_folder)

matching_percent = similarity(categories, output_categories)

print("Similarity Percentage:", matching_percent)