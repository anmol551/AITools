from ai import generate_content
from utils import load_files, paper_cite, load_config


def generate_implementation():
    
    title, literature_review_summary,research_gaps, code_summary, web_app_summary, code_summary_val_specific, novelty, data_details, methodology, research_question_and_objectives, base_paper_summary, result_summary, failed_attempts, web_app_development, web_app_testing_results, prompt_parameters   = load_files()
    paper_citation = paper_cite()
    title_and_citation = paper_citation[['title', 'citation']]
    
    config = load_config('config.yaml')
    format = int(config['FORMAT'])
    

    IMPLEMENTATION_GENERATION_PROMPT = prompt_parameters + """
    Generate an implementation section of my report. There will be following subsections present:

    Subsections 1 : Statistical Analysis (Change heading to match project topic) (100 words)
        1. Begin with a one-line introductory sentence.
        2. Describe the statistical characteristics of the dataset, including:
        3. Total data count, Data types, Statistical measures such as mean, standard deviation, minimum, maximum, and quartiles if available.
        4. Include all values present in the statistical analysis.
        5. Do not use parentheses, asterisks, backticks, or any special formatting around values.
        6. Do not mention code, code execution, or the term "statistical data analysis" directly.
        7. Do not add citations.
        8. Strictly need a content of approximately 100 words.
        
    Subsections 2 : EDA (Change heading to match project topic) (600 words)
        1. Begin with a one-line introductory sentence connecting this section to the previous one. 
        2. Include and explain only figures and insights that belong to the Exploratory Data Analysis stage. Do not include any content or visuals from data preprocessing, feature engineering, or model building.
        3. For each plot used in the EDA: Clearly state the plot title, followed by the type of plot (e.g., bar plot, histogram, heatmap), then give a detailed explanation and insight and only include EDA and visual analysis plot do not add from data preprocessing or results.
        4. Each insight must be written as a paragraph of 60 to 80 words, clearly explaining what the plot reveals.
        5. Mention all numerical values shown in the plot. Do not use parentheses to express values.
        6. Do not refer to axes labels unless the plot is complex (e.g., waveform, MFCC).
        7. Refer to each figure using the format Figure 4.X starting from Figure 4.1, and mention it naturally in the text (e.g., as seen in Figure 4.1, as visualised in Figure 4.2). Vary the placement of figure references (beginning, middle, or end of paragraphs) to avoid repetition.
        8. Do not summarise the section at the end.
        9. Do not add citations.
        10. Do not add plot title from the sentences and do not use words like "this" or "lastly" at the start of sentence.
        11. Do not mention the plot name also in the start.
        12. Do not mention like the first plot and all.
        13. Do not mention plot name in initial time.
        14. Do not use () to show values
        10. Strictly need a content of approximately 600 words.
        
    Subsections 3 : Data Preprocessing (Change heading to match project topic)
        1. Start with a single introductory sentence about the data preprocessing section.
        2. Write about how each technique was implemented, make a sub heading for it. Each sub heading content in 100 words).
        3. If Feature Extraction/Engineering/Selection present explain its implementation in it 150 words.
        4. Add figures insight if available.
        5. Do not add citations.
        6. Strictly need a content of approximately 100 for each technique.
        7. Always keep 2 paragraphs.
        8. Keep content in past tense.
        
    Subsections 4 : Model Training (Change heading to match project topic) 
        1. Begin with a one-line introduction to the model building section.
        2. For each model or algorithm used, write how it was implemented in detail, mention all the used parameters, (Each model content in 150 to 180 words ).
        3. Do not mention any model score.
        4. Do not add citations.
        5. Use comma and fullstop where needed mainly when mentioning parameters value.
        6. Strictly need a content of approximately 150 to 180 words for each model.
        7. Always keep 2 paragraphs.
        8. Keep content in past tense.
        

    Subsections 5 : XAI Framework (Change heading) (150 words)
        First check if XAI term is present is present if yes then:
            1. Write how the XAI method was implemented in detail and for which models.
            2. Mention about the parameters used if any.
            3. Do not mention any score.
            4. Do not add citations.
            5. Strictly need a content of approximately 150 words.
            6. Keep content in past tense.
            

    Subsections 6 : Web Application Framework (Change heading) (200 words)
        1. Write how a web application was developed in detail.
        2. Mention about the parameters used if any.
        3. Do not mention any function name.
        4. Don't mention the names of  created functions and the used best model for prediction.
        5. Do not add citations.
        6. Strictly need a content of approximately 200 words.
        7. Keep content in past tense.
        

    Subsections 7 : Challenges And Solutions (150 words)
        1. Discuss about the challenges faced and solutions implemented while working on this project in brief. 
        2. It should be technical enough.
        3. Add citations for one or 2 challenges. Cite them based on the given title and citation file.  And do not use title it is just for knowing the paper and matching it with the method for citation purposes. 
        4. Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc. In-text citation example: Sharif et al. (2020)
        5. Strictly need a content of approximately 150 words.
        6. Keep content in past tense.
        
    
    Note : 
        Use commas only when necessary and needed. 

    Use code summary value specific, web app summary and citation from:
    {a} {b} {c}
    
    """.format(a=code_summary_val_specific, b=web_app_summary, c=title_and_citation)
    implementation = generate_content(IMPLEMENTATION_GENERATION_PROMPT)
    
    ##########################################################
    
    ##-- WEB APPLICATION DEVELOPMENT --##
    
    WEB_APP_DEVELOPMENT_GENERATION_PROMPT = prompt_parameters + """
    Write about web application development in approximately 200 words in the research report.

    1. Do not mention the web application framework definition.
    2. Keep a paragraph.
    3. Don't mention the any definition.
    4. Do not use parenthesis to mention values'()'
    5. Do use the function or library name in it like keras.sequential() and etc.
    6. Do not mention any code or sub heading.
    7. Strictly need a content of approximately 200 words.

    Note: Only implementation, not theoretical framework
    
    Use web app summary code from:
    {a}
    
    """.format(a=web_app_summary)
    
    web_app_development = generate_content(WEB_APP_DEVELOPMENT_GENERATION_PROMPT)
    
    
    ##########################################################
    
    # Save Research question and objective - FIXED WITH UTF-8 ENCODING
    with open("InputFiles/wad.txt", "w", encoding='utf-8') as file:
        file.write("Web App Development:\n")
        file.write(web_app_development + "\n\n")
    
    # Dictionary to hold section titles and corresponding content
    sections = {
        "IMPLEMENTATION": implementation,
    }
    
    # Writing to file - FIXED WITH UTF-8 ENCODING
    with open("OutputFiles/implementation.txt", "w", encoding='utf-8') as file:
        file.write("IMPLEMENTATION\n")
        file.write("------------------------\n")
        for i, (title, content) in enumerate(sections.items(), 1):
            file.write(f"{i}. {title}\n")
            file.write("-" * 40 + "\n")
            file.write(content + "\n\n")
    
    ##############################################################################################