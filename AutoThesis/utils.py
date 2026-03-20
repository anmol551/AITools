import yaml
import pandas as pd

prompt_parameters = """
    Parameters: 
    - Tone: Research Oriented
    - Writing technique: Student level 
    - Language: British English always.
    - Comma usage: very less 
    - Words that should not be used: leverage, rigor, overall, additionally, furthermore, moreover, nuanced, 
        notably, utilized, utilize, foster, pivot, pivotal, robust, highlights, enhances, tailored, employed,
        finally, lastly, relevance, encompassed, reveals, generalizability, demonstrate, meticulously, paramount, realm, employing, employ. Avoid using this words and its related verbs.
        
    - Properly calculate the word count. (Do not do things like actual word count is 98 and mentioned is 198 also do not consider space in the word count calculation)
    - Do not mention word count.
    - Avoid technical jargon where possible and ensure readability.
    - Do not make it first person, write it professionally 
    - Do not start any sentence from Moreover, in addition or furthermore.
    - Avoid using words line in conclusion.
    - No citation should be repeated twice.
    - Avoid using * or () or - of points or content
    - Do not make any sentence bold or italic or ' or 's in words.
    - For each section keep a 30 words information.
    - Citation should be : Sharif et al. (2020) do not add this it is only example. And do not use other format.
    - Use '%' symbol instead of writing word percent.
    
    Note: Keep language as UK/British English only.

    """
    
def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
    
def load_files():
    
    config = load_config('config.yaml')
    
    with open(config['LITERATURE_REVIEW_SUMMARY_PATH'], "r", encoding="utf-8") as file:
        literature_review_summary = file.read()
        
    with open(config['RESEARCH_GAPS'], "r", encoding="utf-8") as file:
        research_gaps = file.read()
        
    with open(config['CODE_SUMMARY_PATH'], "r", encoding="utf-8") as file:
        code_summary = file.read()
        
    with open(config['WEB_APP_SUMMARY_PATH'], "r", encoding="utf-8") as file:
        web_app_summary = file.read()
        
    with open(config['CODE_SUMMARY_VAL_SPECIFIC_PATH'], "r", encoding="utf-8") as file:
        code_summary_val_specific = file.read()
        
    with open(config['NOVELTY_PATH'], "r", encoding="utf-8") as file:
        novelty = file.read()
        
    with open(config['DATA_DETAILS_PATH'], "r", encoding="utf-8") as file:
        data_details = file.read()
        
    with open(config['METHODOLOGY'], "r", encoding="utf-8") as file:
        methodology = file.read()
        
    with open(config['RESEARCH_QUESTION_OBJECTIVES'], "r") as file:
        research_question_and_objectives = file.read()
    
    with open(config['BASE_PAPER_SUMMARY_PATH'], "r", encoding="utf-8") as file:
        base_paper_summary = file.read()
        
    with open(config['RESULT_SUMMARY_PATH'], "r", encoding="utf-8") as file:
        result_summary = file.read()
    
    with open(config['FAILED_ATTEMPT_PATH'], "r", encoding="utf-8") as file:
        failed_attempts = file.read()
        
    with open(config['WEB_APP_DEVELOPMENT'], "r", encoding="utf-8") as file:
        web_app_development = file.read()
        
    with open(config['WEB_APP_TESTING_RESULTS'], "r", encoding="utf-8") as file:
        web_app_testing_results = file.read()
    
        
    title = config['TITLE']
         
     
    ##-- LOAD FILES --##
    return title, literature_review_summary,research_gaps, code_summary, web_app_summary, code_summary_val_specific, novelty, data_details, methodology, research_question_and_objectives, base_paper_summary, result_summary, failed_attempts, web_app_development, web_app_testing_results, prompt_parameters    

def load_question_objectives():
    config = load_config('config.yaml')
    
    question = config['RESEARCH_QUESTION']
    
    objectives = config['RESEARCH_OBJECTIVES']
    
    return question, objectives
    

def paper_cite():
    config = load_config('config.yaml')
    paper_citation = pd.read_csv(config['PAPER_CITATION'], encoding='utf-8')
    return paper_citation

def save_text_file(content: str, file_path: str) -> None:
    """Saves the given content to a .txt file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Error: {e}")