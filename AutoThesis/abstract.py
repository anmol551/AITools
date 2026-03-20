from ai import generate_content
from utils import load_files

def generate_abstract():
    
    title, literature_review_summary,research_gaps, code_summary, web_app_summary, code_summary_val_specific, novelty, data_details, methodology, research_question_and_objectives, base_paper_summary, result_summary, failed_attempts, web_app_development, web_app_testing_results, prompt_parameters = load_files()
    
    
    ABSTRACT_GENERATION_PROMPT = prompt_parameters + """"
     Write abstract for approximately  230 words for the research report. 
     Begin with problem intro, then ML role, selected dataset name, then proposed methodology, methods used, best model and best score, surpassed benchmark web app also.
     Mention XAI if only present else do not mention anything of it.
     Mention the web app framework name also.
     Keep it technical. Mention only accuracy of best model not other scores
     Do not use words like In Conclusion or in summarising.
     Do not mention future work.
     
    Also generate the comma separated  12 keywords (most important) like used techniques and model name or layer names-- capitalize form all in 1 line.
     
    Note: Put strict instructions: not less than 230 words + should be 1 paragraphs (continuous paragraphs as per thesis)
     
     
     Use Code Summary Value Specific from:
     {a} {b} {c}
    """.format(a=code_summary_val_specific, b=web_app_summary, c=data_details)
    
    abstract = generate_content(ABSTRACT_GENERATION_PROMPT)
    
    # Dictionary to hold section titles and corresponding content
    sections = {
        "ABSTRACT": abstract,
    }
    
    # Writing to file
    with open("OutputFiles/abstract.txt", "w") as file:
        file.write("ABSTRACT\n")
        file.write("------------------------\n")
        for i, (title, content) in enumerate(sections.items(), 1):
            file.write(f"{i}. {title}\n")
            file.write("-" * 40 + "\n")
            file.write(content + "\n\n")

# call the abstract function
# generate_abstract()
# print("🕺🕺🕺 Hooray Section Generated, Nacho 🕺🕺🕺!")
