from ai import generate_content
from utils import load_files, load_config
import re

def generate_result_conclusion():
    
    title, literature_review_summary,research_gaps, code_summary, web_app_summary, code_summary_val_specific, novelty, data_details, methodology, research_question_and_objectives, base_paper_summary, result_summary, failed_attempts, web_app_development, web_app_testing_results, prompt_parameters   = load_files()
    
    config = load_config('config.yaml')
    base_paper_citation = config['BASE_PAPER_CITATION']
    format = int(config['FORMAT'])
    
    global performance_evaluation, comparison_with_benchmark
    
    RESULT_PLOT_TITLE_CATEGORY_GENERATION_PROMPT = prompt_parameters + """"
        From the result plot summary, collect all the titles plots.
         
        Use Results Summary from:
        {a}
         
        """.format(a=result_summary)
         
    result_plot_title_and_category = generate_content(RESULT_PLOT_TITLE_CATEGORY_GENERATION_PROMPT)
    
    
    ##-- PERFORMANCE EVALUATION --##
    
    if format == 1:
        
        PERFORMANCE_EVALUATION_GENERATION_PROMPT = prompt_parameters + """
            Write a technical performance evaluation section for my research dissertation. At the beginning, write a short introduction of 30 to 50 words for this section. The introduction should mention that the section follows after performing data collection, EDA, data pre-processing, and model training, and now focuses on analysing the results. The section should be divided into four main subheadings. Please modify the subheadings to better suit the research project topic. Use clear, meaningful titles. 
            Subheading 1: Individual Model Performance (Change heading to match project topic). 
                1. Present a results table showing the performance metrics of all individual models. Give the suitable and relevant table name. Do not use asterisk (*).  
                2. In the explanation: Write two paragraphs discussing the important findings from the table. Strictly do not include or discuss any plot insights (like Confusion Matrix, AUC-ROC Curves, PR Curves, or PR AUC, Actual vs predicted in this part. Mention only a few key metric values, but they should be clearly explained.  
                3. For metrics ranging from 0 to 1, convert them to percentage format using the % symbol. (Up to 2 Decimal Places). 
                4. End this section with a discussion on potential limitations in model performance.
                5. Strictly don’t use parentheses '()' for mentioning metric values. 

            Subheading 2: Visual Comparison of Model Predictions and Trade-offs (Change heading to match project topic). 
                1. Keep the following plots like Confusion Matrix for each model separate, AUC-ROC Curves for each model separate, PR Curves for each model separate, Actual vs predicted for each model separate. 
                2. Provide detailed insights for all plots, at least 30 to 40 words of insights must be there for each plot. Strictly ensure that all metric values are mentioned
                3. Provide 30-40 words of insights for each learning curve plot (Training, validation : accuracy and loss)
                4. Explain all the XAI plots if available and explain thoroughly, at least 80 to 90 words of insights must be there for each plot of models.  
                5. After describing each set of plot insights: On a new line, write the “figure number starting from 5.1 and title in Title Case format”. You may combine plot titles if needed for grouped plots.  
                6. Do not combine any plot explanation.
                7. Ensure the titles are relevant to the project topic and precise. 
                8. Do not use asterisk (*).  
                9. Strictly don’t use parentheses '()' for mentioning metric values.
                10. If additional evaluation plots (such as lift curves, calibration plots, KS-statistic curves, gain charts, etc.) are found, describe them thoroughly in the same format, ensuring metric-based analysis and assign the next figure number with a relevant and clear title. 

            Subheading 3: Comparative Analysis (Change heading to match project topic). 
                1. Then, briefly discuss insights from the remaining individual comparative plots separately, at least 30 to 40 words of insights must be there for each plot. 
                2. Strictly ensure that all metric values are mentioned. For metrics ranging from 0 to 1, convert them to percentage format using the % symbol. (Up to 2 Decimal Places). 
                3. After describing each set of plot insights: On a new line, write the “figure number, continuing from last section and title in Title Case format”. 
                4. Do not use asterisk (*). 
                5. Strictly don’t use parentheses '()' for mentioning metric values. 
                6. Write a paragraph on strengths and weaknesses of each model. 
                7. Include a paragraph that justifies why a particular model performed the best. 
                8. Add another paragraph to state clearly which model is the best, a good choice, and the worst based on performance.  

            Subheading 4: Comparison with Benchmark Research paper (Change heading to match project topic) 
                1. Attachment has benchmarks research paper summary, use it for this section. Compare the research pipeline and result of the base paper with this research work. Word count can go up to 150 words. Strictly don’t use parentheses '()' for mentioning metric values.

            Important Guidelines: 
                1. Use UK English. 
                2. Do not use asterisk (*).
                3. Use commas only when necessary. 
                4. Write in very simple and clear language suitable for a student thesis. Maintain a reflective tone and make sure the content reads like a natural and useful explanation for the reader. 
                5. Do not use any of the following words: leverage, rigor, overall, additionally, furthermore, moreover, nuanced, notably, utilised, foster, pivot, pivotal. 
                6. Strictly don’t use parentheses for mentioning metric values. 
                7. Write them clearly in the sentence. 
     
                   
        Use  Code Summary Value Specific, Result Summary for Table and Plot Summary, Result Plot Title and Category and Base Paper Summary and Base Paper Citation from:
        {a} {b} {c} {d} {e}
        
        """.format(a=code_summary_val_specific, b=result_summary, c=result_plot_title_and_category, d=base_paper_summary, e=base_paper_citation)
        
        performance_evaluation = generate_content(PERFORMANCE_EVALUATION_GENERATION_PROMPT)
         
         
    ##############################################################################################
    
    elif format == 2:
        PERFORMANCE_EVALUATION_GENERATION_PROMPT = prompt_parameters + """
            Write a technical performance evaluation section for my research dissertation.  Begin with a short introduction of 30 to 50 words. The introduction should state that this section follows after data collection, EDA, pre-processing, and model training, and that it now shifts focus to evaluating model performance based on the experimental results. Structure the section under four clear and meaningful subheadings that are tailored to the topic. Each subheading should follow a consistent layout using blocks or short labelled sections where relevant (e.g., “Key Findings,” “Metric Highlights,” “Strengths & Weaknesses”).
            Subheading 1: Individual Model Performance (Change heading to match project topic). 
                1. Make a result table and give a suitable table name. In the discussion: 
                2. Present 2 short labelled paragraphs: “Key Findings” – summarise major metric trends across models without mentioning plots. “Metric Highlights” – cite only a few important metric values (use % format up to 2 decimal places) to support the findings. 
                3. End this section with a separate short paragraph on possible reasons for performance gaps. 
                4. Do not mention plot insights like for Confusion Matrices, AUC-ROC, PR Curves, PR AUC or for Actual vs predicted here. 
                5. Strictly don’t use parentheses for mentioning metric values. 

            Subheading 2 Visual Comparison of Model Predictions and Trade-offs (Change heading to match project topic). 
                Do not generate insights for any plots that are not present in the attachments.

                1. Group the following evaluation plots **only if they are present** in the attachments: Confusion Matrix, AUC-ROC Curves, Precision-Recall (PR) Curves, and Actual vs. Predicted Graphs. For each group:
                - Provide **detailed and balanced insights** across **all models**, ensuring **equal depth of explanation**
                - Each group explanation must be **at least 120 to 130 words**, and include:
                    • Performance trade-offs per model  
                    • All key metric values (e.g. accuracy, precision, recall, F1-score, AUC, sensitivity, specificity) — **do not use parentheses**  
                    • Direct comparisons among models  
                    • Trends or unusual patterns observed

                2. For **each Learning Curve plot** (training and validation accuracy/loss), if present:
                - Write **30 to 40 words of concise insight** per plot
                - Comment on training behavior like overfitting, underfitting, or generalization stability

                3. For **each Explainable AI (XAI) plot** provided (e.g., Grad-CAM, SHAP, LIME), if available:
                - Provide **40 to 50 words** of insights **per model**
                - Do **not combine insights across models**
                - Explain what each plot reveals about the model's decision-making

                4. After each set of plot insights:
                - On a new line, write the **Figure Number** starting from **Figure 5.1** and a **Title Case caption** relevant to the project
                - Refer to figures using phrasings like **“as seen in Figure 5.x”** or **“as visualized in Figure 5.x”**

                5. **Strictly do not** use parentheses for metric values — mention them inline

                6. If **any additional evaluation plots** are present (e.g., Lift Curves, Calibration Plots, KS Statistic Curves, Gain Charts):
                - Follow the same format: 120–130 words, metric-based analysis, assign next figure number and relevant caption

                ➤ Do not assume or hallucinate any plot type that is not in the attachments  
                ➤ Ensure all explanations are complete, accurate, and formatted as instructed

            Subheading 3: Comparative Analysis (Change heading to match project topic). 
                1. Briefly describe remaining comparative plots not already covered. For each, use a short header or bolded label followed by a short paragraph with observations. at least 30 to 40 words of insights should be there for each plot.  
                2. Strictly ensure that all metric values are mentioned and don’t use parentheses for mentioning metric values. Include metric values (use % format) when referenced. 
                3. After describing each set of plot insights: On a new line, write the “figure number, continuing from last section and title in Title Case format”. 
                4. After all plots: Add a labelled paragraph “Strengths and Weaknesses of Each Model” explaining each model’s characteristics. 
                5. Add a paragraph “Why [Model Name] Performed the Best” that justifies top model choice. 
                6. Add a final paragraph “Model Ranking Summary” categorising best, good, and poor-performing models (optionally separate ML and DL categories or any other factor found). 
                7. After describing each set of plot insights: On a new line, write the “figure number starting from 5.1 and title in Title Case format”. You may combine plot titles if needed for grouped plots. 
                8. Do not use asterisk (*). 
                9. Ensure the titles are relevant to the project topic and precise. 
                10. Strictly don’t use parentheses '()' for mentioning metric values.

            Subheading 4: Comparison with Benchmark Research paper (Change heading to match project topic). 
                1. In 120 to 150 words: Compare the research pipeline and results from the benchmark paper with the current study. 
                2. Highlight differences in approach, model selection, or evaluation strategy. 
                3. Clearly indicate any improvements or deviations. 
                4. Strictly don’t use parentheses for mentioning metric values.
            
            Writing Style and Language Guidelines: 
                1. Use UK English. 
                2. Do not use asterisk (*). 
                3. Use commas only when necessary. 
                4. Write in very simple and clear language suitable for a student thesis. Maintain a reflective tone and make sure the content reads like a natural and useful explanation for the reader. 
                5. Do not use any of the following words: leverage, rigor, overall, additionally, furthermore, moreover, nuanced, notably, utilised, foster, pivot, pivotal. 
                6. Strictly don’t use parentheses for mentioning metric values. Write them clearly in the sentence. 
                
  
            
        Use  Code Summary Value Specific, Result Summary for Table and Plot Summary, Result Plot Title and Category and Base Paper Summary and Base Paper Citation from:
        {a} {b} {c} {d} {e}
        
        """.format(a=code_summary_val_specific, b=result_summary, c=result_plot_title_and_category, d=base_paper_summary, e=base_paper_citation)
        
        performance_evaluation = generate_content(PERFORMANCE_EVALUATION_GENERATION_PROMPT)
    
    ##############################################################################################
    
    elif format == 3:
        PERFORMANCE_EVALUATION_GENERATION_PROMPT = prompt_parameters + """
            Write a technical performance evaluation section for my research dissertation. Strictly the word count should be of approximately 900 words. At the beginning, write a short introduction of 30 to 50 words for this section. The introduction should mention that the section follows after performing data collection, EDA, data pre-processing, and model training, and now focuses on analysing the results. The section should be divided into four main subheadings. Please modify the subheadings to better suit the research project topic. Use clear, meaningful titles. 
            Subheading 1: Individual Model Performance (Change heading to match project topic). 
                1. Present a results table showing the performance metrics of all individual models. Give the table a relevant and suitable table name. 
                2. Do not use asterisk (*). 
                3. In the explanation: Write two paragraphs discussing the important findings from the table. Strictly do not include or discuss any plot insights (like Confusion Matrix, AUC-ROC Curves, PR Curves, or PR AUC, Actual vs predicted in this part. Mention only a few key metric values, but they should be clearly explained. For metrics ranging from 0 to 1, convert them to percentage format using the % symbol. (Up to 2 Decimal Places). 
                4. End this section with a discussion on potential limitations in model performance. Strictly don’t use parentheses ‘()’ for mentioning metric values.

            Subheading 2: Visual Comparison of Model Predictions and Trade-offs (Change heading to match project topic). 
                Important Instructions:  
                Only describe and analyze plots that are actually present in the provided attachments. Do not generate or assume insights for missing or unrelated plots.
                1. For each model, **group together** the following plots **if available**:  
                    - Confusion Matrix, AUC-ROC Curve, Precision-Recall (PR) Curve, Actual vs Predicted graph  
                        ➤ Treat each group as representing one model.  
                        ➤ For each model’s grouped plots, provide a **single block of insights with 120 to 130 words**.  
                        ➤ Ensure the explanation includes:  
                            • Detailed metric values such as accuracy, precision, recall, F1-score, AUC, specificity, sensitivity, etc. (**Do not use parentheses for metric values**)  
                            • Model-specific trade-offs and comparative observations  
                            • Any patterns, anomalies, or interesting behaviors in the visualizations  
                        ➤ All models must be given equal weight — do not shorten or combine model sections.
                2. For **each learning curve plot** (training/validation accuracy and loss), provide:  
                    - **30 to 40 words of insight** per plot  
                    - Mention model performance trends like overfitting, underfitting, or convergence behavior, if observed
                3. For **each Explainable AI (XAI) plot** (e.g., Grad-CAM, SHAP, LIME), if present:  
                    - Provide **40 to 50 words of explanation per plot of each model**,
                    - Do not combine explanations — give each XAI plot a dedicated, standalone insight  
                    - Explain how the XAI plot reveals decision patterns, important features, or model reasoning
                4. After each group of plot insights, include a figure reference on a **new line**, formatted as: **Figure 5.x: Title in Title Case**  
                    - Start from **Figure 5.1** and increment sequentially  
                    - Use descriptive, project-specific titles  
                    - Reference each figure inside the text using phrases like **“as seen in Figure 5.x”** or **“as visualized in Figure 5.x”**
                5. Do **not use asterisks (*)** anywhere in the output.
                6. Do **not use parentheses ( )** for any metric values — write values inline, e.g., “recall was 91 percent”.
                7. If **additional evaluation plots** are available (e.g., Lift Curve, Calibration Plot, KS Statistic Curve, Gain Chart):  
                    - Analyze each using the same detailed format as above  
                    - Assign the next sequential **figure number** with an appropriate title

                ➤ Final Note: Strictly follow all format, word count, and metric rules. Do not skip, shorten, or assume any content. Only generate insights based on the actual plots shared.

            Subheading 3: Comparative Analysis (Change heading to match project topic) 
                1. Then, briefly discuss insights from the remaining individual comparative plots separately. at least 30 to 40 words of insights must be there for each plot. 
                2. Strictly ensure that all metric values are mentioned. For metrics ranging from 0 to 1, convert them to percentage format using the % symbol. (Up to 2 Decimal Places). 
                3. After describing each set of plot insights: On a new line, write the “figure number, continuing from last section and title in Title Case format”. 
                4. Do not use asterisk (*). 
                5. Strictly don’t use parentheses '()' for mentioning metric values. 

            Subheading 4: Comparison with Benchmark Research paper (Change heading to match project topic)
                1. Attachment has benchmarks research paper summary, use it for this section. Compare the research pipeline and result of the base paper with this research work. Word count can go up to 150 words. 
                2. Strictly don’t use parentheses for mentioning metric values. 
                3. Write a paragraph on strengths and weaknesses of each model. 
                4. Include a paragraph that justifies why a particular model performed the best. Add another paragraph to state clearly which model is the best, a good choice, and the worst based on performance. 
                5. You may use comparison categories such as traditional vs advanced or ML vs DL models.

            Important Guidelines: 
                1. Use UK English. 
                2. Do not use asterisk (*). 
                3. Use commas only when necessary. 
                4. Write in very simple and clear language suitable for a student thesis. Maintain a reflective tone and make sure the content reads like a natural and useful explanation for the reader. 
                5. Do not use any of the following words: leverage, rigor, overall, additionally, furthermore, moreover, nuanced, notably, utilised, foster, pivot, pivotal. 
                6. Strictly don’t use parentheses for mentioning metric values. 
                7. Write them clearly in the sentence. 
            
        Use  Code Summary Value Specific, Result Summary for Table and Plot Summary, Result Plot Title and Category and Base Paper Summary and Base Paper Citation from:
        {a} {b} {c} {d} {e}
        
        """.format(a=code_summary_val_specific, b=result_summary, c=result_plot_title_and_category, d=base_paper_summary, e=base_paper_citation)
        
        performance_evaluation = generate_content(PERFORMANCE_EVALUATION_GENERATION_PROMPT)
    ##############################################################################################
    
    elif format == 4:
        PERFORMANCE_EVALUATION_GENERATION_PROMPT = prompt_parameters + """
            Write a technical performance evaluation section for my research dissertation. Strictly the word count should be of approximately 900 words. At the beginning, write a short introduction of 30 to 50 words for this section. The introduction should mention that the section follows after performing data collection, EDA, data pre-processing, and model training, and now focuses on analysing the results. The section should be divided into five main subheadings. Please modify the subheadings to better suit the research project topic. Use clear, meaningful titles. 

            Subheading 1: Individual Model Performance (Change heading to match project topic). 
                1. Present a results table showing the performance metrics of all individual models. Give the table a relevant and suitable title. 
                2. In the explanation: Write two paragraphs discussing the important findings from the table. Strictly do not include or discuss any plot insights (like Confusion Matrix, AUC-ROC Curves, PR Curves, or PR AUC, Actual vs predicted in this part. 
                3. Mention only a few key metric values, but they should be clearly explained. 
                4. Strictly don’t use parentheses for mentioning metric values.

            Subheading 2: Visual Comparison of Model Predictions and Trade-offs (Change heading to match project topic) 
                Important Instructions:
                Only describe plots that are actually available in the shared code file or attachments. Do not generate insights for plots that are not present.
                1. Treat the following plot types separately for **each model**:
                    - Confusion Matrix, AUC-ROC Curve, Precision-Recall (PR) Curve, Actual vs. Predicted Plot  
                        ➤ For each plot, provide a **dedicated and detailed insight of at least 50 to 60 words**.  
                        ➤ Ensure the following are strictly included in each explanation:
                            • Key metric values (e.g. accuracy, precision, recall, F1-score, AUC, sensitivity, specificity)  
                            • Inline values only — **do not use parentheses**  
                            • Clear interpretation of the plot's significance to the model's performance  
                        ➤ Do not combine plot insights — each must be discussed separately.
                2. For **each Explainable AI (XAI) plot**, such as Grad-CAM, SHAP, or LIME:
                    - If available, provide a **separate explanation for each XAI plot**, with at least **40 to 50 words**
                    - Do not merge insights across models or plot types
                    - Describe what the plot reveals about the model’s decision-making and focus areas
                3. After explaining each plot:
                    - On a new line, include the figure number and title in this format: **Figure 5.x: Title in Title Case Format**  
                    - Start from **Figure 5.1** and increment sequentially  
                    - Use phrasing like **“as seen in Figure 5.x”** or **“as visualized in Figure 5.x”** when referencing figures in the text  
                    - Titles must be relevant to the project domain and clearly describe the plot content
                4. Do not use any of the following in your output:
                    - Asterisk (*)  
                    - Parentheses for metric values  
                    - Combined or merged plot descriptions
                5. If any **additional evaluation plots** are present (e.g., Lift Curves, Calibration Plots, KS Statistic Curves, Gain Charts):
                    - Follow the same explanation format: 50 to 60 words per plot, with metric-based insights
                    - Assign the next appropriate figure number and a precise title
                ➤ Final Notes:
                - Do not assume or fabricate plots not found in the code or attachments  
                - Every explanation must follow the required word count and include complete metric references  
                - Follow all format, content, and language rules exactly to ensure clarity and consistency

            Subheading 3: Comparative Analysis (Change heading to match project topic) 
                1. Then, briefly discuss insights from the remaining individual comparative plots separately. at least 30 to 40 words of insights must be there for each plot. 
                2. Strictly ensure that all metric values are mentioned. 
                3. After describing each set of plot insights: On a new line, write the “figure number, continuing from last section and title in Title Case format”. 
                4. Do not use asterisk (*). 
                5. Strictly don’t use parentheses '()' for mentioning metric values. 
                6. Write a paragraph on strengths and weaknesses of each model. Include a paragraph that justifies why a particular model performed the best. 
                7. Add another paragraph to state clearly which model is the best, a good choice, and the worst based on performance. 
                8. You may use comparison categories such as traditional vs advanced. 

            Subheading 4: Comparison with Benchmark Research paper (Change heading to match project topic)
                1. Attachment has benchmarks research paper summary, use it for this section. 
                2. Compare the research pipeline and result of the base paper with this research work. Word count can go up to 150 words. 
                3. Strictly don’t use parentheses for mentioning metric values.

            Subheading 5 : Limitations of this Research Work (Change heading to match project topic) 
                1. As per your analysis, write limitations of this research work in 60 words.

            Important Guidelines: 
                1. Use UK English. 
                2. Do not use asterisk (*). 
                3. Use commas only when necessary. 
                4. Write in very simple and clear language suitable for a student thesis. Maintain a reflective tone and make sure the content reads like a natural and useful explanation for the reader. 
                5. Do not use any of the following words: leverage, rigor, overall, additionally, furthermore, moreover, nuanced, notably, utilised, foster, pivot, pivotal. 
                6. Strictly don’t use parentheses for mentioning metric values. Write them clearly in the sentence. 
                

        Use  Code Summary Value Specific, Result Summary for Table and Plot Summary, Result Plot Title and Category and Base Paper Summary and Base Paper Citation from:
        {a} {b} {c} {d} {e}
        
        """.format(a=code_summary_val_specific, b=result_summary, c=result_plot_title_and_category, d=base_paper_summary, e=base_paper_citation)
        
        performance_evaluation = generate_content(PERFORMANCE_EVALUATION_GENERATION_PROMPT)
    
    ##############################################################################################
    
    else: 
        print("Error in Format")
    
    ##########################################################
    
    ##-- WEB APP TESTING --##
    
    WEB_APP_TESTING_GENERATION_PROMPT = prompt_parameters + """
        Write about the web application testing. At the beginning, write a short introduction of 25 to 35 words for this section. Please modify the subheadings to better suit the research project topic. Use clear, meaningful titles. 
        Word count can go up to 200 words. Please read the provided content and write how web app testing was carried out and what were the results received for each test sample. Also we can explain how the code handles errors or unexpected inputs (If taken care of). Don't mention the best model name. After describing each test sample: On a new line, write the “figure number and title of test sample in Title Case format”.  For each figure it should be present. Strictly don’t use parentheses for mentioning metric values. 

        Important Guidelines: 
            1. Use UK English. 
            2. Do not use asterisk (*). 
            3. Use commas only when necessary. 
            4. Write in very simple and clear language suitable for a student thesis. Maintain a reflective tone and make sure the content reads like a natural and useful explanation for the reader. 
            5. Do not use any of the following words: leverage, rigor, overall, additionally, furthermore, moreover, nuanced, notably, utilised, foster, pivot, pivotal. 
            6. Avoid parentheses for metric values. 
            7. Strictly need a content of approximately 200 words.
            
    
    Use Web App Development and Web App Testing Results from:
    {a} {b}
    
    """.format(a=web_app_development, b=web_app_testing_results)
    
    web_app_test_res_content = generate_content(WEB_APP_TESTING_GENERATION_PROMPT)
    
    ##########################################################
    
    ##-- SIGNIFICANCE OF KEY RESULTS --##
    
    SIGNIFICANCE_OF_KEY_RESULTS_GENERATION_PROMPT = prompt_parameters + """
        Write a technical performance evaluation section for my research dissertation. The section should be divided into two main subheadings. Please modify the subheadings to better suit the research project topic. Use clear, meaningful titles. Don't add figure titles in this section.

        Subheading 1: Meaning of Key Findings (Change heading to match project topic) 
            1. Word count can go up to 100 words. 
            2. Highlight how these results align with or differ from your expectations. Emphasize the significance of specific advanced metrics.

        Subheading 2: Business or Real-World Implications (Change heading to match project topic) 
            1. Generate an Interpretation of Results for my research dissertation word count can go up to 200 words.
            2. Discuss how the key findings can be translated into practical applications.
            3. Reflect on the potential benefits and risks of implementing the proposed model(s) in real-world settings.
            4. Consider the ethical, social or business-related impacts of using machine learning.

        Important Guidelines: 
            1. Use UK English. 
            2. Do not use asterisk (*). 
            3. Use commas only when necessary. 
            4. Write in very simple and clear language suitable for a student thesis. Maintain a reflective tone and make sure the content reads like a natural and useful explanation for the reader. 
            5. Do not use any of the following words: leverage, rigor, overall, additionally, furthermore, moreover, nuanced, notably, utilised, foster, pivot, pivotal. 
            6. Avoid parentheses for metric values. Write them clearly in the sentence. For metrics ranging from 0 to 1, convert them to percentage format using the % symbol. (Up to 2 Decimal Places). 
            7. Strictly need a content of approximately 300 words.

    Use performance evaluation and web app testing results from:
    {a} {b}
    
    """.format(a=performance_evaluation, b=web_app_testing_results)
    
    significance_of_key_results = generate_content(SIGNIFICANCE_OF_KEY_RESULTS_GENERATION_PROMPT)
    
    ##########################################################
    
    ##-- FAILED ATTEMPTS --##
    
    FAILED_ATTEMPT_GENERATION_PROMPT = prompt_parameters + """
    Discuss any failed attempts. At the beginning, write a short introduction of 25 to 35 words for this section. Add a performance result table if available. Mention why a particular method is more suitable than others, as per your analysis. Please modify the subheadings to better suit the research project topic. Use clear, meaningful titles. Word count can go up to 100 words. 

    Important Guidelines: 
        1. Use UK English. 
        2. Do not use asterisks. 
        3. Use commas only when necessary. 
        4. Write in very simple and clear language suitable for a student thesis. Maintain a reflective tone and make sure the content reads like a natural and useful explanation for the reader. 
        5. Do not use any of the following words: leverage, rigor, overall, additionally, furthermore, moreover, nuanced, notably, utilised, foster, pivot, pivotal. 
        6. Avoid parentheses for metric values. For metrics ranging from 0 to 1, convert them to percentage format using the % symbol. (Up to 2 Decimal Places). Add figure names and continue figure numbers from the previous section, write it like as seen in or as visualised and likewise. For each plot it should be present. 
        7. Strictly need a content of approximately 100 words.

    
    Use failed attempt file from:
    {a}
    
    """.format(a=failed_attempts)
    
    failed_attempts_content = generate_content(FAILED_ATTEMPT_GENERATION_PROMPT)
    
    ##########################################################
    
    ##-- RESEARCH NOVELTY --##
    
    RESEARCH_NOVELTY_GENERATION_PROMPT = prompt_parameters + """
    Read the provided content carefully and identify the novel contributions of the research work. Based on your analysis, write a clear and concise 300 words of content highlighting the key innovations or unique aspects that distinguish this study. Don't add figure titles in this section.

    Important Guidelines: 
        1. Use UK English. 
        2. Do not use asterisk (*).
        3. Use commas only when necessary. 
        4. Write in very simple and clear language suitable for a student thesis. Maintain a reflective tone and make sure the content reads like a natural and useful explanation for the reader. 
        5. Do not use any of the following words: leverage, rigor, overall, additionally, furthermore, moreover, nuanced, notably, utilised, foster, pivot, pivotal. Avoid parentheses for metric values. 
        6. Avoid parentheses for metric values. For metrics ranging from 0 to 1, convert them to percentage format using the % symbol. (Up to 2 Decimal Places). 
        7. Strictly need a content of approximately 300 words.

    Use Novelty from:
    {a}

    """.format(a=novelty)
    
    novelty_of_research = generate_content(RESEARCH_NOVELTY_GENERATION_PROMPT)
    
    ##########################################################
    
    
    ##-- IF BASE PAPER NOT PRESENT --##
    
    match = re.search(r'Comparison with Benchmark Research paper[:\s]*(.*)', performance_evaluation, re.IGNORECASE)

    if match:
        comparison_with_benchmark = match.group(1).strip()
        print("Match Found")  # Output the extracted text
        # Dictionary to hold section titles and corresponding content
        # print(comparison_with_benchmark)
        
        sections = {
            "PERFORMANCE EVALUATION": performance_evaluation,
            "WEB APP TESTING": web_app_test_res_content,
            "SIGNIFICANCE OF KEY RESULTS": significance_of_key_results,
            "Failed Attempts" : failed_attempts_content,
            "RESEARCH NOVELTY": novelty_of_research,
        }
        
        # Writing to file
        with open("OutputFiles/results.txt", "w") as file:
            file.write("RESULTS\n")
            file.write("------------------------\n")
            for i, (title, content) in enumerate(sections.items(), 1):
                file.write(f"{i}. {title}\n")
                file.write("-" * 40 + "\n")
                file.write(content + "\n\n")
            
    else:
        WHEN_NO_BASE_PAPER_AVAILABLE_PROMPT = prompt_parameters + """
            Generate an Interpretation of Results for my research dissertation word count can go up to 300 words. This section will have three subheadings. (Change heading to match project topic). Don't add figure titles in this section.
                1. Discussion on How Findings Answer the Research Question
                2. Direct correlation between results and research objectives.
                3 Addressing any unexpected findings and their relevance.

            Important Guidelines: 
                1. Use UK English. Do not use asterisks. 
                2. Use commas only when necessary. 
                3. Write in very simple and clear language suitable for a student thesis. 
                4. Maintain a reflective tone and make sure the content reads like a natural and useful explanation for the reader. 
                5. Do not use any of the following words: leverage, rigor, overall, additionally, furthermore, moreover, nuanced, notably, utilised, foster, pivot, pivotal. 
                6. Avoid parentheses for metric values. For metrics ranging from 0 to 1, convert them to percentage format using the % symbol. (Up to 2 Decimal Places). 
                7. Do not use asterisk (*). 
                8. Strictly need a content of approximately 300 words.
                   
        
        Use Code with Summary and Research Question from:
        {a} {b}
        
        """.format(a=code_summary, b=result_summary)
        
        with_no_base_paper = generate_content(WHEN_NO_BASE_PAPER_AVAILABLE_PROMPT)
        
        # Dictionary to hold section titles and corresponding content
        sections = {
            "PERFORMANCE EVALUATION": performance_evaluation,
            "WEB APP TESTING": web_app_test_res_content,
            "SIGNIFICANCE OF KEY RESULTS": significance_of_key_results,
            "Failed Attempts" : failed_attempts_content,
            "WHEN NO BASE PAPER": with_no_base_paper,
            "RESEARCH NOVELTY": novelty_of_research,
        }
        
        # Writing to file
        with open("OutputFiles/results.txt", "w", encoding="utf-8") as file:
            file.write("RESULTS\n")
            file.write("------------------------\n")
            for i, (title, content) in enumerate(sections.items(), 1):
                file.write(f"{i}. {title}\n")
                file.write("-" * 40 + "\n")
                file.write(content + "\n\n")
    
    
    
    ##################################################################################################
    
    ##-- CONCLUSION --##
    
    
    CONCLUSION_GENERATION_PROMPT = prompt_parameters + """
        Generate a summary for the results section of my research, up to 300 words. The summary should address the following aspects: The pipeline and best results. The novelty of the research. Improvement over the base paper. The web application component. Don't add figure titles in this section.

        Important Guidelines: 
            1. Do not use formatting such as bold or italics, and avoid subheadings. 
            2. Write in paragraph form only. 
            3. Do not include any summary statements or conclusions. Focus solely on summarizing the code-related results. 
            4. Use formal, concise language with a logical structure. Include technical explanations where relevant, but do not repeat basic definitions already discussed in the methodology section. 
            5. Put strict instructions: not less than 300 words + should be paragraphs (continuous paragraphs as per thesis).

    Use Code Summary and Novelty  from:
    {a} {b}
    """.format(a=code_summary, b=novelty)
    
    conclusion = generate_content(CONCLUSION_GENERATION_PROMPT)
    
    
    ##########################################################
    
    ##-- FUTURE WORK --##
    
    FUTURE_WORK_GENERATION_PROMPT = prompt_parameters + """
        Generate the "Future Work & Recommendations" subsection in approximately 300 words. This subsection should explore potential directions for future research and provide actionable recommendations to improve the methodology or expand the study’s scope. Structure the content in formal, well-organized paragraphs without subheadings. Focus on technical depth while maintaining clarity. Don't add figure titles in this section. Put strict instructions: not less than 300 words + should be paragraphs (continuous paragraphs as per thesis). Include the following elements: 
            1. Potential Improvements to the Methodology : Suggestions for alternative machine learning models or deep learning architectures. Integration of additional data sources to enhance predictive performance. Refinement of feature selection techniques to improve interpretability and accuracy. Exploration of more advanced evaluation methods for robust model validation.
            2. Suggestions for Further Research : Investigation of the impact of different preprocessing techniques on model performance. Application of research findings to real-world scenarios or specific industry use cases. Consideration of ethical aspects and fairness in model predictions.
        
        Important Guidelines: 
            1. Don't use formatting like bold or italics. and don't give subheadings written in paragraphs. 
            2. Do not mention anything beyond attachments, also don't mention summary in the end. 
            3. Ensure that the content is formal, concise, and structured logically. 
            4. Use technical explanations where needed but avoid repeating basic definitions that are already covered in the methodology section.  
    
    Use code summary value specific file from:
    {a}
    """.format(a=code_summary_val_specific) 
    
    future_work = generate_content(FUTURE_WORK_GENERATION_PROMPT)
    
    # Dictionary to hold section titles and corresponding content
    sections = {
        "CONCLUSION": conclusion,
        "FUTURE WORK": future_work,
    }

    # Writing to file
    with open("OutputFiles/conclusion.txt", "w", encoding="utf-8") as file:
        file.write("CONCLUSION AND FUTURE WORK\n")
        file.write("------------------------\n")
        for i, (title, content) in enumerate(sections.items(), 1):
            file.write(f"{i}. {title}\n")
            file.write("-" * 40 + "\n")
            file.write(content + "\n\n")
            
        