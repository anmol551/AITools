from ai import generate_content
from utils import load_files, load_config
import re
import os


# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL RULES
# ─────────────────────────────────────────────────────────────────────────────

FIGURE_RULE = """
FIGURE PLACEHOLDERS RULE (Apply to ALL sections that discuss plots, charts, or visual outputs):
- Every plot, chart, graph, confusion matrix, ROC curve, learning curve, XAI plot,
  web app screenshot, or any other visual output MUST have a placeholder.
- Use this exact 3-block structure, always in this order, never merged or skipped:

    [Figure 5.X: <short descriptive caption of what the figure shows>]
    Caption: Figure 5.X — <full caption sentence describing the figure in context>
    Insight: <one paragraph of the required word count for this section explaining
              what the figure reveals, key metric values observed, patterns, trade-offs,
              and what conclusion can be drawn — no parentheses for values>

- X is a globally incrementing integer starting from 1 across the ENTIRE results
  section (performance evaluation + web app testing + failed attempts).
  Never reset the counter between subsections or sections.
- Place each 3-block group inline in the text, immediately after the sentence that
  first describes or references that figure.
- Refer to the figure naturally in the sentence before the block using phrases like:
    "as seen in Figure 5.1", "as visualised in Figure 5.2", "shown in Figure 5.3"
- Example:
    "The confusion matrix for the ElasticNet model revealed strong classification
     behaviour across both classes, as seen in Figure 5.1."
    [Figure 5.1: Confusion Matrix for ElasticNet Regressor]
    Caption: Figure 5.1 — Confusion matrix showing the classification performance
             of the ElasticNet model on the test set of 4,000 samples.
    Insight: The confusion matrix shows that the ElasticNet model correctly
             classified 3,412 instances as low risk and 487 as high risk.
             A total of 101 false positives and 0 false negatives were observed,
             indicating a strong recall of 100 percent for the high-risk class,
             though precision was slightly reduced at 82.8 percent.

- Do NOT group figures at the end of a section — each must appear inline.
- Do NOT use [FIG_X], Figure 4.X, or any other format — only [Figure 5.X: caption].
- Do NOT skip any figure — every visual output present in the result summary must appear.
- Insight word count per figure must match the word count required by that subsection's
  instructions (e.g., 30-40 words for learning curves, 80-90 words for XAI plots,
  120-130 words for grouped model evaluation plots).
"""

COMMON_GUIDELINES = """
Important Guidelines:
    1. Use UK English.
    2. Do not use asterisk (*).
    3. Use commas only when necessary.
    4. Write in very simple and clear language suitable for a student thesis.
       Maintain a reflective tone so the content reads like a natural explanation.
    5. Do not use any of the following words: leverage, rigor, overall, additionally,
       furthermore, moreover, nuanced, notably, utilised, foster, pivot, pivotal.
    6. Strictly do not use parentheses for mentioning metric values — write them
       inline in the sentence.
    7. For metrics ranging from 0 to 1, convert them to percentage format using the
       % symbol, up to 2 decimal places.
"""


# ─────────────────────────────────────────────────────────────────────────────
# PERFORMANCE EVALUATION PROMPTS  (one per format)
# ─────────────────────────────────────────────────────────────────────────────

