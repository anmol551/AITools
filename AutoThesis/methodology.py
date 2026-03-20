from ai import generate_content
from utils import load_files, paper_cite, load_config
import os

def generate_methodology():
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

    METHODOLOGY_GENERATION_PROMPT = prompt_parameters + """
    Generate a methodology section of my research report.

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
       - Components that happen BEFORE model building go between
         Data Preprocessing and Model Building.
       - Components that happen AFTER model building go between
         Model Performance Evaluation Metrics and Ethics.
    5. Do NOT skip any pipeline component — if it is in the pipeline,
       it must have its own subsection.
    6. Number all subsections sequentially.

    ══════════════════════════════════════════════════════════
    EQUATION PLACEHOLDERS RULE (apply to ALL subsections):
    Wherever a mathematical formula or expression would appear, do NOT
    write the actual formula. Insert a placeholder instead:
        [EQ_N: brief description of what the equation represents]
    where N increments globally across the entire methodology (never reset).
    Apply to: model formulas, preprocessing transformations, feature
    engineering expressions, metric formulas, loss functions, activations,
    and any other mathematical expression.
    ══════════════════════════════════════════════════════════

    ── FIXED SUBSECTION 1 : Research Design (~150 words) ──────────────────
    Change heading to match project topic.
        1. Describe the full research design pipeline without results.
           Start from literature survey or data collection, cover ALL stages
           in the pipeline, and end at web app testing if present.
        2. Must be technical — mention all methods, techniques, model names,
           web app name, and LLM if present.
        3. Do not mention the best-performing model name.
        4. Avoid function names.
        5. Write in 2 paragraphs. No citations.
        6. Strictly approximately 150 words.

    ── FIXED SUBSECTION 2 : Dataset Description (~150 words) ──────────────
    Change heading to match project topic.
        1. Describe the dataset used — source, author if present, shape.
        2. Explain why it was chosen and its characteristics.
        3. File formats only if present (e.g., .wav, .jpg).
        4. Do not use exact feature names — use a summary table instead.
        5. Mention the data source link. Example: Source: Link
        6. No citations.
        7. Structure: a) shape/size/physical characteristics,
                       b) why chosen,
                       c) data ethics — 2-3 paragraphs,
           then a table or bullets for key data representations.
        8. Strictly approximately 150 words.

    ── FIXED SUBSECTION 3 : Data Preprocessing ────────────────────────────
    Change heading to match project topic.
        1. Begin with one introductory sentence.
        2. For EACH preprocessing technique, create a dedicated subheading.
        3. Under each subheading (~130 words, 2 paragraphs):
            - Definition, reason for selection, how it improves quality,
              equation placeholder where applicable, and one in-text citation.
        4. In-text citations embedded in sentences.
           Example: "According to Sharif et al. (2020), …"
        5. No summary at the end. Cover every technique.
        6. Match citations from the citation file. Do not use paper titles.

    ── DYNAMIC SUBSECTIONS (pre-model) ────────────────────────────────────
    For each pipeline stage that occurs BEFORE model training
    (e.g., Feature Selection, Feature Engineering, Class Balancing,
    Hyperparameter Tuning, or any other component found in the pipeline):

    Generate a dedicated subsection (~150 words, 2 paragraphs):
        - Paragraph 1: Definition and specific reason for use in this research.
        - Paragraph 2: Key steps, parameters, tools, equation placeholders,
          and one in-text citation from the citation file.
        - Do not use paper titles in citations.

    ── FIXED SUBSECTION : Model Building ──────────────────────────────────
    Change heading to match project topic.
        1. Begin with one introductory sentence.
        2. For EVERY model used, create a dedicated subheading (~200 words,
           2 paragraphs):
            - Paragraph 1 (~100 words): Clear definition and specific
              justification for why this model was chosen for THIS research.
              Do not give generic reasons.
            - Paragraph 2 (~100 words): Working principles, parameters,
              equation placeholders (per EQUATION PLACEHOLDERS RULE),
              and at least one in-text citation.
        3. For neural network architectures (CNN, TabNet, etc.), ALSO create
           a dedicated subheading for EACH layer or block present, including:
           Conv1D, BatchNormalisation, Dense, Dropout, Flatten,
           Attention Mechanism, and any other named layer.
           Each layer subheading MUST have:
            - Approximately 120 words minimum in EXACTLY 2 paragraphs.
            - Paragraph 1 (~60 words): Definition and specific role in
              THIS model's architecture.
            - Paragraph 2 (~60 words): Internal workings, parameter values,
              and one equation placeholder.
            - Do NOT write one-line descriptions — full 2-paragraph
              treatment is required for every layer regardless of simplicity.
        4. No implementation details, function names, or results.
        5. No summaries.

    ── FIXED SUBSECTION : Model Performance Evaluation Metrics (~200 words)
        1. One-line introduction.
        2. Define each evaluation metric used (40-50 words each).
        3. Include one equation placeholder per metric formula.
        4. Discuss metrics in context of the research topic.
        5. No citations. Strictly approximately 200 words.

    ── DYNAMIC SUBSECTIONS (post-model) ───────────────────────────────────
    For each pipeline stage that occurs AFTER model training
    (e.g., LLM Integration, Web Application, XAI Framework, or any other
    component found in the pipeline):

    Generate a dedicated subsection with the following requirements:

    LLM Integration (~180 words, 2 paragraphs):
        - What LLM was integrated and why it was chosen.
        - Its role in the pipeline, API/interface used, prompt design.
        - Benefits for explainability and decision support.
        - Citations where relevant from the citation file.

    Web Application Framework (~180 words, 2 paragraphs):
        - Definition of the framework and reason for selecting it.
        - Key benefits: deployment ease, interactivity, user-friendliness.
        - What the application does — inputs, processing, outputs.
        - Citations from the citation file.

    XAI Framework (~150 words, 2 paragraphs):
        - Definition and reason for selecting the XAI method.
        - Citations from the citation file.
        - Equation placeholders where formulas appear.

    Any other post-model component: ~150 words, 2 paragraphs,
    definition + justification + citations if available.

    ── FIXED LAST SUBSECTION : Professional, Legal, and Ethical
       Considerations (~200 words) ─────────────────────────────────────
        1. Professional, legal, and ethical considerations for this research.
        2. Data and model-related factors.
        3. One or two paragraphs only. No citations.
        4. Strictly approximately 200 words.

    ══════════════════════════════════════════════════════════
    IMPORTANT FINAL CHECKS before finishing:
    - Confirm EVERY pipeline stage has a corresponding subsection.
    - Confirm LLM Integration is present if LLM appears in the pipeline.
    - Confirm Web Application is present if a web app appears in the pipeline.
    - Confirm no section is missing, merged, or out of order.
    - Use commas only when necessary.
    ══════════════════════════════════════════════════════════

    Use code summary, web app summary, and citations from:
    {a} {b} {c} {d}
    """.format(
        pipeline = pipeline_content,
        a        = data_details,
        b        = code_summary,
        c        = web_app_summary,
        d        = title_and_citation,
    )

    # Generate with Unicode safety
    try:
        methodology = generate_content(METHODOLOGY_GENERATION_PROMPT)
    except UnicodeEncodeError as e:
        print(f"Unicode error during content generation: {e}")
        clean_prompt = METHODOLOGY_GENERATION_PROMPT.encode('ascii', 'ignore').decode('ascii')
        methodology = generate_content(clean_prompt)

    # Dictionary to hold section titles and corresponding content
    sections = {
        "METHODOLOGY": methodology,
    }

    # Ensure output directory exists
    os.makedirs("OutputFiles", exist_ok=True)

    # Write to file with comprehensive Unicode handling
    try:
        with open("OutputFiles/methodology.txt", "w", encoding="utf-8", errors='replace') as file:
            file.write("METHODOLOGY\n")
            file.write("------------------------\n")
            for i, (title, content) in enumerate(sections.items(), 1):
                file.write(f"{i}. {title}\n")
                file.write("-" * 40 + "\n")
                if isinstance(content, str):
                    file.write(content + "\n\n")
                else:
                    file.write(str(content) + "\n\n")
        print("Methodology file created successfully with UTF-8 encoding.")

    except UnicodeEncodeError as e:
        print(f"Unicode encoding error: {e}")
        with open("OutputFiles/methodology.txt", "w", encoding="utf-8", errors='replace') as file:
            file.write("METHODOLOGY\n")
            file.write("------------------------\n")
            for i, (title, content) in enumerate(sections.items(), 1):
                file.write(f"{i}. {title}\n")
                file.write("-" * 40 + "\n")
                clean_content = str(content).encode('utf-8', 'replace').decode('utf-8')
                file.write(clean_content + "\n\n")
        print("Methodology file created with character replacement.")

    except Exception as e:
        print(f"Unexpected error: {e}")
        with open("OutputFiles/methodology.txt", "w", encoding="ascii", errors='replace') as file:
            file.write("METHODOLOGY\n")
            file.write("------------------------\n")
            for i, (title, content) in enumerate(sections.items(), 1):
                file.write(f"{i}. {title}\n")
                file.write("-" * 40 + "\n")
                ascii_content = str(content).encode('ascii', 'replace').decode('ascii')
                file.write(ascii_content + "\n\n")
        print("Methodology file created with ASCII encoding as fallback.")
