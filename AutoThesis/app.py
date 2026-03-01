import time, yaml, os
import streamlit as st
import streamlit.components.v1 as components
from utils import save_text_file
from introduction import generate_introduction
from methodology import generate_methodology
from implementation import generate_implementation
from abstract import generate_abstract
from keywords import generate_keywords
from get_citation import get_ref_citation
from result import generate_result_conclusion
import chardet
import base64

# state the output path
directory = "OutputFiles"

def get_base64_of_bin_file(bin_file):
    """Convert binary file to base64 string"""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.warning(f"Background image '{bin_file}' not found. Using default background.")
        return None

def set_png_as_page_bg(png_file):
    """Set background image for the Streamlit app"""
    bin_str = get_base64_of_bin_file(png_file)
    if bin_str:
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/webp;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* Make content areas semi-transparent for better readability */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {{
            background-color: rgba(255, 255, 255, 0.9) !important;
            color: #000000 !important;
        }}
        
        /* Style for expander content */
        .streamlit-expanderContent {{
            background-color: rgba(255, 255, 255, 0.95) !important;
            border-radius: 10px;
            padding: 10px;
        }}
        
        /* Style for main content container */
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 2rem;
            backdrop-filter: blur(10px);
        }}
        
        /* Button styling */
        .stButton > button {{
            background-color: rgba(94, 183, 194, 0.7) !important;
            color: white !important;
            border: none !important;
            border-radius: 5px !important;
            backdrop-filter: blur(5px);
        }}
        
        .stButton > button:hover {{
            background-color: rgba(94, 183, 194, 1) !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        
        /* Header styling */
        h1, h2, h3 {{
            color: #ffffff !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        }}
        
        /* Success/warning message styling */
        .stSuccess, .stWarning, .stError {{
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 5px;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)

# Set background image
set_png_as_page_bg('bg.webp')

def read_file_auto_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        encoding = chardet.detect(raw_data)['encoding']
        return raw_data.decode(encoding or 'utf-8', errors='replace')

# Initialize session state for tracking generation progress
if 'generation_step' not in st.session_state:
    st.session_state.generation_step = 0

if 'sections_generated' not in st.session_state:
    st.session_state.sections_generated = {
        'keywords': False,
        'citations': False,
        'abstract': False,
        'introduction': False,
        'methodology': False,
        'implementation': False,
        'results': False
    }

# Text area for user input
st.title("Dissertation Report Auto Generation")

title = st.text_area("Title of the research:")

format = st.selectbox("Select Format", ["1", "2", "3", "4"])

question = st.text_area("Research Question:")

objective = st.text_area("Objectives of the Research:")

data_details = st.text_area("Data Details (information about dataset and source link):")
save_text_file(data_details, "InputFiles/dd.txt")

##-- LITERATURE REVIEW SUMMARY --## 
LITERATURE_REVIEW_PROMPT = "Analyze the given Literature Review and generate a structured summary while preserving all essential technical content and citations. Before summarization, conduct a background search to understand the topic thoroughly. The summary should be 15-20% of the original length while maintaining clarity, coherence, and completeness.Summary Must Include:Topic Overview: Provide a concise background and relevance of the topic based on the Literature Review.Importance of the Chosen Field (with Citations): Explain why this field of research is significant, its real-world applications, and its impact on industries, society, or technology.Key Technical Content: Extract critical theories, models, methodologies, or frameworks discussed.Findings & Insights: Summarize major findings, patterns, or trends identified in the literature.Limitations Identified: Highlight gaps, weaknesses, or missing elements in existing research.Unresolved Issues: Mention ongoing debates, contradictions, or unanswered questions that remain open for further study.Preserve Citations: Retain all references and in-text citations exactly as they appear in the original document.Parameters:Background Search: First, gather relevant information to ensure a well-informed summary.Word Limit: Compress to 15-20% of the original content (i.e., 525-700 words for 3,500 words).Technical Accuracy: Maintain integrity of complex concepts, models, and frameworks.Mention all the important values like performance percentage if present.Clarity & Coherence: Ensure readability and logical flow.Citation Integrity: Do not remove or alter any references; they must be retained as in the original document.Deliver the summary in a well-structured format while ensuring all major points, technical details, and research gaps are clearly presented."

components.html(
    f"""
    <button onclick="copyToClipboard()">Copy your literature review prompt(req: Literature Document)</button>
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText("{LITERATURE_REVIEW_PROMPT}");
        alert("Copied to clipboard!");
    }}
    </script>
    """,
    height=50,
)

literature_review_summary = st.text_area("Paste the Literature Review Summary:")
save_text_file(literature_review_summary, "InputFiles/lrs.txt")

##-- RESEARCH GAPS--##
research_gaps = st.text_area("Paste the Research Gaps (Obtained from LR):")
save_text_file(research_gaps, "InputFiles/rg.txt")

##-- BASE PAPER SUMMARY --##
BASE_PAPER_PROMPT = "Instructions: 1. What is the complete flow or pipeline of research 2. Details of the data getting used. 3. What is the accuracy of all the methods used 4. Which algorithm achieved best accuracy and what is it 5. What is the novel or unique element in the research 6. What are the future recommendations of the research paper All in 500 words."

components.html(
    f"""
    <button onclick="copyToClipboard()">Copy your base paper prompt</button>
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText("{BASE_PAPER_PROMPT}");
        alert("Copied to clipboard!");
    }}
    </script>
    """,
    height=50,
)

base_paper_summary = st.text_area("Paste the Base Paper Summary:")
save_text_file(base_paper_summary, "InputFiles/bps.txt")

base_paper_citation = st.text_area("Base Paper Citation")

##-- CONFIG UPDATE --##
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

config["TITLE"] = title
config["FORMAT"] = format
config['RESEARCH_QUESTION'] = question
config['RESEARCH_OBJECTIVES'] = objective
config["BASE_PAPER_CITATION"] = base_paper_citation

with open("config.yaml", "w") as file:
    yaml.dump(config, file, default_flow_style=False)

##-- CODE SUMMARY --##
CODE_SUMMARY_PROMPT = "Summarize the following code, which focuses on [extract key focus from the code, e.g., machine learning, web scraping, financial analysis, etc.], into 2-3 concise paragraphs while preserving all essential technical details.Summary must include:Overview: Purpose and functionality of the code.Key Components: Main functions, classes, or modules and their roles.Execution Flow: How the code runs from input to output.Core Logic: Important algorithms or computations.Web App Elements (if any): API endpoints, routes, or database interactions.Parameters:Format: Paragraph-based (2-3 paragraphs).Conciseness: 15-20% of original length.Technical Accuracy: Preserve key function names and logic.Readability: Clear, structured, and informative.Deliver the summary in a well-structured, readable format with a clear focus on the main purpose of the code."

components.html(
    f"""
    <button onclick="copyToClipboard()">Copy your code summary prompt(req: code)</button>
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText("{CODE_SUMMARY_PROMPT}");
        alert("Copied to clipboard!");
    }}
    </script>
    """,
    height=50,
)

code_summary = st.text_area("Paste the Code Summary:")
save_text_file(code_summary, "InputFiles/cs.txt")

##-- CODE SUMMARY WITH VALUES --##
CODE_SUMMARY_WITH_VALUES_PROMPT = "Analyze the given code (~1000 lines) stored in a .txt file. Extract a list of libraries used and segment the code into the following categories, ensuring all details are accurately captured.Required Segments:Statistical Analysis:Identify all functions used for statistical analysis.Provide their purpose and the outcome they generate.Exploratory Data Analysis (EDA):Extract details of each plot, including:Plot Type (e.g., histogram, scatter plot, box plot, etc.).Plot Title and what it represents.X and Y Variables being analyzed.Insights from each visualization, explaining trends, patterns, outliers, and distributions.If there are correlation matrices or summary statistics, include key takeaways.Data Preprocessing:List functions used for preprocessing (e.g., scaling, encoding, missing value treatment).Specify parameters and their values for each function.Do not mention Train-Test-Split hereFeature EngineeringMention all the selected column names if feature selection is done.Train Split InformationModel Details:Identify functions used for model building and training .Mention the name of the tuning method if done.List the models used and their associated parameters.If the code has both a base model (default parameters) and a tuned model (optimized parameters), display them separately.Model Results & Performance Evaluation:First, list the performance metrics used for evaluation.Then, provide a table showing:Algorithm namePerformance values across each metric (e.g., accuracy, precision, recall, RMSE, etc.).If multiple models are compared, highlight which model performed best.Parameters:Format: Structured and well-organized for readability.Conciseness: Extract only relevant details while ensuring completeness.Technical Accuracy: Preserve function names, parameters, and values.Insightful Output: Provide meaningful explanations, especially in the EDA section.Ensure that all extracted details are correctly categorized and that model performance is clearly presented with insightful comparisons."

components.html(
    f"""
    <button onclick="copyToClipboard()">Copy your code summary with values</button>
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText("{CODE_SUMMARY_WITH_VALUES_PROMPT}");
        alert("Copied to clipboard!");
    }}
    </script>
    """,
    height=50,
)

code_summary_with_values = st.text_area("Paste the Code Summary With Values:")
save_text_file(code_summary_with_values, "InputFiles/csvs.txt")

##-- WEBAPP SECTION --##
WEBAPP_PROMPT = "Analyze the given web application code and generate a concise summary (150-200 words) covering all key functionalities and technical components. Summary Must Include:Overview: Briefly describe the purpose and functionality of the web app.Python Framework Used: Clearly state the web framework (e.g., Flask, Django, FastAPI, streamlit, etc) used in the application.Libraries & Dependencies: List all major libraries and dependencies.User Input Handling: Explain how user input is collected (e.g., input text box, file upload, dropdown, etc.).Main Functions & Features: Summarize key functions, including API endpoints, data processing, and UI components.Prediction Function: Provide a focused explanation of the core prediction logic, including the model used and how it processes input data.Parameters:Conciseness: Keep the summary within 100-150 words while ensuring completeness.Technical Accuracy: Retain function names and their core purpose.Readability: Ensure the summary is clear and structured for easy understanding.Deliver the summary in a well-structured format while preserving all critical details of the web application."

components.html(
    f"""
    <button onclick="copyToClipboard()">Copy your WebApp prompt(req: webapp)</button>
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText("{WEBAPP_PROMPT}");
        alert("Copied to clipboard!");
    }}
    </script>
    """,
    height=50,
)

webapp_summary = st.text_area("Paste the WebApp Summary:")
save_text_file(webapp_summary, "InputFiles/ws.txt")

##-- WEB APP TESTING RESULTS --##
WEB_APP_TEST_PROMPT = "Provide me the insight of the web test result in 80 words with mentioning each of the values and don't use parenthesis to mention values'()'"

components.html(
    f"""
    <button onclick="copyToClipboard()">Copy your WebApp testing images prompt(req: webapp)</button>
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText("{WEB_APP_TEST_PROMPT}");
        alert("Copied to clipboard!");
    }}
    </script>
    """,
    height=50,
)

webapp_test = st.text_area("Paste the WebApp Test Case Result Here:")
save_text_file(webapp_test, "InputFiles/wat.txt")

##-- NOVELTY --##
NOVELTY_PROMPT = "Analyze the provided code and identify its novelty in depth in 300 words para. Explain the unique aspects, innovations, or optimizations present in the code, including algorithmic improvements, architectural design, efficiency enhancements, and any novel methodologies or techniques applied. Discuss how these aspects contribute to the overall performance, maintainability, and scalability of the system."

components.html(
    f"""
    <button onclick="copyToClipboard()">Copy Novelty Prompt(req: code+webapp)</button>
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText("{NOVELTY_PROMPT}");
        alert("Copied to clipboard!");
    }}
    </script>
    """,
    height=50,
)

novelty = st.text_area("Paste the Novelty:")
save_text_file(novelty, "InputFiles/novelty.txt")

##-- RESULTS SECTION --##
RESULTS_PLOT_PROMPT = "Requirements:1. create a table 2. mention all the plots individually do not write collectively3. mention all plots for all the modelsTable 1- all result plot information table:Title: Title of the plots from codeType of plot: Type of plot [Bar chart, Pie chart, etc]Insights: Insights of the chart from the code which should include the values presentCharts can be considered in Table 1: Explainable AI, ROC, AUC, Training and loss neural network, comparison curve, confusion matrixNote:1. Do not include any plot from data exploration, preprocessing, feature engineering, or data transformation steps.2. For the comparison plots mention insight as 'will be taken from table'"

components.html(
    f"""
    <button onclick="copyToClipboard()">Copy your results plot prompt(req: code)</button>
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText("{RESULTS_PLOT_PROMPT}");
        alert("Copied to clipboard!");
    }}
    </script>
    """,
    height=50,
)

result_plot_summary = st.text_area("Paste the Result Plot Summary:")

RESULTS_TABLE_PROMPT = "Generate a table for: Performance Table: Include all models, all metrics (as extracted from the code), and highlight the best-performing model."

components.html(
    f"""
    <button onclick="copyToClipboard()">Copy your results table prompt(req: code)</button>
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText("{RESULTS_TABLE_PROMPT}");
        alert("Copied to clipboard!");
    }}
    </script>
    """,
    height=50,
)

result_table_summary = st.text_area("Paste the Result Table Summary:")
save_text_file(result_plot_summary+"\n\n"+result_table_summary, "InputFiles/rs.txt")

##-- FAILED ATTEMPTS --##
FAILED_ATTEMPTS_PROMPT = "Discuss any failed attempts. At the beginning, write a short introduction of 25 to 35 words for this section. Add a performance result table if available. Mension why a particular method is suitable than other, as per your analysis. Please modify the subheadings to better suit the research project topic. Use clear, meaningful titles. Word count can go up to 100 words."

components.html(
    f"""
    <button onclick="copyToClipboard()">Copy your failed attempt prompt(req: code)</button>
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText("{FAILED_ATTEMPTS_PROMPT}");
        alert("Copied to clipboard!");
    }}
    </script>
    """,
    height=50,
)

failed_attempt_summary = st.text_area("Paste the Failed Attempt Summary:")
save_text_file(result_plot_summary+"\n\n"+failed_attempt_summary, "InputFiles/fa.txt")

# Generation Progress Section
st.markdown("---")
st.header("📝 Document Generation Progress")

# Step-by-step generation without preview functionality
col1, col2 = st.columns([3, 1])

with col1:
    st.write("**Generation Steps:**")
    steps = [
        ("Keywords & Citations", ["keywords", "citations"]),
        ("Abstract", ["abstract"]),
        ("Introduction", ["introduction"]),
        ("Methodology", ["methodology"]),
        ("Implementation", ["implementation"]),
        ("Results & Conclusion", ["results"])
    ]
    
    for i, (step_name, step_keys) in enumerate(steps):
        status = "✅" if all(st.session_state.sections_generated[key] for key in step_keys) else "⏳"
        st.write(f"{i+1}. {status} {step_name}")

# Generate individual sections
if st.button("🚀 Start Generation Process"):
    st.session_state.generation_step = 1
    
if st.session_state.generation_step >= 1:
    st.subheader("Step 1: Keywords & Citations")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Generate Keywords & Citations"):
            with st.spinner("Generating keywords..."):
                generate_keywords()
                st.session_state.sections_generated['keywords'] = True
                st.success("Keywords generated!")
                time.sleep(1)
            
            with st.spinner("Generating citations..."):
                get_ref_citation()
                st.session_state.sections_generated['citations'] = True
                st.success("Citations generated!")
    
    if st.session_state.sections_generated['keywords'] and st.session_state.sections_generated['citations']:
        with col2:
            if st.button("Continue to Abstract"):
                st.session_state.generation_step = 2
                st.rerun()

if st.session_state.generation_step >= 2:
    st.subheader("Step 2: Abstract")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Generate Abstract"):
            with st.spinner("Generating abstract..."):
                generate_abstract()
                st.session_state.sections_generated['abstract'] = True
                st.success("Abstract generated!")
    
    if st.session_state.sections_generated['abstract']:
        with col2:
            col_continue, col_retry = st.columns(2)
            with col_continue:
                if st.button("Continue", key="continue_abstract"):
                    st.session_state.generation_step = 3
                    st.rerun()
            with col_retry:
                if st.button("🔄 Retry", key="retry_abstract"):
                    st.session_state.sections_generated['abstract'] = False
                    st.rerun()

if st.session_state.generation_step >= 3:
    st.subheader("Step 3: Introduction")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Generate Introduction"):
            with st.spinner("Generating introduction..."):
                generate_introduction()
                st.session_state.sections_generated['introduction'] = True
                st.success("Introduction generated!")
    
    if st.session_state.sections_generated['introduction']:
        with col2:
            col_continue, col_retry = st.columns(2)
            with col_continue:
                if st.button("Continue", key="continue_intro"):
                    st.session_state.generation_step = 4
                    st.rerun()
            with col_retry:
                if st.button("Retry", key="retry_intro"):
                    st.session_state.sections_generated['introduction'] = False
                    st.rerun()

if st.session_state.generation_step >= 4:
    st.subheader("Step 4: Methodology")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Generate Methodology"):
            with st.spinner("Generating methodology..."):
                generate_methodology()
                st.session_state.sections_generated['methodology'] = True
                st.success("Methodology generated!")
    
    if st.session_state.sections_generated['methodology']:
        with col2:
            col_continue, col_retry = st.columns(2)
            with col_continue:
                if st.button("Continue", key="continue_method"):
                    st.session_state.generation_step = 5
                    st.rerun()
            with col_retry:
                if st.button("Retry", key="retry_method"):
                    st.session_state.sections_generated['methodology'] = False
                    st.rerun()

if st.session_state.generation_step >= 5:
    st.subheader("Step 5: Implementation")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Generate Implementation"):
            with st.spinner("Generating implementation..."):
                generate_implementation()
                st.session_state.sections_generated['implementation'] = True
                st.success("Implementation generated!")
    
    if st.session_state.sections_generated['implementation']:
        with col2:
            col_continue, col_retry = st.columns(2)
            with col_continue:
                if st.button("Continue", key="continue_impl"):
                    st.session_state.generation_step = 6
                    st.rerun()
            with col_retry:
                if st.button("Retry", key="retry_impl"):
                    st.session_state.sections_generated['implementation'] = False
                    st.rerun()

if st.session_state.generation_step >= 6:
    st.subheader("Step 6: Results & Conclusion")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Generate Results & Conclusion"):
            with st.spinner("Generating results and conclusion..."):
                generate_result_conclusion()
                st.session_state.sections_generated['results'] = True
                st.success("Results & Conclusion generated!")
    
    if st.session_state.sections_generated['results']:
        with col2:
            col_continue, col_retry = st.columns(2)
            with col_continue:
                if st.button("Finalize Document", key="finalize_doc"):
                    st.session_state.generation_step = 7
                    st.rerun()
            with col_retry:
                if st.button("Retry", key="retry_results"):
                    st.session_state.sections_generated['results'] = False
                    st.rerun()

# Final document download
if st.session_state.generation_step >= 7:
    st.markdown("---")
    st.subheader("🎉 Document Generation Complete!")
    
    # List of file names in order
    file_names = [
        "abstract.txt",
        "introduction.txt", 
        "methodology.txt",
        "implementation.txt",
        "results.txt",
        "conclusion.txt"
    ]
    
    # Initialize an empty string to store the combined content
    combined_content = ""

    # Read and combine the files
    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        try:
            content = read_file_auto_encoding(file_path)
            combined_content += content + "\n\n"
        except FileNotFoundError:
            st.warning(f"Warning: {file_name} not found!")

    # Convert content to bytes
    safe_title = "".join(c for c in title if c.isalnum() or c in [' ', '_', '-']).strip().replace(" ", "_")
    file_name = f"final_document({safe_title}).txt"
    
    file_bytes = combined_content.encode("utf-8")

    # Create download button
    st.download_button(
        label="📥 Download Final Document",
        data=file_bytes,
        file_name=file_name,
        mime="text/plain"
    )
    
    # Option to start over
    if st.button("Start New Document"):
        st.session_state.generation_step = 0
        st.session_state.sections_generated = {
            'keywords': False,
            'citations': False,
            'abstract': False,
            'introduction': False,
            'methodology': False,
            'implementation': False,
            'results': False
        }
        st.rerun()