def build_performance_evaluation_prompt(
    prompt_parameters, format_,
    code_summary_val_specific, result_summary,
    result_plot_title_and_category, base_paper_summary, base_paper_citation
) -> str:

    shared_data = """
Use Code Summary Value Specific, Result Summary, Result Plot Title and Category,
Base Paper Summary, and Base Paper Citation from:
{a} {b} {c} {d} {e}
""".format(
        a=code_summary_val_specific,
        b=result_summary,
        c=result_plot_title_and_category,
        d=base_paper_summary,
        e=base_paper_citation,
    )

    # ── FORMAT 1 ────────────────────────────────────────────────────────────
    if format_ == 1:
        body = """
Write a technical performance evaluation section for my research dissertation.
Begin with a short introduction of 30 to 50 words stating that this section follows
data collection, EDA, preprocessing, and model training, and now focuses on results.
Divide the section into four subheadings tailored to the research topic.

{figure_rule}

Subheading 1: Individual Model Performance (Change heading to match project topic)
    1. Present a results table for all individual models with a suitable table name.
       Do not use asterisk (*).
    2. Write two paragraphs on important findings from the table only — do not
       discuss plot insights (Confusion Matrix, AUC-ROC, PR Curves, Actual vs Predicted).
    3. Mention only a few key metric values, clearly explained.
    4. For metrics 0-1 use % format up to 2 decimal places.
    5. End with a paragraph on potential limitations in model performance.
    6. Do not use parentheses for metric values.

Subheading 2: Visual Comparison of Model Predictions and Trade-offs
               (Change heading to match project topic)
    1. Keep the following plots separate for each model: Confusion Matrix, AUC-ROC Curve,
       PR Curve, Actual vs Predicted.
    2. Apply the FIGURE PLACEHOLDERS RULE for every plot — place each 3-block group
       inline immediately after the sentence describing that plot.
    3. Each insight paragraph must be at least 30 to 40 words and must state all
       metric values. Do not use parentheses for metric values.
    4. For each learning curve plot provide 30 to 40 words of insight per plot,
       commenting on overfitting, underfitting, or generalisation.
    5. For each XAI plot provide 80 to 90 words of insight per model explaining
       feature importance and decision patterns.
    6. If additional evaluation plots are present (lift curves, calibration plots,
       KS-statistic curves, gain charts), describe them in the same format and assign
       the next figure number.
    7. Do not combine plot explanations. Do not assume plots not in the result summary.

Subheading 3: Comparative Analysis (Change heading to match project topic)
    1. Discuss remaining comparative plots separately — at least 30 to 40 words each.
    2. Apply the FIGURE PLACEHOLDERS RULE for every comparative plot inline.
    3. All metric values must be mentioned. Use % format. No parentheses.
    4. Write a paragraph on strengths and weaknesses of each model.
    5. Write a paragraph justifying why the best model performed best.
    6. Write a paragraph stating clearly the best, acceptable, and worst models.

Subheading 4: Comparison with Benchmark Research Paper
               (Change heading to match project topic)
    1. Compare the pipeline and results of the benchmark paper with this research.
       Word count up to 150 words.
    2. Do not use parentheses for metric values.
"""

    # ── FORMAT 2 ────────────────────────────────────────────────────────────
    elif format_ == 2:
        body = """
Write a technical performance evaluation section for my research dissertation.
Begin with a short introduction of 30 to 50 words stating that this section follows
data collection, EDA, preprocessing, and model training, and shifts focus to evaluating
results. Use four subheadings tailored to the topic with consistent labelled blocks
(e.g., Key Findings, Metric Highlights, Strengths and Weaknesses).

{figure_rule}

Subheading 1: Individual Model Performance (Change heading to match project topic)
    1. Make a result table with a suitable name.
    2. Write two short labelled paragraphs:
       "Key Findings" — summarise major metric trends without mentioning plots.
       "Metric Highlights" — cite only a few key values in % format up to 2 decimal places.
    3. End with a short paragraph on possible reasons for performance gaps.
    4. Do not mention plot insights here. Do not use parentheses for metric values.

Subheading 2: Visual Comparison of Model Predictions and Trade-offs
               (Change heading to match project topic)
    1. Group the following plots per model if present: Confusion Matrix, AUC-ROC Curve,
       PR Curve, Actual vs Predicted. For each group:
       - Apply the FIGURE PLACEHOLDERS RULE — place each 3-block group inline.
       - Insight must be 120 to 130 words covering all metric values, trade-offs,
         direct model comparisons, and any unusual patterns.
    2. For each learning curve plot provide 30 to 40 words of insight per plot.
       Comment on training behaviour like overfitting or generalisation stability.
    3. For each XAI plot provide 40 to 50 words of insight per model.
       Do not combine insights across models.
    4. If additional evaluation plots are present assign the next figure number
       and provide 120 to 130 words of metric-based analysis.
    5. Do not generate insights for any plot not in the result summary.

Subheading 3: Comparative Analysis (Change heading to match project topic)
    1. Describe remaining comparative plots separately with 30 to 40 words each.
    2. Apply the FIGURE PLACEHOLDERS RULE for every comparative plot inline.
    3. All metric values must be mentioned. Use % format. No parentheses.
    4. Add a labelled paragraph "Strengths and Weaknesses of Each Model".
    5. Add a paragraph "Why [Model Name] Performed the Best".
    6. Add a paragraph "Model Ranking Summary" categorising best, good, and poor models.

Subheading 4: Comparison with Benchmark Research Paper
               (Change heading to match project topic)
    1. Compare the pipeline and results of the benchmark paper with this research
       in 120 to 150 words.
    2. Highlight differences in approach, model selection, and evaluation strategy.
    3. Clearly indicate any improvements or deviations.
    4. Do not use parentheses for metric values.
"""

    # ── FORMAT 3 ────────────────────────────────────────────────────────────
    elif format_ == 3:
        body = """
Write a technical performance evaluation section for my research dissertation.
Target approximately 900 words total. Begin with a short introduction of 30 to 50 words.
Divide into four subheadings tailored to the research topic.

{figure_rule}

Subheading 1: Individual Model Performance (Change heading to match project topic)
    1. Present a results table for all models with a relevant table name.
    2. Write two paragraphs on important findings — no plot insights here.
    3. Mention only key metric values. Use % format up to 2 decimal places.
    4. End with potential limitations. Do not use parentheses for metric values.

Subheading 2: Visual Comparison of Model Predictions and Trade-offs
               (Change heading to match project topic)
    Only describe plots actually present in the result summary — do not assume others.
    1. For each model group Confusion Matrix, AUC-ROC Curve, PR Curve, and
       Actual vs Predicted together if available:
       - Apply the FIGURE PLACEHOLDERS RULE — place each 3-block group inline.
       - Insight must be 120 to 130 words covering accuracy, precision, recall,
         F1-score, AUC, specificity, sensitivity, trade-offs, and anomalies.
       - All models must receive equal depth — do not shorten any model's section.
    2. For each learning curve plot provide 30 to 40 words of insight per plot.
       Mention convergence behaviour, overfitting, or underfitting if observed.
    3. For each XAI plot provide 40 to 50 words per model per plot.
       Do not combine across models. Explain decision patterns and feature focus.
    4. For additional evaluation plots follow the same format and assign next figure number.

Subheading 3: Comparative Analysis (Change heading to match project topic)
    1. Discuss remaining comparative plots separately — at least 30 to 40 words each.
    2. Apply the FIGURE PLACEHOLDERS RULE for every comparative plot inline.
    3. All metric values must be mentioned. Use % format. No parentheses.
    4. Write a paragraph on strengths and weaknesses of each model.
    5. Write a paragraph justifying why the best model performed best.
    6. Add a paragraph stating the best, acceptable, and worst models by performance.

Subheading 4: Comparison with Benchmark Research Paper
               (Change heading to match project topic)
    1. Compare pipeline and results of benchmark paper with this research up to 150 words.
    2. Do not use parentheses for metric values.
    3. Write a paragraph on strengths and weaknesses of each model.
    4. Write a paragraph justifying the best model.
    5. Write a paragraph clearly ranking best, acceptable, and worst models.
"""

    # ── FORMAT 4 ────────────────────────────────────────────────────────────
    elif format_ == 4:
        body = """
Write a technical performance evaluation section for my research dissertation.
Target approximately 900 words total. Begin with a short introduction of 30 to 50 words.
Divide into five subheadings tailored to the research topic.

{figure_rule}

Subheading 1: Individual Model Performance (Change heading to match project topic)
    1. Present a results table for all models with a relevant table name.
    2. Write two paragraphs on findings from the table — no plot insights here.
    3. Mention only a few key metric values, clearly explained.
    4. Do not use parentheses for metric values.

Subheading 2: Visual Comparison of Model Predictions and Trade-offs
               (Change heading to match project topic)
    Only describe plots actually present in the result summary — do not assume others.
    1. Treat each of the following separately per model if available:
       Confusion Matrix, AUC-ROC Curve, PR Curve, Actual vs Predicted.
       - Apply the FIGURE PLACEHOLDERS RULE — place each 3-block group inline.
       - Insight must be 50 to 60 words per plot covering key metric values,
         model-specific trade-offs, and interpretation of the plot's significance.
       - Do not combine plot insights — each must be discussed separately.
    2. For each XAI plot provide 40 to 50 words per model per plot.
       Do not merge insights across models or plot types.
    3. For additional evaluation plots follow the same format and assign next figure number.
    4. Do not use asterisk (*) or parentheses for metric values anywhere.

Subheading 3: Comparative Analysis (Change heading to match project topic)
    1. Discuss remaining comparative plots separately — at least 30 to 40 words each.
    2. Apply the FIGURE PLACEHOLDERS RULE for every comparative plot inline.
    3. All metric values must be mentioned. No parentheses.
    4. Write a paragraph on strengths and weaknesses of each model.
    5. Write a paragraph justifying why the best model performed best.
    6. Add a paragraph clearly ranking best, acceptable, and worst models.

Subheading 4: Comparison with Benchmark Research Paper
               (Change heading to match project topic)
    1. Compare pipeline and results of benchmark paper with this research up to 200 words.
    2. Do not use parentheses for metric values.

Subheading 5: Limitations of this Research Work
               (Change heading to match project topic)
    1. Write limitations of this research work in approximately 60 words.
"""

    else:
        raise ValueError(f"Unknown format: {format_}. Must be 1, 2, 3, or 4.")

    body = body.format(figure_rule=FIGURE_RULE)
    return prompt_parameters + body + COMMON_GUIDELINES + shared_data


