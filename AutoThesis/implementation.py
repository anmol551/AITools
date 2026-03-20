from ai import generate_content
from utils import load_files, paper_cite, load_config
import os

def generate_implementation():
    title, literature_review_summary, research_gaps, code_summary, web_app_summary, \
    code_summary_val_specific, novelty, data_details, methodology, \
    research_question_and_objectives, base_paper_summary, result_summary, \
    failed_attempts, web_app_development, web_app_testing_results, \
    prompt_parameters = load_files()

    paper_citation = paper_cite()
    title_and_citation = paper_citation[['title', 'citation']]

    config = load_config('config.yaml')
    format = int(config['FORMAT'])

    # Load pipeline file — used to drive dynamic section generation
    pipeline_path = config.get('PIPELINE', 'InputFiles/pipeline.txt')
    try:
        with open(pipeline_path, 'r', encoding='utf-8') as f:
            pipeline_content = f.read()
    except FileNotFoundError:
        pipeline_content = ""
        print(f"Warning: Pipeline file not found at '{pipeline_path}'.")

    IMPLEMENTATION_GENERATION_PROMPT = prompt_parameters + """
    Generate an implementation section of my research report.

    ══════════════════════════════════════════════════════════
    PIPELINE CONTENT (read carefully before generating):
    {pipeline}
    ══════════════════════════════════════════════════════════

    SECTION GENERATION RULES:
    1. Read the pipeline content above carefully.
    2. Generate the FIXED subsections listed below (always present).
    3. Then identify ALL additional components present in the pipeline
       (e.g., Feature Selection, Feature Engineering, Class Balancing,
       Hyperparameter Tuning, LLM Integration, Web Application, XAI, etc.)
       and generate a dedicated subsection for EACH one found.
    4. Place subsections in pipeline order:
       - Components before model training go between Data Preprocessing
         and Model Training.
       - Components after model training go between Model Training
         and Challenges And Solutions.
    5. Do NOT skip any pipeline component — every stage must have a section.
    6. Number all subsections sequentially.

    ══════════════════════════════════════════════════════════
    FIGURE PLACEHOLDERS RULE (apply to EDA, Preprocessing, Model Training,
    and any section that produces visual output):
    Every plot, chart, graph, or screenshot MUST have a placeholder using
    this exact 3-block structure placed INLINE immediately after the sentence
    that describes the figure:

        [Figure 4.X: short caption]
        Caption: Figure 4.X — full caption sentence
        Insight: one paragraph of 60-80 words explaining what the figure
                 reveals, key values, patterns, and conclusions

    X increments globally across the entire implementation section.
    Never reset between subsections. Use ONLY [Figure 4.X: caption] format.
    ══════════════════════════════════════════════════════════

    ══════════════════════════════════════════════════════════
    SPECIFICITY RULE (apply to ALL subsections):
    Every technique must be named EXACTLY as used in the code.
    Never use generic descriptions.
        WRONG  → "normalisation was applied"
        CORRECT → "StandardScaler was applied to 13 continuous features"
        WRONG  → "a neural network was trained"
        CORRECT → "Conv1D with 32 filters, kernel_size=2, relu activation,
                   trained for 50 epochs with batch_size=32, Adam optimizer"
    State every parameter value explicitly — do not omit any.
    ══════════════════════════════════════════════════════════

    ── FIXED SUBSECTION 1 : Statistical Analysis (~100 words) ─────────────
    Change heading to match project topic.
        1. Begin with one introductory sentence.
        2. Describe statistical characteristics: total count, data types,
           mean, standard deviation, minimum, maximum, quartiles.
        3. Include all values. No parentheses, asterisks, or special
           formatting around values.
        4. Do not mention code or code execution.
        5. No citations. Follow the SPECIFICITY RULE.
        6. Strictly approximately 100 words.

    ── FIXED SUBSECTION 2 : EDA (~600 words) ──────────────────────────────
    Change heading to match project topic.
        1. Begin with one introductory sentence connecting to previous section.
        2. Include ONLY figures from the EDA stage — no preprocessing,
           feature engineering, or model plots.
        3. For each EDA plot apply the FIGURE PLACEHOLDERS RULE inline.
        4. Each insight paragraph: 60-80 words, all numerical values stated,
           no parentheses for values.
        5. Do not refer to axes labels unless the plot is complex.
        6. No summary at the end. No citations.
        7. Do not use "this" or "lastly" to start a sentence.
        8. Do not mention plot names at the start of sentences.
        9. Follow the SPECIFICITY RULE.
        10. Strictly approximately 600 words.

    ── FIXED SUBSECTION 3 : Data Preprocessing ────────────────────────────
    Change heading to match project topic.
        1. Start with one introductory sentence.
        2. One subheading per technique (~100 words each, always 2
           paragraphs, past tense).
        3. Name the EXACT method used under each subheading.
           Follow the SPECIFICITY RULE strictly.
        4. For any preprocessing plot apply the FIGURE PLACEHOLDERS RULE.
        5. No citations. Past tense.

    ── DYNAMIC SUBSECTIONS (pre-model training) ───────────────────────────
    For each pipeline stage that occurs BEFORE model training
    (e.g., Feature Selection, Feature Engineering, Class Balancing,
    Hyperparameter Tuning, or any other component in the pipeline):

    Generate a dedicated subsection (~150 words, always 2 paragraphs,
    past tense):
        - Paragraph 1: How it was implemented — exact class names,
          parameter names, and parameter values.
        - Paragraph 2: What was achieved, any plots (apply FIGURE
          PLACEHOLDERS RULE if applicable).
        - Follow the SPECIFICITY RULE for all values.
        - No citations.

    ── FIXED SUBSECTION : Model Training ──────────────────────────────────
    Change heading to match project topic.
        1. Begin with one introductory sentence.
        2. For EACH model (~150-180 words, always 2 paragraphs, past tense):
            - Name the exact class, every parameter, and every value.
            - Example: "Conv1D with 32 filters, kernel_size=2, relu
              activation, BatchNormalization, Conv1D with 64 filters,
              kernel_size=2, relu, BatchNormalization, Flatten, Dense with
              64 units and relu, Dropout at 0.3, Dense with 1 unit output,
              trained 50 epochs, batch_size=32, validation_split=0.2,
              Adam optimizer."
        3. For EACH model's training plots apply FIGURE PLACEHOLDERS RULE.
        4. No model scores or results. No citations. Past tense.
        5. Follow the SPECIFICITY RULE.

    ── DYNAMIC SUBSECTIONS (post-model training) ──────────────────────────
    For each pipeline stage that occurs AFTER model training
    (e.g., LLM Integration, Web Application, XAI, or any other component
    in the pipeline):

    Generate a dedicated subsection in past tense. Requirements by type:

    LLM Integration (~180 words, 2 paragraphs):
        - Exact model name, API used, prompt structure, key parameters
          with exact values (temperature, max_tokens, etc.).
        - How input is prepared, what the API returns, and how that
          output is used in the application.
        - Follow the SPECIFICITY RULE. No citations. No scores.

    Web Application Development (~200 words, 2 paragraphs):
        - Exact framework used and key configurations.
        - UI components, number of input fields, types of fields,
          output display logic, business rules applied.
        - Include figure placeholders for web app screenshots
          using FIGURE PLACEHOLDERS RULE.
        - Do not mention function names or best model name.
        - No citations. Follow the SPECIFICITY RULE.

    XAI Implementation (~150 words, 2 paragraphs):
        - Exact XAI technique name, which models it was applied to,
          all parameters and their values.
        - What the output visualisation shows.
        - Include figure placeholders for XAI plots.
        - No scores. No citations. Follow the SPECIFICITY RULE.

    Any other post-model component: ~150 words, 2 paragraphs, past tense,
    exact implementation details, SPECIFICITY RULE applied.

    ── FIXED LAST SUBSECTION : Challenges And Solutions (~150 words) ───────
        1. Technical challenges faced and solutions implemented.
        2. Name exact methods, classes, or workarounds used.
        3. Citations for one or two challenges from the citation file.
           Do not use paper titles. Example: Sharif et al. (2020).
           Embed citations in sentences, not at start or end.
        4. Strictly approximately 150 words. Past tense.
        5. Follow the SPECIFICITY RULE.

    ══════════════════════════════════════════════════════════
    IMPORTANT FINAL CHECKS before finishing:
    - Confirm EVERY pipeline stage has a corresponding subsection.
    - Confirm LLM Integration is present if LLM appears in the pipeline.
    - Confirm Web Application is present if a web app appears in the pipeline.
    - Confirm no section is missing, merged, or out of order.
    - Use commas only when necessary.
    ══════════════════════════════════════════════════════════

    Use code summary value specific, web app summary, and citations from:
    {a} {b} {c}
    """.format(
        pipeline = pipeline_content,
        a        = code_summary_val_specific,
        b        = web_app_summary,
        c        = title_and_citation,
    )

    implementation = generate_content(IMPLEMENTATION_GENERATION_PROMPT)

    ##########################################################

    ##-- WEB APPLICATION DEVELOPMENT --##

    WEB_APP_DEVELOPMENT_GENERATION_PROMPT = prompt_parameters + """
    Write about web application development in approximately 200 words in the research report.

    1. Do not mention the web application framework definition.
    2. Keep a single paragraph.
    3. Do not mention any definitions.
    4. Do not use parentheses to mention values.
    5. Do not use function or library names like keras.sequential() etc.
    6. Do not mention any code or subheadings.
    7. Strictly approximately 200 words.
    8. Keep content in past tense.
    9. Name the exact framework, UI components, input fields, and
       configurations — do not stay generic.

    Note: Implementation only — no theoretical framework.

    Use web app summary from:
    {a}
    """.format(a=web_app_summary)

    web_app_development = generate_content(WEB_APP_DEVELOPMENT_GENERATION_PROMPT)

    ##########################################################

    # Save web app development to InputFiles (used downstream)
    os.makedirs("InputFiles", exist_ok=True)
    with open("InputFiles/wad.txt", "w", encoding='utf-8') as file:
        file.write("Web App Development:\n")
        file.write(web_app_development + "\n\n")

    # Dictionary to hold section titles and corresponding content
    sections = {
        "IMPLEMENTATION": implementation,
    }

    # Write to file with UTF-8 encoding
    os.makedirs("OutputFiles", exist_ok=True)
    with open("OutputFiles/implementation.txt", "w", encoding='utf-8') as file:
        file.write("IMPLEMENTATION\n")
        file.write("------------------------\n")
        for i, (title, content) in enumerate(sections.items(), 1):
            file.write(f"{i}. {title}\n")
            file.write("-" * 40 + "\n")
            file.write(content + "\n\n")
