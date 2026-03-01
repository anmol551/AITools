from ai import generate_content
from utils import load_files, paper_cite, load_config

def generate_methodology():
    title, literature_review_summary,research_gaps, code_summary, web_app_summary, code_summary_val_specific, novelty, data_details, methodology, research_question_and_objectives, base_paper_summary, result_summary, failed_attempts, web_app_development, web_app_testing_results, prompt_parameters = load_files()
    
    paper_citation = paper_cite()
    title_and_citation = paper_citation[['title', 'citation']]
    
    config = load_config('config.yaml')
    format = int(config['FORMAT'])

    
    METHODOLOGY_GENERATION_PROMPT = prompt_parameters + """
    Generate a methodology section of my report. There will be following subsections present:

    Subsections 1 : Research Design (Change heading to match project topic) (150 words)
        1. Write the research designed for the research work. 
        2. Here the full pipeline of research should be mentioned without results. (Start from literature survey or data collection to web app testing, if present.)
        3. It should be technical containing all the methods, techniques and models.  Mention model and web app name.
        4. Don't mention the best model name here.
        5. Avoid Using Function Names.
        6. Make in 2 paragraphs and do not add citations.
        7. Do not add citations.
        8. Strictly need a content of approximately 150 words.
    

    Subsections 2 : Dataset Description (Change heading to match project topic) (150 words)
        1. Write the data description of the used dataset in this research work. 
        2. Specify all data sources and if present mention dataset author name. 
        3. Specify the reason for choosing the data and explain its characteristics.
        4. Mention the shape of the dataset.
        5. In short explain about the format of the files like (.wav for audio, .jpeg or png for images) strictly if present only else skip this. 
        6. Do not mention the exact feature name instead make a table keeping the general info of the features.
        7. Mention the data source link. Eg: Source: Link
        8. Do not add citations.
        9. Strictly need a content of approximately 150 words.
        10. Make it in this way: a. shape, size, and other physical chars, b. why chosen and c. data ethics in 2-3 paragraph all.
        11. And then table or bullets for data key representations.
        

    Subsections 3 : Data Preprocessing (Change heading to match project topic)
        Instructions:
        1. Begin the section with **one clear introductory sentence** describing the importance of data preprocessing in the context of the current project.
        2. For **each data preprocessing technique used** (even if applied inside a function or pipeline), create a **dedicated subheading**.
        3. Under each subheading:
            - Provide a well-structured explanation in **two distinct paragraphs**
            - The total length must be **approximately 130 words per technique**
            - Include:
                • A definition of the technique  
                • The specific reason for its selection in the current context  
                • How it improves model performance or data quality  
                • A citation integrated naturally within the explanation
        4. Use **in-text citations** embedded within sentences. Do not place citations at the beginning or end of paragraphs.  
            - Example citation formats:
                • “According to Sharif et al. (2020), …”  
                • “As demonstrated in a study by Wang et al. (2019), …”  
                • “In a survey conducted by Lee et al. (2021), …”
        5. **Do not include a summary at the end** of the section.
        6. Every preprocessing technique must be covered — even if the implementation is embedded within a function or automated step.
        7. Use the citation file to match the method with the appropriate paper. Do not refer to or mention the title of the paper in the explanation — only use the authors and year for citation.
        → Ensure full compliance with word count, structure (2 paragraphs), and citation rules for each technique to maintain consistency and completeness.
         
    Subsections 4 : Model Building (Change heading to match project topic) 
        Instructions:
        1. Begin with a **one-line introductory sentence** explaining the importance of the model-building stage in the current research context.
        2. For **each model, sub-model, or block** used in the architecture (including hybrid models or stacked designs), follow the instructions below:
            - If the architecture includes a **combined or hybrid model** (e.g., CNN+LSTM+Attention), you must explain **each component separately** — create **individual subheadings** for CNN, LSTM, and Attention. 
            - Do not merge all explanations under a single hybrid model heading. Each core component must be justified and explained **on its own**.
        3. Under each subheading:
            - Write a structured explanation of approximately **200 words**, divided into **two paragraphs**.
            - Paragraph 1: Provide a clear definition and explain **why this model or block was selected**, specifically in the context of your research problem. Avoid generic reasons.
            - Paragraph 2: Describe the **main working principles, internal components, and important parameters** of the model/block. Add **mathematical formulas** where relevant.
            - **Do not** include implementation-level details, function names, training routines, or evaluation results.
        4. Every model or technique mentioned in the architecture — even if used inside a function or as part of another block — **must be explained**.
        5. Include **at least one proper in-text citation** per model or component, based on the given citation file:
            - Do not mention paper titles. Use only author names and years.
            - Example: “As demonstrated by Sharif et al. (2020), …” or “According to the findings of Wang et al. (2019), …”
        6. Strictly **do not include any summaries**, implementation, or performance details in this section.
        ➤ Final Note: This section must fully explain all parts of the model architecture — including any **hybrid**, **stacked**, or **augmented** designs — by **breaking them into their building blocks**. All blocks (e.g., CNN, LSTM, Attention, SE blocks, residual units, etc.) must be given equal and independent treatment, regardless of whether they are standalone or embedded.

    Subsections 5 : Model Performance Evaluation Metrics (200 words)
        1. Write a 1 line introduction of the section.
        2. Write the definition of the model evaluation metrics used in this research. (Each metrics should be explained in 40-50 words)
        3. Discuss evaluation metrics considering the research topic. 
        4. Elaborate on why that particular metric is used in this research if there is any specific reason.
        5. Do not add citations. 
        6. Strictly need a content of approximately 200 words.

    Subsections 6 : XAI Framework (Change heading) (150 words)
        First check if XAI term is present is present if yes then:
            1. Write definition and reason for selecting the used XAI method. 
            2. Add citations for all method. Cite each method based on the given title and citation file.  And do not use title it is just for knowing the paper and matching it with the method for citation purpose. 
            3. Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc. In-text citation example: Sharif et al. (2020)
            4. Word Count should not be less that 150 words. 
            5. Strictly need a content of approximately 150 words.

    Subsections 7 : Web Application Framework (Change heading) (180 words)
        1. Write definition and reason for selecting the used web application framework.
        2. Discuss its benefits and how it's useful and user friendly. 
        3. Add citations for all method. Cite each method based on the given title and citation file.  And do not use title it is just for knowing the paper and matching it with the method for citation purpose. 
        4. Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc. In-text citation example: Sharif et al. (2020)
        5. Strictly Word Count should be approximately 180 words. 
        

    Subsections 8 : Professional, Legal, and Ethical Considerations (200 words)
        1. Write professional, legal and ethical Considerations done while working on this research work.
        2. It may include data and models related factors.
        3. Make one or two paragraphs only. 
        3. Do not add citations.
        4. Strictly need a content of approximately 200 words.
        

    Note : 
    Use commas only when necessary. 
    
    Use code summary, web app summary and citation from:
    {a} {b} {c} {d}
    """.format(a=data_details, b=code_summary, c=web_app_summary, d=title_and_citation)
    
    # Generate content with error handling for Unicode issues
    try:
        methodology = generate_content(METHODOLOGY_GENERATION_PROMPT)
    except UnicodeEncodeError as e:
        print(f"Unicode error during content generation: {e}")
        # Clean the prompt of problematic characters as fallback
        clean_prompt = METHODOLOGY_GENERATION_PROMPT.encode('ascii', 'ignore').decode('ascii')
        methodology = generate_content(clean_prompt)
    
    ##########################################################
    
    # Dictionary to hold section titles and corresponding content
    sections = {
        "METHODOLOGY": methodology,
    }
    
    # Ensure the output directory exists
    import os
    os.makedirs("OutputFiles", exist_ok=True)
    
    # Writing to file with comprehensive Unicode handling
    try:
        with open("OutputFiles/methodology.txt", "w", encoding="utf-8", errors='replace') as file:
            file.write("METHODOLOGY\n")
            file.write("------------------------\n")
            for i, (title, content) in enumerate(sections.items(), 1):
                file.write(f"{i}. {title}\n")
                file.write("-" * 40 + "\n")
                # Ensure content is properly encoded
                if isinstance(content, str):
                    file.write(content + "\n\n")
                else:
                    file.write(str(content) + "\n\n")
        
        print("Methodology file created successfully with UTF-8 encoding.")
        
    except UnicodeEncodeError as e:
        print(f"Unicode encoding error: {e}")
        # Fallback: write with character replacement
        with open("OutputFiles/methodology.txt", "w", encoding="utf-8", errors='replace') as file:
            file.write("METHODOLOGY\n")
            file.write("------------------------\n")
            for i, (title, content) in enumerate(sections.items(), 1):
                file.write(f"{i}. {title}\n")
                file.write("-" * 40 + "\n")
                # Replace problematic characters
                clean_content = str(content).encode('utf-8', 'replace').decode('utf-8')
                file.write(clean_content + "\n\n")
        
        print("Methodology file created with character replacement.")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        # Final fallback: ASCII-only output
        with open("OutputFiles/methodology.txt", "w", encoding="ascii", errors='replace') as file:
            file.write("METHODOLOGY\n")
            file.write("------------------------\n")
            for i, (title, content) in enumerate(sections.items(), 1):
                file.write(f"{i}. {title}\n")
                file.write("-" * 40 + "\n")
                ascii_content = str(content).encode('ascii', 'replace').decode('ascii')
                file.write(ascii_content + "\n\n")
        
        print("Methodology file created with ASCII encoding as fallback.")
                
    ##############################################################################################