# ─────────────────────────────────────────────────────────────────────────────
# REMAINING SECTION PROMPT BUILDERS
# ─────────────────────────────────────────────────────────────────────────────

def build_web_app_testing_prompt(
    prompt_parameters, web_app_development, web_app_testing_results
) -> str:
    return prompt_parameters + f"""
Write about web application testing for my research dissertation.
Begin with a short introduction of 25 to 35 words.
Modify subheadings to suit the research topic. Use clear, meaningful titles.
Target approximately 200 words total.

{FIGURE_RULE}

Instructions:
    1. Describe how web app testing was carried out and what results were received
       for each test sample.
    2. Explain how the system handles errors or unexpected inputs if applicable.
    3. Do not mention the best model name.
    4. For each test sample, apply the FIGURE PLACEHOLDERS RULE — place the full
       3-block structure inline immediately after describing that test case.
       The insight for each test sample figure must be 30 to 40 words describing
       the input used, the output received, and whether it matched expectations.
    5. Do not use parentheses for metric values.

{COMMON_GUIDELINES}

Use Web App Development and Web App Testing Results from:
{web_app_development} {web_app_testing_results}
"""


def build_significance_prompt(
    prompt_parameters, performance_evaluation, web_app_testing_results
) -> str:
    return prompt_parameters + f"""
Write a significance of key results section for my research dissertation.
Divide into two subheadings tailored to the research topic.
Do not add figure placeholders in this section.

Subheading 1: Meaning of Key Findings (Change heading to match project topic)
    1. Up to 100 words.
    2. Highlight how results align with or differ from expectations.
    3. Emphasise the significance of specific advanced metrics.

Subheading 2: Business or Real-World Implications (Change heading to match project topic)
    1. Up to 200 words.
    2. Discuss how key findings translate into practical applications.
    3. Reflect on potential benefits and risks of implementing the model in real-world settings.
    4. Consider ethical, social, or business-related impacts of using machine learning.

{COMMON_GUIDELINES}
    8. Strictly approximately 300 words total.

Use performance evaluation and web app testing results from:
{performance_evaluation} {web_app_testing_results}
"""


