from ai import generate_content
from utils import load_files, load_config, load_question_objectives



def generate_introduction():
    
    ##-- BACKGROUND --##
    
    title, literature_review_summary,research_gaps, code_summary, web_app_summary, code_summary_val_specific, novelty, data_details, methodology, research_question_and_objectives, base_paper_summary, result_summary, failed_attempts, web_app_development, web_app_testing_results, prompt_parameters  = load_files()
    
    question, objective = load_question_objectives()
    
    config = load_config('config.yaml')
    format = int(config['FORMAT'])
    
    def safe_encode(text, encoding="utf-8"):
            return text.encode(encoding, errors="ignore").decode(encoding)
    

    if format == 1: 
        BACKGROUND_GENERATION_PROMPT = prompt_parameters + """
            Write a well-structure Background section of approximately 250 words for a research paper. This section should include the following components:

            First give a general idea about the topic and the problem, strictly in 80 words, here don't consider ML and DL. If possible add any numeric data obtained from any survey or news like Wikipedia to support the information. 

            Write how ML and DL can help in resolving this identified problem in brief. Summarize key advancements in this area. Mention relevant studies, technological breakthroughs, or academic contributions that highlight the importance of the field. 
            Keep full terms of phrases in the initial part of the report.
            Discuss the importance of researching this topic at the present time. Explain how this study contributes to addressing the identified research gaps.
            Ensure the writing is clear, precise, and free of unnecessary repetition. Do not introduce the specific research problem in detail, as that will be covered in the next section.
            Make the content look like conversational, engaging and flow like a natural story. Also the paragraphs should be linked with previous one.
            Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc.
            Do not mention any model scores and results. In-text citation example: Sharif et al. (2020) - keep this only no other.
                        
            Note: Put strict instructions: not less than 250 words + should be paragraphs (continuous paragraphs as per thesis)
            Use the literature review summary and research gap from:
            {a} {b}
        
        """. format(a=literature_review_summary, b= research_gaps)
        
        background = generate_content(BACKGROUND_GENERATION_PROMPT)
        
        ##########################################################
        
        ##-- PROBLEM STATEMENT --##
        
        PROBLEM_STATEMENT_GENERATION_PROMPT = prompt_parameters + """
            Write a well-structure problem statement section of approximately 250 words for a research paper. This section should be  a concise description of a specific issue or gap in knowledge that a study aims to investigate and resolve in daily life.

            First analysis the given research gaps, general pipeline found in the literature review survey. 
            Current Issues: Clearly describe a specific challenge or limitation in the chosen research domain. Identify an unsolved problem that researchers are currently facing.
            Impact of the Problem: Explain how this issue affects real-world applications, industry, or academia. Provide concrete examples where relevant.
            Existing Attempts and Their Limitations: Highlight previous studies or methods that attempted to address the problem but failed to fully resolve it. Emphasize their shortcomings.
            Need for Your Research: Justify why a new approach is necessary. Clearly outline the research gap that this dissertation aims to fill.
            Do not focus on literature and gaps unresolved issues.
            
            Should mention about model and preprocessing steps and how they are related to the problem statement.

            Maintain a formal academic tone, avoid repetition, and do not introduce research objectives or methodology at this stage. Ensure clarity and coherence in articulating the problem. And do not use words like literature review or analysis of literature review.
            Cite the research citation using literature research. Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc. In-text citation example: Sharif et al. (2020)  - keep this only no other.
            
            Note: Put strict instructions: not less than 250 words + should be paragraphs (continuous paragraphs as per thesis)
            
            
            Use the research gap and literature review from:
            {a} {b}
                
        """.format(a=research_gaps, b=literature_review_summary)
        
        problem_statement =  generate_content(PROBLEM_STATEMENT_GENERATION_PROMPT)
        
        ##########################################################
        
         ##-- RESEARCH OBJECTIVES --##
        
        research_objectives = objective
        
        ##########################################################
        
        ##-- RESEARCH QUESTION --##
        
        
        research_question = question
        
        
       
        ##########################################################
        
        ##-- SIGNIFICANCE OF THE RESEARCH STUDY --##
        
        SIGNIFICANCE_GENERATION_PROMPT = prompt_parameters + """
        Write the Significance of the research section of approximately 250 words for the research paper. This should  highlights the value or impact of the study in advancing knowledge or solving a real-world problem. 

        Elaborate on the potential contributions of the research, such as advancing theoretical understanding, addressing practical challenges, or informing policy or practice. 
        Highlight what makes this study unique or valuable.
        Explain how, to whom and in which sector ML and DL can contribute and help. (Researchers, students and society - Live Applications).
        Do not mention any score of the model ot the result concluding result.
        Cite the research citation using literature research. Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc. In-text citation example: Sharif et al. (2020)  - keep this only no other.
            
        
        Avoid repeating the problem statement. Instead, focus on the broader academic, practical, and societal significance of the findings.
        
        Note: Put strict instructions: not less than 250 words + should be 3 paragraphs (continuous paragraphs as per thesis)
        
        use the code summary with value and novelty file:
        {a} {b} {c}
        
        """.format(a=code_summary_val_specific, b=novelty, c=literature_review_summary)
        
        significance = generate_content(SIGNIFICANCE_GENERATION_PROMPT)
        
        ##########################################################
        
        ##-- SCOPE and LIMITATIONS --##
        
        SCOPE_LIMITATIONS_GENERATION_PROMPT = prompt_parameters + """
        Write the Scope and Limitations of the research section of approximately 250 words for the research paper. This should highlight what is the research doing and what are the limitations observed.

        First explain what the research are doing in a research work and are there any limitations present. (Data related limitations, trust issues, reliability, overall accuracy of model - not about proposed models), market limitations
        Mention possible ways to handle limitations, just give an opinion.
        Do not mention any model or model score or dataset shape.
        
        Ensure clarity and conciseness while avoiding repetition. Do not include future research suggestions, as those belong in the discussion or conclusion section.
        Cite the research citation using literature research.Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc. In-text citation example: Sharif et al. (2020)  - keep this only no other.
            
        Note: Put strict instructions: not less than 250 words + should be 3 paragraphs (continuous paragraphs as per thesis)
        
        
        use the code summary with value and data details file:
        {a} {b} {c} {d}

        """.format(a=code_summary_val_specific, b=data_details, c=research_gaps, d=literature_review_summary)
        
        scope_limitations = generate_content(SCOPE_LIMITATIONS_GENERATION_PROMPT)
        
        ##########################################################
        
        ##-- STRUCTURE OF THE REPORT --##
        
        STRUCTURE_GENERATION_PROMPT = prompt_parameters + """
        Write the content for the organisation of the report in 100 words para for the research paper, summarising the purpose and content of each chapter to guide the reader through the document. 
        
        Do not add citation. 
        
        Note: Put strict instructions: not less than 100 words + should be 1 paragraphs (continuous paragraphs as per thesis)
        
        """
        structure_report = generate_content(STRUCTURE_GENERATION_PROMPT)
        
        ##########################################################
    
    
        # Dictionary to hold section titles and corresponding content
        sections = {
            "BACKGROUND": background,
            "PROBLEM STATEMENT": problem_statement,
            "RESEARCH QUESTION": research_question,
            "RESEARCH OBJECTIVES": research_objectives,
            "SIGNIFICANCE": significance,
            "SCOPE AND LIMITATIONS": scope_limitations,
            "STRUCTURE": structure_report
        }
        
        # Save Research question and objective
        with open("InputFiles/rqo.txt", "w", encoding="utf-8") as file:
            file.write("Research Question:\n")
            file.write(research_question + "\n\n")
            file.write("Research Objectives:\n")
            file.write(research_objectives.strip())
            
        

        with open("OutputFiles/introduction.txt", "w", encoding="utf-8") as file:
            file.write("INTRODUCTION\n")
            file.write("------------------------\n")
            for i, (title, content) in enumerate(sections.items(), 1):
                file.write(f"{i}. {safe_encode(title)}\n")
                file.write("-" * 40 + "\n")
                file.write(safe_encode(content) + "\n\n")
                
    ##############################################################################################
    
    elif format == 2:
        
        BACKGROUND_GENERATION_PROMPT = prompt_parameters + """
            Write a well-structure Background section of approximately 250 words for a research paper. This section should include the following components:

            First the general information of the topic should be discussed that a give a brief idea to the user in 80 words and definition or information of the topic. If possible add any numeric data obtained from any survey or news. 
            
            Summarize key advancements in this area. Mention relevant studies, technological breakthroughs, or academic contributions that highlight the importance of the field. Keep full terms of phrases in the initial part of the report.
            Discuss the importance of researching this topic at the present time. Explain how this study contributes to addressing the identified research gaps.
            Ensure the writing is clear, precise, and free of unnecessary repetition. Do not introduce the specific research problem in detail, as that will be covered in the next section.
            Make the content look like conversational, engaging and flow like a natural story. Also the paragraphs should be linked with previous one.
            Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc.
            Do not mention any model scores and results. In-text citation example: Sharif et al. (2020)
            
            Note: Put strict instructions: not less than 250 words + should be paragraphs (continuous paragraphs as per thesis)
            

            Use the literature review summary and research gap from:
            {a} {b}
        
        """. format(a=literature_review_summary, b= research_gaps)
        
        background = generate_content(BACKGROUND_GENERATION_PROMPT)
        
        ##########################################################
        
        ##-- PROBLEM STATEMENT --##
        
        PROBLEM_STATEMENT_GENERATION_PROMPT = prompt_parameters + """
            Write a well-structure problem statement section of approximately 250 words for a research paper. This section should be  a concise description of a specific issue or gap in knowledge that a study aims to investigate and resolve.

            First analysis the given research gaps, general pipeline found in the literature review survey. 
            Current Issues: Clearly describe a specific challenge or limitation in the chosen research domain. Identify an unsolved problem that researchers are currently facing.
            Impact of the Problem: Explain how this issue affects real-world applications, industry, or academia. Provide concrete examples where relevant.
            Existing Attempts and Their Limitations: Highlight previous studies or methods that attempted to address the problem but failed to fully resolve it. Emphasize their shortcomings.
            Need for Your Research: Justify why a new approach is necessary. Clearly outline the research gap that this dissertation aims to fill.
            Do not focus on literature and gaps unresolved issues.
            
            Should mention about model and preprocessing steps and how they are related to the problem statement.
            

            Maintain a formal academic tone, avoid repetition, and do not introduce research objectives or methodology at this stage. Ensure clarity and coherence in articulating the problem. And do not use words like literature review or analysis of literature review.
            Cite the research citation using literature research. Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc. In-text citation example: Sharif et al. (2020)  - keep this only no other.
            
            Note: Put strict instructions: not less than 250 words + should be paragraphs (continuous paragraphs as per thesis)
            
            Use the research gap from:
            {a} {b}
                
        """.format(a=research_gaps, b=literature_review_summary)
        
        problem_statement =  generate_content(PROBLEM_STATEMENT_GENERATION_PROMPT)
        
        ##########################################################
        
        ##-- RESEARCH QUESTION & OBJECTIVES --##
        RESEARCH_QUESTION_OBJECTIVE_GENERATION_PROMPT = prompt_parameters + """
            Combine the question and objective from the given file and make the format proper add one line sentence before question and objectives.

            Mention objectives as it is.

            Use the research question and objective from:
            {a} {b} 

            """.format(a=question, b=objective)

        research_question_and_objectives = generate_content(RESEARCH_QUESTION_OBJECTIVE_GENERATION_PROMPT)

        ##########################################################
        
        ##-- SIGNIFICANCE OF THE RESEARCH STUDY --##
        
        SIGNIFICANCE_GENERATION_PROMPT = prompt_parameters + """
        Write the Significance of the research section of approximately 250 words for the research paper. This should  highlights the value or impact of the study in advancing knowledge or solving a real-world problem. 

        Elaborate on the potential contributions of the research, such as advancing theoretical understanding, addressing practical challenges, or informing policy or practice. 
        Highlight what makes this study unique or valuable.
        Explain how, to whom and in which sector ML and DL can contribute and help. (Researchers, students and society - Live Applications).
        Do not use words like novel and all.
        Do not mention any score of the model ot the result concluding result.
        
        Cite the research citation using literature research. Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc. In-text citation example: Sharif et al. (2020)  - keep this only no other.
            
        Avoid repeating the problem statement. Instead, focus on the broader academic, practical, and societal significance of the findings.
        
        Note: Put strict instructions: not less than 150 words + should be paragraphs (continuous paragraphs as per thesis)
        
        
        use the code summary with value and novelty file:
        {a} {b} {c}
        
        """.format(a=code_summary_val_specific, b=novelty, c=literature_review_summary)
        
        significance = generate_content(SIGNIFICANCE_GENERATION_PROMPT)
        
        ##########################################################
        
        ##-- SCOPE and LIMITATIONS --##
        
        SCOPE_LIMITATIONS_GENERATION_PROMPT = prompt_parameters + """
        Write the Scope and Limitations of the research section of approximately 150 words for the research paper. This should highlight what is the research doing and what are the limitations observed.

        First explain what the research are doing in a research work and are there any limitations present. (Data related limitations, trust issues, reliability, overall accuracy of model - not about proposed models), market limitations
        Mention possible ways to handle limitations, just give an opinion.
        Do not mention any model or model score or dataset shape.
        Ensure clarity and conciseness while avoiding repetition. Do not include future research suggestions, as those belong in the discussion or conclusion section.
        Cite the research citation using literature research.Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc. In-text citation example: Sharif et al. (2020)  - keep this only no other.
            
        Note: Put strict instructions: not less than 150 words + should be paragraphs (continuous paragraphs as per thesis)
            
        use the code summary with value and data details file:
        {a} {b} {c}

        """.format(a=code_summary_val_specific, b=data_details, c=research_gaps)
        
        scope_limitations = generate_content(SCOPE_LIMITATIONS_GENERATION_PROMPT)
        
        ##########################################################
        
        ##-- STRUCTURE OF THE REPORT --##
        
        STRUCTURE_GENERATION_PROMPT = prompt_parameters + """
        Write the content for the organisation of the report in 100 words para for the research paper, summarising the purpose and content of each chapter to guide the reader through the document. 
        
        Do not citation
        
        Note: Put strict instructions: not less than 100 words + should be paragraphs (continuous paragraphs as per thesis)
        It should not be more than 100 words.
        
        """
        structure_report = generate_content(STRUCTURE_GENERATION_PROMPT)
        
        ##########################################################
    
    
        # Dictionary to hold section titles and corresponding content
        sections = {
            "BACKGROUND": background,
            "PROBLEM STATEMENT": problem_statement,
            "RESEARCH QUESTION AND OBJECTIVES": research_question_and_objectives,
            "SIGNIFICANCE": significance,
            "SCOPE AND LIMITATIONS": scope_limitations,
            "STRUCTURE": structure_report
        }
        
        # Save Research question and objective
        with open("InputFiles/rqo.txt", "w") as file:
            file.write("Research Question and Objectives:\n")
            file.write(research_question_and_objectives + "\n\n")
        
        # Writing to file
        with open("OutputFiles/introduction.txt", "w", encoding="utf-8") as file:
            file.write("INTRODUCTION\n")
            file.write("------------------------\n")
            for i, (title, content) in enumerate(sections.items(), 1):
                file.write(f"{i}. {safe_encode(title)}\n")
                file.write("-" * 40 + "\n")
                file.write(safe_encode(content) + "\n\n")
                
    ##############################################################################################
    
    elif format == 3:
        BACKGROUND_GENERATION_PROMPT = prompt_parameters + """
            Write a well-structure Background section of approximately 250 words for a research paper. This section should include the following components:

            First the general information of the topic should be discussed that a give a brief idea to the user in 80 words and definition or information of the topic. If possible add any numeric data obtained from any survey or news. 
            Summarize key advancements in this area. Mention relevant studies, technological breakthroughs, or academic contributions that highlight the importance of the field. Keep full terms of phrases in the initial part of the report.
            Discuss the importance of researching this topic at the present time. Explain how this study contributes to addressing the identified research gaps.
            Ensure the writing is clear, precise, and free of unnecessary repetition. Do not introduce the specific research problem in detail, as that will be covered in the next section.
            Make the content look like conversational, engaging and flow like a natural story. Also the paragraphs should be linked with previous one.
            Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc.
            Do not mention any model scores and results. In-text citation example: Sharif et al. (2020)
            
            Make subheadings like: Historical Context, Current Developments this is example do not make this only. Total 3 sub heading should be there.
            
            Note: Put strict instructions: not less than 250 words + should be paragraphs (continuous paragraphs as per thesis)
             

            Use the literature review summary and research gap from:
            {a} {b}
        
        """. format(a=literature_review_summary, b= research_gaps)
        
        background = generate_content(BACKGROUND_GENERATION_PROMPT)
        
        ##########################################################
        
        ##-- PROBLEM STATEMENT --##
        
        PROBLEM_STATEMENT_GENERATION_PROMPT = prompt_parameters + """
            Write a well-structure problem statement section of approximately 250 words for a research paper. This section should be  a concise description of a specific issue or gap in knowledge that a study aims to investigate and resolve.

            First analysis the given research gaps, general pipeline found in the literature review survey. 
            Current Issues: Clearly describe a specific challenge or limitation in the chosen research domain. Identify an unsolved problem that researchers are currently facing.
            Impact of the Problem: Explain how this issue affects real-world applications, industry, or academia. Provide concrete examples where relevant.
            Existing Attempts and Their Limitations: Highlight previous studies or methods that attempted to address the problem but failed to fully resolve it. Emphasize their shortcomings.
            Need for Your Research: Justify why a new approach is necessary. Clearly outline the research gap that this dissertation aims to fill.
            Do not focus on literature and gaps unresolved issues.
            
            Should mention about model and preprocessing steps and how they are related to the problem statement.
            

            Maintain a formal academic tone, avoid repetition, and do not introduce research objectives or methodology at this stage. Ensure clarity and coherence in articulating the problem. And do not use words like literature review or analysis of literature review.
            Cite the research citation using literature research. Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc. In-text citation example: Sharif et al. (2020)  - keep this only no other.
            
            
            Note: Put strict instructions: not less than 250 words + should be paragraphs (continuous paragraphs as per thesis)
            
            Use the research gap from:
            {a} {b}
                
        """.format(a=research_gaps, b=literature_review_summary)
        
        problem_statement =  generate_content(PROBLEM_STATEMENT_GENERATION_PROMPT)
        
        ##########################################################
        
        
        RESEARCH_QUESTION_OBJECTIVE_GENERATION_PROMPT = prompt_parameters + """
            Combine the question and objective from the given file and make the format proper add one line sentence before question and objectives.
            
            Mention objectives as it is.
            Use the research question and objective from:
            {a} {b} 

            """.format(a=question, b=objective)

        research_question_and_objectives = generate_content(RESEARCH_QUESTION_OBJECTIVE_GENERATION_PROMPT)

        
        ##########################################################
        
        ##-- SIGNIFICANCE OF THE RESEARCH STUDY --##
        
        SIGNIFICANCE_GENERATION_PROMPT = prompt_parameters + """
        Write the Significance of the research section of approximately 250 words for the research paper. This should  highlights the value or impact of the study in advancing knowledge or solving a real-world problem. 

        Elaborate on the potential contributions of the research, such as advancing theoretical understanding, addressing practical challenges, or informing policy or practice. 
        Highlight what makes this study unique or valuable.
        Explain how, to whom and in which sector ML and DL can contribute and help. (Researchers, students and society - Live Applications).
        Do not use words like novel and all.
        Do not mention any score of the model ot the result concluding result.
        
        Cite the research citation using literature research. Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc. In-text citation example: Sharif et al. (2020)  - keep this only no other.
            
        Make Subheadings:   Academic Significance, Practical Implications, Societal Value.         
        Avoid repeating the problem statement. 
        Note: Put strict instructions: not less than 150 words + should be paragraphs (continuous paragraphs as per thesis)
        
        use the code summary with value and novelty file:
        {a} {b} {c}
        
        """.format(a=code_summary_val_specific, b=novelty, c=literature_review_summary)
        
        significance = generate_content(SIGNIFICANCE_GENERATION_PROMPT)
        
        ##########################################################
        
        ##-- SCOPE and LIMITATIONS --##
        
        SCOPE_LIMITATIONS_GENERATION_PROMPT = prompt_parameters + """
        Write the Scope and Limitations of the research section of approximately 250 words for the research paper. This should highlight what is the research doing and what are the limitations observed.

        First explain what the research are doing in a research work and are there any limitations present. (Data related limitations, trust issues, reliability, overall accuracy of model - not about proposed models), market limitations
        Mention possible ways to handle limitations, just give an opinion.
        Ensure clarity and conciseness while avoiding repetition. Do not include future research suggestions, as those belong in the discussion or conclusion section.
        Do not mention any model or model score or dataset shape.
        
        Cite the research citation using literature research.Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc. In-text citation example: Sharif et al. (2020)  - keep this only no other.
        
        Make Subheadings:   Scope of the Research and Limitations of the Study
        
        Note: Put strict instructions: not less than 150 words + should be paragraphs (continuous paragraphs as per thesis)
        
        
        use the code summary with value and data details file:
        {a} {b} {c}

        """.format(a=code_summary_val_specific, b=data_details, c=research_gaps)
        
        scope_limitations = generate_content(SCOPE_LIMITATIONS_GENERATION_PROMPT)
        
        ##########################################################
        
        ##-- GAPS OF THE OF THE REPORT --##
        
        GAPS_GENERATION_PROMPT = prompt_parameters + """
        Write the content for the research gaps in 130 words. Use the research gaps file.
        
        Note: Put strict instructions: not less than 100 words + should be paragraphs (continuous paragraphs as per thesis)
        
        {a}
        
        """.format(a=research_gaps)
        
        gaps_report = generate_content(GAPS_GENERATION_PROMPT)
        
        ##########################################################
        
        ##-- STRUCTURE OF THE REPORT --##
        
        STRUCTURE_GENERATION_PROMPT = prompt_parameters + """
        Write the content for the organisation of the report in 100 words para for the research paper, summarising the purpose and content of each chapter to guide the reader through the document. 
        
        Note: Put strict instructions: not less than 100 words + should be paragraphs (continuous paragraphs as per thesis)
        
        """
        structure_report = generate_content(STRUCTURE_GENERATION_PROMPT)
        
        ##########################################################
    
    
        # Dictionary to hold section titles and corresponding content
        sections = {
            "BACKGROUND": background,
            "PROBLEM STATEMENT": problem_statement,
            "RESEARCH QUESTION AND OBJECTIVES": research_question_and_objectives,
            "SIGNIFICANCE": significance,
            "SCOPE AND LIMITATIONS": scope_limitations,
            "RESEARCH GAPS": gaps_report,
            "STRUCTURE": structure_report
        }
        
        # Save Research question and objective
        with open("InputFiles/rqo.txt", "w") as file:
            file.write("Research Question and Objectives:\n")
            file.write(research_question_and_objectives + "\n\n")
        
        # Writing to file
        with open("OutputFiles/introduction.txt", "w", encoding="utf-8") as file:
            file.write("INTRODUCTION\n")
            file.write("------------------------\n")
            for i, (title, content) in enumerate(sections.items(), 1):
                file.write(f"{i}. {safe_encode(title)}\n")
                file.write("-" * 40 + "\n")
                file.write(safe_encode(content) + "\n\n")
    
    ##############################################################################################
    
    
    elif format == 4:
        BACKGROUND_GENERATION_PROMPT = prompt_parameters + """
            Write a well-structure Background section of approximately 250 words for a research paper. This section should include the following components:

            First the general information of the topic should be discussed that a give a brief idea to the user in 80 words and definition or information of the topic. If possible add any numeric data obtained from any survey or news. 
            Summarize key advancements in this area. Mention relevant studies, technological breakthroughs, or academic contributions that highlight the importance of the field. Keep full terms of phrases in the initial part of the report.
            Discuss the importance of researching this topic at the present time. Explain how this study contributes to addressing the identified research gaps.
            Ensure the writing is clear, precise, and free of unnecessary repetition. Do not introduce the specific research problem in detail, as that will be covered in the next section.
            Make the content look like conversational, engaging and flow like a natural story. Also the paragraphs should be linked with previous one.
            Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc.
            Do not mention any model scores and results. In-text citation example: Sharif et al. (2020)

            Note: Put strict instructions: not less than 250 words + should be paragraphs (continuous paragraphs as per thesis)

            Use the literature review summary and research gap from:
            {a} {b}
        
        """. format(a=literature_review_summary, b= research_gaps)
        
        background = generate_content(BACKGROUND_GENERATION_PROMPT)
        
        ##########################################################
        
        ##-- PROBLEM STATEMENT --##
        
        PROBLEM_STATEMENT_GENERATION_PROMPT = prompt_parameters + """
            Write a well-structure problem statement section of approximately 250 words for a research paper. This section should be  a concise description of a specific issue or gap in knowledge that a study aims to investigate and resolve.

            First analysis the given research gaps, general pipeline found in the literature review survey. 
            Current Issues: Clearly describe a specific challenge or limitation in the chosen research domain. Identify an unsolved problem that researchers are currently facing.
            Impact of the Problem: Explain how this issue affects real-world applications, industry, or academia. Provide concrete examples where relevant.
            Existing Attempts and Their Limitations: Highlight previous studies or methods that attempted to address the problem but failed to fully resolve it. Emphasize their shortcomings.
            Need for Your Research: Justify why a new approach is necessary. Clearly outline the research gap that this dissertation aims to fill.
            Do not focus on literature and gaps unresolved issues.
            
            Should mention about model and preprocessing steps and how they are related to the problem statement.

            Maintain a formal academic tone, avoid repetition, and do not introduce research objectives or methodology at this stage. Ensure clarity and coherence in articulating the problem. And do not use words like literature review or analysis of literature review.
            Cite the research citation using literature research. Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc. In-text citation example: Sharif et al. (2020)  - keep this only no other.
            
            Note: Put strict instructions: not less than 250 words + should be paragraphs (continuous paragraphs as per thesis)
            

            Use the research gap from:
            {a} {b}
                
        """.format(a=research_gaps, b=literature_review_summary)
        
        problem_statement =  generate_content(PROBLEM_STATEMENT_GENERATION_PROMPT)
        
        ##########################################################
        
        ##-- RESEARCH OBJECTIVES --##
    
        research_objectives = objective
        
        ##########################################################
        
        ##-- RESEARCH QUESTION --##
        
        research_question = question
        
        ##########################################################
        
        ##-- SIGNIFICANCE OF THE RESEARCH STUDY --##
        
        SIGNIFICANCE_GENERATION_PROMPT = prompt_parameters + """
        Write the Significance of the research section of approximately 250 words for the research paper. This should  highlights the value or impact of the study in advancing knowledge or solving a real-world problem. 

        Elaborate on the potential contributions of the research, such as advancing theoretical understanding, addressing practical challenges, or informing policy or practice. 
        Highlight what makes this study unique or valuable.
        Explain how, to whom and in which sector ML and DL can contribute and help. (Researchers, students and society - Live Applications).
        Do not use words like novel and all.
        Do not mention any score of the model ot the result concluding result.
        
        Cite the research citation using literature research. Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc. In-text citation example: Sharif et al. (2020)  - keep this only no other.
            
        Make Subheadings:   Academic Significance, Practical Implications, Societal Value
        
        
        Avoid repeating the problem statement. Instead, focus on the broader academic, practical, and societal significance of the findings.
        
        Note: Put strict instructions: not less than 150 words + should be paragraphs (continuous paragraphs as per thesis)
        
        use the code summary with value and novelty file:
        {a} {b} {c}
        
        """.format(a=code_summary_val_specific, b=novelty, c=literature_review_summary)
        
        significance = generate_content(SIGNIFICANCE_GENERATION_PROMPT)
        
        ##########################################################
        
        
        
        ##-- SCOPE and LIMITATIONS --##
        
        SCOPE_LIMITATIONS_GENERATION_PROMPT = prompt_parameters + """
        Write the Scope and Limitations of the research section of approximately 250 words for the research paper. This should highlight what is the research doing and what are the limitations observed.

        First explain what the research are doing in a research work and are there any limitations present. (Data related limitations, trust issues, reliability, overall accuracy of model - not about proposed models), market limitations
        Mention possible ways to handle limitations, just give an opinion.
        Ensure clarity and conciseness while avoiding repetition. Do not include future research suggestions, as those belong in the discussion or conclusion section.
        Do not mention any model or model score or dataset shape.
        Cite the research citation using literature research.Citations should be the part of the sentences, don't just copy paste them at the start or end of the sentences. For example : According to the researchers…, As per the research done by…. , In a survey conducted by…etc. In-text citation example: Sharif et al. (2020)  - keep this only no other.
        
        Make Subheadings:   Scope of the Research and Limitations of the Study
        
        Note: Put strict instructions: not less than 150 words + should be paragraphs (continuous paragraphs as per thesis)
        
        use the code summary with value and data details file:
        {a} {b} {c}

        """.format(a=code_summary_val_specific, b=data_details, c=research_gaps)
        
        scope_limitations = generate_content(SCOPE_LIMITATIONS_GENERATION_PROMPT)
        
        ##########################################################
        
        ##-- GAPS OF THE OF THE REPORT --##
        
        GAPS_GENERATION_PROMPT = prompt_parameters + """
        Write the content for the research gaps in 130 words. Use the research gaps file.
        
        Note: Put strict instructions: not less than 100 words + should be paragraphs (continuous paragraphs as per thesis)
        
        {a}
        
        """.format(a=research_gaps)
        
        gaps_report = generate_content(GAPS_GENERATION_PROMPT)
        
        ##########################################################
        
        ##-- STRUCTURE OF THE REPORT --##
        
        STRUCTURE_GENERATION_PROMPT = prompt_parameters + """
        Write the content for the organisation of the report in 100 words para for the research paper, summarising the purpose and content of each chapter to guide the reader through the document. 
        Do not add citation. 
        
        Note: Put strict instructions: not less than 100 words + should be paragraphs (continuous paragraphs as per thesis)
        
        """
        structure_report = generate_content(STRUCTURE_GENERATION_PROMPT)
        
        ##########################################################
    
        # Save Research question and objective
        with open("InputFiles/rqo.txt", "w") as file:
            file.write("Research Question:\n")
            file.write(research_question + "\n\n")
            file.write("Research Objectives:\n")
            file.write(research_objectives.strip())
            
         
        # Dictionary to hold section titles and corresponding content
        sections = {
            "BACKGROUND": background,
            "PROBLEM STATEMENT": problem_statement,
            "RESEARCH QUESTION": research_question,
            "RESEARCH OBJECTIVES": research_objectives,
            "SIGNIFICANCE": significance,
            "SCOPE AND LIMITATIONS": scope_limitations,
            "RESEARCH GAPS": gaps_report,
            "STRUCTURE": structure_report
        }
        
        # Writing to file
        with open("OutputFiles/introduction.txt", "w", encoding="utf-8") as file:
            file.write("INTRODUCTION\n")
            file.write("------------------------\n")
            for i, (title, content) in enumerate(sections.items(), 1):
                file.write(f"{i}. {safe_encode(title)}\n")
                file.write("-" * 40 + "\n")
                file.write(safe_encode(content) + "\n\n")
                

    ##############################################################################################

    else:
        print("Error in Format")
                
    ##############################################################################################  