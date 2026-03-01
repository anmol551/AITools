from ai import generate_content
from utils import load_files

def generate_keywords():
    
    title, literature_review_summary,research_gaps, code_summary, web_app_summary, code_summary_val_specific, novelty, data_details, methodology, research_question_and_objectives, base_paper_summary, result_summary, failed_attempts, web_app_development, web_app_testing_results, prompt_parameters = load_files()
    
    
    KEYWORDS_GENERATION_PROMPT = """
    Provide me all the preprocessing techniques and model name used  in the code file:
    Give only name  and keep only 1 name in each line
    Do not mention the function name or evaluation metrics name.
    Do not use - or any thing 
    
    Use the code summary value specific file from:
    {a} {b}
    
    """.format(a=code_summary_val_specific, b=web_app_summary)
    
    keywords = generate_content(KEYWORDS_GENERATION_PROMPT)
    
    # Save to a text file
    with open("InputFiles/keywords.txt", "w") as file:
        file.write(keywords)

# generate_keywords()    