def build_failed_attempts_prompt(prompt_parameters, failed_attempts) -> str:
    return prompt_parameters + f"""
Discuss any failed attempts in my research dissertation.
Begin with a short introduction of 25 to 35 words.
Add a performance result table if available.
Mention why a particular method is more suitable than others.
Modify subheadings to suit the research topic. Target approximately 100 words.

{FIGURE_RULE}

Instructions:
    1. For any plots related to failed attempts, apply the FIGURE PLACEHOLDERS RULE
       inline — continue the global figure counter from the previous section.
    2. The insight for each failed attempt figure must be 30 to 40 words.
    3. Do not use parentheses for metric values.

{COMMON_GUIDELINES}
    8. Strictly approximately 100 words.

Use failed attempts file from:
{failed_attempts}
"""


def build_research_novelty_prompt(prompt_parameters, novelty) -> str:
    return prompt_parameters + f"""
Read the provided content and identify the novel contributions of this research.
Write a clear and concise highlight of key innovations and unique aspects that
distinguish this study. Do not add figure placeholders in this section.

{COMMON_GUIDELINES}
    8. Strictly approximately 300 words.

Use novelty from:
{novelty}
"""


def build_when_no_base_paper_prompt(
    prompt_parameters, code_summary, result_summary
) -> str:
    return prompt_parameters + f"""
Generate an Interpretation of Results for my research dissertation up to 300 words.
Divide into three subheadings tailored to the research topic.
Do not add figure placeholders in this section.

    1. Discussion on How Findings Answer the Research Question
    2. Direct correlation between results and research objectives.
    3. Addressing any unexpected findings and their relevance.

{COMMON_GUIDELINES}
    8. Strictly approximately 300 words.

Use code summary and research question from:
{code_summary} {result_summary}
"""


def build_conclusion_prompt(prompt_parameters, code_summary, novelty) -> str:
    return prompt_parameters + f"""
Generate a summary for the results section of my research up to 300 words.
Address: the pipeline and best results, the novelty of the research, improvement over
the base paper, and the web application component.
Do not add figure placeholders in this section.

Instructions:
    1. Do not use formatting such as bold or italics. No subheadings.
    2. Write in paragraph form only.
    3. Do not include summary statements or conclusions — focus on code-related results.
    4. Use formal, concise language with logical structure.
    5. Include technical explanations where relevant but do not repeat definitions
       from the methodology section.
    6. Strictly not less than 300 words. Write in continuous paragraphs.

Use code summary and novelty from:
{code_summary} {novelty}
"""


def build_future_work_prompt(prompt_parameters, code_summary_val_specific) -> str:
    return prompt_parameters + f"""
Generate the Future Work and Recommendations subsection in approximately 300 words.
Explore potential directions for future research and provide actionable recommendations.
Write in formal, well-organised paragraphs without subheadings.
Do not add figure placeholders in this section.

Include the following elements:
    1. Potential Improvements to the Methodology:
       - Alternative ML/DL models or architectures.
       - Integration of additional data sources.
       - Refinement of feature selection for better interpretability.
       - More advanced evaluation methods for robust validation.
    2. Suggestions for Further Research:
       - Impact of different preprocessing techniques on model performance.
       - Application to real-world scenarios or industry use cases.
       - Ethical aspects and fairness in model predictions.

Instructions:
    1. Do not use bold, italics, or subheadings — write in paragraphs.
    2. Do not mention anything beyond the provided content.
    3. Ensure content is formal, concise, and logically structured.
    4. Avoid repeating basic definitions already covered in methodology.
    5. Strictly not less than 300 words.

Use code summary value specific from:
{code_summary_val_specific}
"""


# ─────────────────────────────────────────────────────────────────────────────
# OUTPUT WRITER
# ─────────────────────────────────────────────────────────────────────────────

def write_output(filepath: str, label: str, sections: dict):
    """Write a multi-section output file with UTF-8 to ASCII fallback."""
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

    def _write(encoding, errors):
        with open(filepath, "w", encoding=encoding, errors=errors) as f:
            f.write(f"{label}\n")
            f.write("------------------------\n")
            for i, (section_title, content) in enumerate(sections.items(), 1):
                f.write(f"{i}. {section_title}\n")
                f.write("-" * 40 + "\n")
                safe = (
                    content if isinstance(content, str)
                    else str(content).encode(encoding, errors).decode(encoding)
                )
                f.write(safe + "\n\n")

    try:
        _write("utf-8", "replace")
        print(f"{label} written successfully (UTF-8): {filepath}")
    except UnicodeEncodeError as e:
        print(f"UTF-8 error for {label}: {e} — retrying.")
        _write("utf-8", "replace")
    except Exception as e:
        print(f"Unexpected error for {label}: {e} — ASCII fallback.")
        _write("ascii", "replace")


def safe_generate(prompt: str) -> str:
    """Generate content with Unicode fallback."""
    try:
        return generate_content(prompt)
    except UnicodeEncodeError as e:
        print(f"Unicode error during generation: {e} — retrying with ASCII prompt.")
        return generate_content(prompt.encode('ascii', 'ignore').decode('ascii'))


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def generate_result_conclusion():

    (title, literature_review_summary, research_gaps, code_summary, web_app_summary,
     code_summary_val_specific, novelty, data_details, methodology,
     research_question_and_objectives, base_paper_summary, result_summary,
     failed_attempts, web_app_development, web_app_testing_results,
     prompt_parameters) = load_files()

    config              = load_config('config.yaml')
    base_paper_citation = config['BASE_PAPER_CITATION']
    format_             = int(config['FORMAT'])

    # ── Step 1: Collect all result plot titles ─────────────────────────────
    PLOT_TITLE_PROMPT = prompt_parameters + f"""
From the result plot summary, collect all plot titles.

Use Results Summary from:
{result_summary}
"""
    result_plot_title_and_category = safe_generate(PLOT_TITLE_PROMPT)

    # ── Step 2: Performance Evaluation ────────────────────────────────────
    PERFORMANCE_PROMPT = build_performance_evaluation_prompt(
        prompt_parameters              = prompt_parameters,
        format_                        = format_,
        code_summary_val_specific      = code_summary_val_specific,
        result_summary                 = result_summary,
        result_plot_title_and_category = result_plot_title_and_category,
        base_paper_summary             = base_paper_summary,
        base_paper_citation            = base_paper_citation,
    )
    performance_evaluation = safe_generate(PERFORMANCE_PROMPT)

    # ── Step 3: Web App Testing ────────────────────────────────────────────
    web_app_test_res_content = safe_generate(
        build_web_app_testing_prompt(
            prompt_parameters, web_app_development, web_app_testing_results
        )
    )

    # ── Step 4: Significance of Key Results ───────────────────────────────
    significance_of_key_results = safe_generate(
        build_significance_prompt(
            prompt_parameters, performance_evaluation, web_app_testing_results
        )
    )

    # ── Step 5: Failed Attempts ────────────────────────────────────────────
    failed_attempts_content = safe_generate(
        build_failed_attempts_prompt(prompt_parameters, failed_attempts)
    )

    # ── Step 6: Research Novelty ───────────────────────────────────────────
    novelty_of_research = safe_generate(
        build_research_novelty_prompt(prompt_parameters, novelty)
    )

    # ── Step 7: Results file — check for benchmark section ────────────────
    match = re.search(
        r'Comparison with Benchmark Research paper[:\s]*(.*)',
        performance_evaluation,
        re.IGNORECASE
    )

    if match:
        print("Benchmark comparison section found — writing results with it.")
        result_sections = {
            "PERFORMANCE EVALUATION":      performance_evaluation,
            "WEB APP TESTING":             web_app_test_res_content,
            "SIGNIFICANCE OF KEY RESULTS": significance_of_key_results,
            "FAILED ATTEMPTS":             failed_attempts_content,
            "RESEARCH NOVELTY":            novelty_of_research,
        }
    else:
        print("No benchmark section found — generating interpretation of results instead.")
        with_no_base_paper = safe_generate(
            build_when_no_base_paper_prompt(
                prompt_parameters, code_summary, result_summary
            )
        )
        result_sections = {
            "PERFORMANCE EVALUATION":      performance_evaluation,
            "WEB APP TESTING":             web_app_test_res_content,
            "SIGNIFICANCE OF KEY RESULTS": significance_of_key_results,
            "FAILED ATTEMPTS":             failed_attempts_content,
            "WHEN NO BASE PAPER":          with_no_base_paper,
            "RESEARCH NOVELTY":            novelty_of_research,
        }

    write_output("OutputFiles/results.txt", "RESULTS", result_sections)

    # ── Step 8: Conclusion ─────────────────────────────────────────────────
    conclusion = safe_generate(
        build_conclusion_prompt(prompt_parameters, code_summary, novelty)
    )

    # ── Step 9: Future Work ────────────────────────────────────────────────
    future_work = safe_generate(
        build_future_work_prompt(prompt_parameters, code_summary_val_specific)
    )

    write_output(
        "OutputFiles/conclusion.txt",
        "CONCLUSION AND FUTURE WORK",
        {
            "CONCLUSION":  conclusion,
            "FUTURE WORK": future_work,
        }
    )
