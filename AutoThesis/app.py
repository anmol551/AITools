import time, yaml, os, json, io, re, sys
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

# ── Optional extraction libraries (install via: pip install python-docx pypdf) ──
try:
    import docx as _docx_mod
    _DOCX_OK = True
except ImportError:
    _DOCX_OK = False

try:
    import pypdf as _pypdf_mod
    _PYPDF_OK = True
except ImportError:
    _PYPDF_OK = False

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DRAFTMIND AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── NEXUS CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Outfit:wght@300;400;500;600&display=swap');

:root {
  --ink:        #08090d;
  --surface:    #0f1117;
  --panel:      #13161f;
  --raised:     #191d28;
  --rim:        #252a38;
  --gold:       #c9a84c;
  --gold-soft:  rgba(201,168,76,0.10);
  --gold-glow:  rgba(201,168,76,0.25);
  --platinum:   #e8eaf2;
  --mist:       #6b7280;
  --emerald:    #10b981;
  --ruby:       #ef4444;
  --sapphire:   #3b82f6;
  --r:          10px;
}

/* ── Resets ── */
.stApp { background: var(--ink) !important; font-family: 'Outfit', sans-serif !important; color: var(--platinum) !important; }
.block-container { padding: 0 2rem 4rem !important; max-width: 100% !important; margin: 0 !important; }
.main > div { padding: 0 !important; }
[data-testid="stAppViewBlockContainer"] { padding-top: 0 !important; }
#MainMenu, footer, header { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Ambient Grid ── */
.stApp::before {
  content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background-image:
    linear-gradient(rgba(201,168,76,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(201,168,76,0.03) 1px, transparent 1px);
  background-size: 48px 48px;
}

/* ── Topbar ── */
.topbar {
  position: sticky; top: 0; z-index: 100; height: 64px;
  background: rgba(8,9,13,0.92); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--rim);
  padding: 0 36px; display: flex; align-items: center; gap: 18px;
}
.topbar-wordmark {
  font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700;
  letter-spacing: 4px; text-transform: uppercase; color: var(--gold) !important; margin: 0;
}
.topbar-divider { width: 1px; height: 24px; background: var(--rim); }
.topbar-subtitle { font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--mist); margin: 0; }
.topbar-badge {
  margin-left: auto; display: inline-flex; align-items: center; gap: 7px;
  font-size: 10px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;
  color: var(--emerald); background: rgba(16,185,129,0.08);
  border: 1px solid rgba(16,185,129,0.25); border-radius: 999px; padding: 4px 12px;
}
.topbar-badge::before {
  content: ''; width: 6px; height: 6px; border-radius: 50%;
  background: var(--emerald); box-shadow: 0 0 6px var(--emerald);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: var(--panel) !important; border-right: 1px solid var(--rim) !important; width: 300px !important; }
[data-testid="stSidebar"] > div { padding: 0 !important; }

/* ── Sidebar brand block ── */
.sb-brand {
  padding: 28px 22px 22px;
  border-bottom: 1px solid var(--rim);
  background: linear-gradient(180deg, rgba(201,168,76,0.07) 0%, transparent 100%);
}
.sb-title {
  font-family: 'Playfair Display', serif; font-size: 15px; font-weight: 700;
  letter-spacing: 3px; text-transform: uppercase; color: var(--gold); margin: 0 0 4px;
}
.sb-sub { font-size: 11px; color: var(--mist); letter-spacing: 0.5px; margin: 0; }

/* ── Sidebar section label ── */
.sb-label {
  font-size: 9px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase;
  color: var(--mist); margin: 20px 0 10px; padding: 0 22px;
  display: flex; align-items: center; gap: 8px;
}
.sb-label::after { content: ''; flex: 1; height: 1px; background: var(--rim); }

/* ── Stat tiles ── */
.stat-tile {
  background: var(--raised); border: 1px solid var(--rim); border-radius: var(--r);
  padding: 12px 16px; margin: 0 14px 10px; position: relative; overflow: hidden;
}
.stat-tile::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, var(--gold), transparent);
}
.stat-value { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 700; color: var(--gold); margin: 0; }
.stat-label { font-size: 10px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: var(--mist); margin: 2px 0 0; }

/* ── Step progress badges in sidebar ── */
.step-row {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 22px; font-size: 12px; color: var(--mist);
}
.step-dot {
  width: 20px; height: 20px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 9px; font-weight: 700; border: 1px solid var(--rim);
  background: var(--raised); color: var(--mist);
}
.step-dot.done { background: var(--gold); color: var(--ink); border-color: var(--gold); }
.step-dot.active { border-color: var(--gold); color: var(--gold); box-shadow: 0 0 8px var(--gold-glow); }

/* ── Main content wrapper ── */
.content-wrap { max-width: 860px; margin: 0 auto; padding: 8px 28px 160px; }

/* ── Section card ── */
.section-card {
  background: var(--surface); border: 1px solid var(--rim); border-radius: 14px;
  padding: 28px 28px 24px; margin-bottom: 24px; position: relative; overflow: hidden;
}
.section-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, var(--gold), transparent 60%);
}
.section-heading {
  font-family: 'Playfair Display', serif; font-size: 15px; font-weight: 600;
  color: var(--gold); letter-spacing: 0.5px; margin: 0 0 16px;
  display: flex; align-items: center; gap: 10px;
}

/* ── Upload zone ── */
.upload-zone {
  background: var(--raised); border: 1px dashed rgba(201,168,76,0.35); border-radius: 12px;
  padding: 32px 24px; text-align: center; margin-bottom: 8px;
  transition: all 0.2s ease;
}
.upload-zone:hover { border-color: rgba(201,168,76,0.65); background: var(--gold-soft); }
.upload-icon { font-size: 28px; margin-bottom: 10px; }
.upload-title { font-family: 'Playfair Display', serif; font-size: 17px; color: var(--platinum); margin: 0 0 6px; }
.upload-sub { font-size: 12px; color: var(--mist); }

/* ── JSON loaded banner ── */
.json-loaded-banner {
  background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(16,185,129,0.04));
  border: 1px solid rgba(16,185,129,0.3); border-radius: var(--r);
  padding: 14px 18px; display: flex; align-items: center; gap: 12px; margin-bottom: 8px;
}
.jlb-icon { font-size: 20px; }
.jlb-text { font-size: 13px; color: var(--emerald); font-weight: 500; }
.jlb-sub { font-size: 11px; color: var(--mist); margin-top: 2px; }

/* ── Inputs & textareas ── */
.stTextArea textarea, .stTextInput input {
  background: var(--raised) !important; border: 1px solid var(--rim) !important;
  border-radius: var(--r) !important; color: var(--platinum) !important;
  font-family: 'Outfit', sans-serif !important; font-size: 13px !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
  border-color: rgba(201,168,76,0.5) !important;
  box-shadow: 0 0 0 3px var(--gold-soft), 0 0 20px var(--gold-glow) !important;
  outline: none !important;
}
.stTextArea label, .stTextInput label, .stSelectbox label {
  font-size: 10px !important; font-weight: 600 !important; letter-spacing: 1.8px !important;
  text-transform: uppercase !important; color: var(--mist) !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
  background: var(--raised) !important; border: 1px solid var(--rim) !important;
  border-radius: var(--r) !important; color: var(--platinum) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
  background: var(--raised) !important; border: 1px dashed rgba(201,168,76,0.3) !important;
  border-radius: 12px !important;
}
[data-testid="stFileUploader"] label { color: var(--mist) !important; }
[data-testid="stFileUploaderDropzoneInstructions"] { color: var(--mist) !important; }

/* ── Buttons ── */
.stButton > button {
  background: var(--raised) !important; color: var(--platinum) !important;
  border: 1px solid var(--rim) !important; border-radius: var(--r) !important;
  font-family: 'Outfit', sans-serif !important; font-size: 13px !important;
  font-weight: 500 !important; transition: all 0.2s ease !important;
  width: 100% !important; padding: 10px 18px !important;
}
.stButton > button:hover {
  background: var(--gold-soft) !important; border-color: rgba(201,168,76,0.4) !important;
  color: var(--gold) !important; transform: translateX(3px) !important;
}

/* ── Primary button ── */
.primary-btn > button {
  background: linear-gradient(135deg, rgba(201,168,76,0.18), rgba(201,168,76,0.06)) !important;
  border-color: rgba(201,168,76,0.45) !important; color: var(--gold) !important;
  font-weight: 600 !important; font-size: 14px !important; padding: 12px 20px !important;
  transform: none !important;
}
.primary-btn > button:hover {
  box-shadow: 0 0 20px var(--gold-glow) !important;
  transform: translateY(-1px) !important;
}

/* ── Danger button ── */
.danger-btn > button {
  background: rgba(239,68,68,0.07) !important; border-color: rgba(239,68,68,0.3) !important;
  color: #f87171 !important;
}
.danger-btn > button:hover { background: rgba(239,68,68,0.14) !important; }

/* ── Step generation card ── */
.gen-card {
  background: var(--surface); border: 1px solid var(--rim); border-radius: 12px;
  padding: 22px 24px; margin-bottom: 20px;
}
.gen-card-title {
  font-family: 'Playfair Display', serif; font-size: 14px; font-weight: 600;
  color: var(--platinum); margin: 0 0 16px; display: flex; align-items: center; gap: 8px;
}
.step-badge {
  background: var(--gold-soft); border: 1px solid rgba(201,168,76,0.3);
  border-radius: 999px; padding: 2px 10px;
  font-size: 10px; font-weight: 600; letter-spacing: 1px;
  color: var(--gold); text-transform: uppercase;
}
.step-badge.done { background: rgba(16,185,129,0.1); border-color: rgba(16,185,129,0.3); color: var(--emerald); }

/* ── Success/info/warning ── */
.stSuccess { background: rgba(16,185,129,0.1) !important; border: 1px solid rgba(16,185,129,0.25) !important; border-radius: var(--r) !important; }
.stInfo    { background: rgba(59,130,246,0.1) !important; border: 1px solid rgba(59,130,246,0.25) !important; border-radius: var(--r) !important; }
.stWarning { background: rgba(201,168,76,0.1)  !important; border: 1px solid rgba(201,168,76,0.25)  !important; border-radius: var(--r) !important; }

/* ── Spinners ── */
.stSpinner > div { border-top-color: var(--gold) !important; }

/* ── Divider ── */
.nexus-divider { height: 1px; background: var(--rim); margin: 28px 0; }

/* ── Fade-up animation ── */
@keyframes fadeUp { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
.animate { animation: fadeUp 0.55s ease both; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--rim); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
  background: linear-gradient(135deg, rgba(201,168,76,0.15), rgba(201,168,76,0.05)) !important;
  border-color: rgba(201,168,76,0.4) !important; color: var(--gold) !important;
  font-weight: 600 !important; font-size: 14px !important;
}
[data-testid="stDownloadButton"] > button:hover {
  box-shadow: 0 0 18px var(--gold-glow) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] { background: var(--raised) !important; border: 1px solid var(--rim) !important; border-radius: var(--r) !important; }
[data-testid="stExpander"] summary { color: var(--platinum) !important; }
</style>
""", unsafe_allow_html=True)

# ─── Topbar ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <p class="topbar-wordmark">DraftMind AI</p>
  <div class="topbar-divider"></div>
  <p class="topbar-subtitle">Dissertation Report Generator</p>
  <div class="topbar-badge">System Ready</div>
</div>
""", unsafe_allow_html=True)

# ─── Helpers ─────────────────────────────────────────────────────────────────
directory = "OutputFiles"

def read_file_auto_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw = f.read()
        enc = chardet.detect(raw)['encoding']
        return raw.decode(enc or 'utf-8', errors='replace')

def _list_to_str(val):
    """Convert JSON list to newline-separated string if needed."""
    if isinstance(val, list):
        return "\n".join(str(item) for item in val)
    if isinstance(val, dict):
        return json.dumps(val, indent=2)
    return str(val) if val is not None else ""

def _extract_result_plot_summary(val):
    """Flatten result_plot_summary from JSON."""
    if isinstance(val, dict) and "table" in val:
        rows = []
        for row in val["table"]:
            rows.append(
                f"Plot {row.get('Plot_Number','')}: {row.get('Title','')} | "
                f"Type: {row.get('Type','')} | Insights: {row.get('Insights','')}"
            )
        return "\n\n".join(rows)
    return _list_to_str(val)

def _extract_result_table(val):
    """Flatten result_table from JSON."""
    if not isinstance(val, dict):
        return _list_to_str(val)
    lines = []
    for table_key, table_data in val.items():
        if isinstance(table_data, dict):
            lines.append(f"\n### {table_key.replace('_', ' ').title()}")
            note = table_data.get("note", "")
            if note:
                lines.append(f"Note: {note}")
            cols = table_data.get("columns", [])
            rows = table_data.get("rows", [])
            if cols:
                lines.append(" | ".join(cols))
                lines.append(" | ".join(["---"] * len(cols)))
            for row in rows:
                lines.append(" | ".join(str(c) for c in row))
    return "\n".join(lines)

def _extract_code_summary_with_values(val):
    """Flatten the nested code_summary_with_values dict."""
    if isinstance(val, dict):
        return json.dumps(val, indent=2)
    return _list_to_str(val)

# ─── Session state ────────────────────────────────────────────────────────────
if 'generation_step' not in st.session_state:
    st.session_state.generation_step = 0

if 'sections_generated' not in st.session_state:
    st.session_state.sections_generated = {
        'keywords': False, 'citations': False, 'abstract': False,
        'introduction': False, 'methodology': False,
        'implementation': False, 'results': False
    }

if 'json_loaded' not in st.session_state:
    st.session_state.json_loaded = False

if 'json_data' not in st.session_state:
    st.session_state.json_data = {}

if 'lr_loaded' not in st.session_state:
    st.session_state.lr_loaded = False

if 'lr_filename' not in st.session_state:
    st.session_state.lr_filename = ""

if 'generation_running' not in st.session_state:
    st.session_state.generation_running = False

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <p class="sb-title">✦ DraftMind AI</p>
      <p class="sb-sub">Academic Report Engine · v2.0</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Generation Progress ──
    st.markdown('<div class="sb-label">Generation Progress</div>', unsafe_allow_html=True)

    steps_meta = [
        ("Keywords & Citations", ["keywords", "citations"]),
        ("Abstract",             ["abstract"]),
        ("Introduction",         ["introduction"]),
        ("Methodology",          ["methodology"]),
        ("Implementation",       ["implementation"]),
        ("Results & Conclusion", ["results"]),
    ]

    _sg = st.session_state.get("sections_generated", {})
    _gstep = st.session_state.get("generation_step", 0)

    for i, (name, keys) in enumerate(steps_meta):
        done   = all(_sg.get(k, False) for k in keys)
        active = (_gstep == i + 1)
        dot_cls = "done" if done else ("active" if active else "")
        icon    = "✓" if done else str(i + 1)
        txt_color = "#10b981" if done else ("#c9a84c" if active else "#6b7280")
        st.markdown(f"""
        <div class="step-row">
          <div class="step-dot {dot_cls}">{icon}</div>
          <span style="color:{txt_color};font-size:12px">{name}</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Input Source ──
    st.markdown('<div class="sb-label">Input Source</div>', unsafe_allow_html=True)

    _json_loaded = st.session_state.get("json_loaded", False)
    _lr_loaded   = st.session_state.get("lr_loaded", False)
    _gen_count   = sum(1 for v in _sg.values() if v)

    _jcolor = "#10b981" if _json_loaded else "#ef4444"
    _jicon  = "●" if _json_loaded else "○"
    _jtext  = "JSON Loaded" if _json_loaded else "Manual Input"

    _lcolor = "#10b981" if _lr_loaded else "#ef4444"
    _licon  = "●" if _lr_loaded else "○"
    _ltext  = "LR Loaded" if _lr_loaded else "No LR File"

    st.markdown(f"""
    <div class="stat-tile">
      <p class="stat-value" style="font-size:13px;color:{_jcolor}">{_jicon} {_jtext}</p>
      <p class="stat-label">JSON Data</p>
    </div>
    <div class="stat-tile">
      <p class="stat-value" style="font-size:13px;color:{_lcolor}">{_licon} {_ltext}</p>
      <p class="stat-label">Literature Review</p>
    </div>
    <div class="stat-tile">
      <p class="stat-value">{_gen_count}<span style="font-size:14px;color:#6b7280">/7</span></p>
      <p class="stat-label">Sections Done</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Actions ──
    if _json_loaded:
        st.markdown('<div class="sb-label">Actions</div>', unsafe_allow_html=True)
        st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
        if st.button("✕ Clear JSON & Reset"):
            st.session_state.json_loaded = False
            st.session_state.json_data = {}
            st.session_state.generation_step = 0
            st.session_state.sections_generated = {k: False for k in st.session_state.sections_generated}
            st.session_state.lr_loaded = False
            st.session_state.lr_filename = ""
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ─── Main Content ─────────────────────────────────────────────────────────────
st.markdown('<div class="content-wrap animate">', unsafe_allow_html=True)

# ── Page heading ──
st.markdown("""
<h1 style="font-family:'Playfair Display',serif;font-size:30px;font-weight:700;
           color:var(--platinum);margin:0 0 6px;letter-spacing:0.3px">
  Dissertation Report
  <span style="color:var(--gold)">Auto-Generation</span>
</h1>
<p style="font-size:13px;color:var(--mist);margin:0 0 28px">
  Upload a project JSON to auto-fill all fields, or enter your research details manually below.
</p>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 0 — JSON UPLOAD
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-card">
  <div class="section-heading">◆ &nbsp;JSON Project Upload</div>
</div>
""", unsafe_allow_html=True)

# Re-render inside the card properly using st elements
with st.container():
    st.markdown('<div class="section-card" style="margin-top:-20px">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">◆ &nbsp;JSON Project Upload</div>', unsafe_allow_html=True)

    if st.session_state.json_loaded:
        loaded_title = st.session_state.json_data.get("title", "Untitled Project")[:70]
        st.markdown(f"""
        <div class="json-loaded-banner">
          <span class="jlb-icon">✦</span>
          <div>
            <div class="jlb-text">JSON Successfully Loaded</div>
            <div class="jlb-sub">{loaded_title}…</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.info("All fields below have been pre-filled from the JSON. You may edit them before generating.")
    else:
        st.markdown("""
        <div class="upload-zone">
          <div class="upload-icon">⬆</div>
          <div class="upload-title">Upload Project JSON</div>
          <div class="upload-sub">Drop your <code>project_analysis.json</code> file here to auto-populate all fields</div>
        </div>
        """, unsafe_allow_html=True)

        uploaded_json = st.file_uploader(
            "Select JSON file",
            type=["json"],
            label_visibility="collapsed",
            key="json_uploader"
        )

        if uploaded_json is not None:
            try:
                raw = uploaded_json.read().decode("utf-8")
                data = json.loads(raw)
                st.session_state.json_data = data
                st.session_state.json_loaded = True
                st.success("JSON parsed successfully — all fields populated below.")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to parse JSON: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# ── Helper to get default value (JSON if loaded, else empty) ──
def default(key, fallback="", transform=None):
    if st.session_state.json_loaded and key in st.session_state.json_data:
        val = st.session_state.json_data[key]
        if transform:
            return transform(val)
        return _list_to_str(val)
    return fallback

# ── Helper to extract text from uploaded LR file ──
def extract_text_from_upload(uploaded_file):
    name = uploaded_file.name.lower()
    raw = uploaded_file.read()
    if name.endswith(".txt"):
        enc = chardet.detect(raw)['encoding'] or 'utf-8'
        return raw.decode(enc, errors='replace')
    elif name.endswith(".pdf"):
        if _PYPDF_OK:
            try:
                reader = _pypdf_mod.PdfReader(io.BytesIO(raw))
                return "\n\n".join(page.extract_text() or "" for page in reader.pages)
            except Exception as e:
                return f"[PDF extraction failed: {e}]"
        else:
            return "[PDF extraction unavailable — please install pypdf: pip install pypdf]"
    elif name.endswith(".docx"):
        if _DOCX_OK:
            try:
                doc = _docx_mod.Document(io.BytesIO(raw))
                return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
            except Exception as e:
                return f"[DOCX extraction failed: {e}]"
        else:
            return "[DOCX extraction unavailable — please install python-docx: pip install python-docx]"
    else:
        enc = chardet.detect(raw)['encoding'] or 'utf-8'
        return raw.decode(enc, errors='replace')

st.markdown('<div class="nexus-divider"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION LR — LITERATURE REVIEW UPLOAD
# ══════════════════════════════════════════════════════════════════════════════
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">◆ &nbsp;Literature Review Upload</div>', unsafe_allow_html=True)

    if st.session_state.lr_loaded:
        st.markdown(f"""
        <div class="json-loaded-banner">
          <span class="jlb-icon">✦</span>
          <div>
            <div class="jlb-text">Literature Review Loaded</div>
            <div class="jlb-sub">{st.session_state.lr_filename}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.info("LR file saved to InputFiles/lr.txt and will be inserted after Introduction in the final document.")
        st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
        if st.button("✕  Remove LR File", key="remove_lr"):
            st.session_state.lr_loaded = False
            st.session_state.lr_filename = ""
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="upload-zone">
          <div class="upload-icon">⬆</div>
          <div class="upload-title">Upload Literature Review</div>
          <div class="upload-sub">Supports <code>.pdf</code>, <code>.txt</code>, <code>.docx</code> — will be inserted after Introduction</div>
        </div>
        """, unsafe_allow_html=True)

        uploaded_lr = st.file_uploader(
            "Select LR file",
            type=["pdf", "txt", "docx"],
            label_visibility="collapsed",
            key="lr_uploader"
        )

        if uploaded_lr is not None:
            try:
                lr_text = extract_text_from_upload(uploaded_lr)

                # Split into body and references section
                # Find where references section starts (case-insensitive)
                ref_match = re.search(r'(?i)\n\s*references?\s*\n', lr_text)
                if ref_match:
                    lr_body = lr_text[:ref_match.start()].strip()
                    lr_refs = lr_text[ref_match.end():].strip()
                else:
                    lr_body = lr_text.strip()
                    lr_refs = ""

                # Save LR body to OutputFiles/lr.txt (used in final document)
                os.makedirs("OutputFiles", exist_ok=True)
                save_text_file(lr_body, "OutputFiles/lr.txt")

                # Save LR references to OutputFiles/references_lr.txt
                if lr_refs:
                    save_text_file(lr_refs, "OutputFiles/references_lr.txt")

                st.session_state.lr_loaded = True
                st.session_state.lr_filename = uploaded_lr.name
                st.success(f"Literature Review saved — {len(lr_body.split())} words extracted" + (f", {len(lr_refs.splitlines())} reference lines found." if lr_refs else "."))
                st.rerun()
            except Exception as e:
                st.error(f"Failed to process LR file: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS — Input Fields  |  Generation Pipeline
# ══════════════════════════════════════════════════════════════════════════════
tab_input, tab_eda, tab_files, tab_gen = st.tabs(["✦ Input Fields", "📋 Extract Data Prompt", "📦 Input Files", "⚡ Generation Pipeline"])

with tab_input:

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — RESEARCH DETAILS
# ══════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-card"><div class="section-heading">① &nbsp;Research Details</div>', unsafe_allow_html=True)

    title = st.text_area("Title of the Research", value=default("title"), height=80)
    format_val = st.selectbox("Select Format", ["1", "2", "3", "4"])
    question = st.text_area("Research Question", value=default("research_question"), height=100)
    objective = st.text_area("Research Objectives", value=default("research_objectives", transform=lambda v: "\n".join(v) if isinstance(v, list) else _list_to_str(v)), height=160)
    data_details = st.text_area("Data Details (dataset info & source link)", value=default("data_details"), height=110)
    save_text_file(data_details, "InputFiles/dd.txt")

    pipeline_val = st.text_area(
        "Research Pipeline",
        value=default("code_pipeline"),
        height=200,
        placeholder="Paste or auto-fill the research/code pipeline steps here…"
    )
    save_text_file(pipeline_val, "InputFiles/pipeline.txt")

    if pipeline_val.strip():
        with st.expander("🔍 Pipeline Preview", expanded=False):
            st.markdown(
                f"<pre style='background:var(--raised);border:1px solid var(--rim);border-radius:8px;"
                f"padding:16px;font-size:12px;color:var(--platinum);white-space:pre-wrap;"
                f"word-break:break-word;line-height:1.6;font-family:monospace'>"
                f"{pipeline_val.replace('<','&lt;').replace('>','&gt;')}</pre>",
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — LITERATURE & RESEARCH GAPS
# ══════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-card"><div class="section-heading">② &nbsp;Literature Review & Research Gaps</div>', unsafe_allow_html=True)

    LITERATURE_REVIEW_PROMPT = "Analyze the given Literature Review and generate a structured summary while preserving all essential technical content and citations. Before summarization, conduct a background search to understand the topic thoroughly. The summary should be 15-20% of the original length while maintaining clarity, coherence, and completeness.Summary Must Include:Topic Overview: Provide a concise background and relevance of the topic based on the Literature Review.Importance of the Chosen Field (with Citations): Explain why this field of research is significant, its real-world applications, and its impact on industries, society, or technology.Key Technical Content: Extract critical theories, models, methodologies, or frameworks discussed.Findings & Insights: Summarize major findings, patterns, or trends identified in the literature.Limitations Identified: Highlight gaps, weaknesses, or missing elements in existing research.Unresolved Issues: Mention ongoing debates, contradictions, or unanswered questions that remain open for further study.Preserve Citations: Retain all references and in-text citations exactly as they appear in the original document.Parameters:Background Search: First, gather relevant information to ensure a well-informed summary.Word Limit: Compress to 15-20% of the original content (i.e., 525-700 words for 3,500 words).Technical Accuracy: Maintain integrity of complex concepts, models, and frameworks.Mention all the important values like performance percentage if present.Clarity & Coherence: Ensure readability and logical flow.Citation Integrity: Do not remove or alter any references; they must be retained as in the original document.Deliver the summary in a well-structured format while ensuring all major points, technical details, and research gaps are clearly presented."

    components.html(f"""
<style>
  button {{
    background: rgba(201,168,76,0.10); color: #c9a84c; border: 1px solid rgba(201,168,76,0.3);
    border-radius: 8px; padding: 8px 16px; font-size: 12px; font-family: Outfit, sans-serif;
    cursor: pointer; letter-spacing: 0.5px; transition: all 0.2s;
  }}
  button:hover {{ background: rgba(201,168,76,0.2); box-shadow: 0 0 12px rgba(201,168,76,0.3); }}
</style>
<button onclick="navigator.clipboard.writeText(`{LITERATURE_REVIEW_PROMPT}`).then(()=>alert('Copied!'))">
  ⎘ Copy Literature Review Prompt
</button>
""", height=50)

    literature_review_summary = st.text_area("Literature Review Summary", value=default("literature_review_summary"), height=250)
    save_text_file(literature_review_summary, "InputFiles/lrs.txt")

    research_gaps = st.text_area("Research Gaps (from Literature Review)", value=default("research_gap"), height=200)
    save_text_file(research_gaps, "InputFiles/rg.txt")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — BASE PAPER
# ══════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-card"><div class="section-heading">③ &nbsp;Base Paper</div>', unsafe_allow_html=True)

    BASE_PAPER_PROMPT = "Instructions: 1. What is the complete flow or pipeline of research 2. Details of the data getting used. 3. What is the accuracy of all the methods used 4. Which algorithm achieved best accuracy and what is it 5. What is the novel or unique element in the research 6. What are the future recommendations of the research paper All in 500 words."

    components.html(f"""
<style>
  button {{
    background: rgba(201,168,76,0.10); color: #c9a84c; border: 1px solid rgba(201,168,76,0.3);
    border-radius: 8px; padding: 8px 16px; font-size: 12px; font-family: Outfit, sans-serif;
    cursor: pointer; letter-spacing: 0.5px; transition: all 0.2s;
  }}
  button:hover {{ background: rgba(201,168,76,0.2); }}
</style>
<button onclick="navigator.clipboard.writeText(`{BASE_PAPER_PROMPT}`).then(()=>alert('Copied!'))">
  ⎘ Copy Base Paper Prompt
</button>
""", height=50)

    base_paper_summary = st.text_area("Base Paper Summary", value=default("base_paper_summary"), height=200)
    save_text_file(base_paper_summary, "InputFiles/bps.txt")

    base_paper_citation = st.text_area("Base Paper Citation", value=default("base_paper_reference"), height=80)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — CODE ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-card"><div class="section-heading">④ &nbsp;Code Analysis</div>', unsafe_allow_html=True)

    CODE_SUMMARY_PROMPT = "Summarize the following code, which focuses on [extract key focus from the code, e.g., machine learning, web scraping, financial analysis, etc.], into 2-3 concise paragraphs while preserving all essential technical details.Summary must include:Overview: Purpose and functionality of the code.Key Components: Main functions, classes, or modules and their roles.Execution Flow: How the code runs from input to output.Core Logic: Important algorithms or computations.Web App Elements (if any): API endpoints, routes, or database interactions.Parameters:Format: Paragraph-based (2-3 paragraphs).Conciseness: 15-20% of original length.Technical Accuracy: Preserve key function names and logic.Readability: Clear, structured, and informative.Deliver the summary in a well-structured, readable format with a clear focus on the main purpose of the code."

    components.html(f"""
<style>
  button {{
    background: rgba(201,168,76,0.10); color: #c9a84c; border: 1px solid rgba(201,168,76,0.3);
    border-radius: 8px; padding: 8px 16px; font-size: 12px; font-family: Outfit, sans-serif;
    cursor: pointer; letter-spacing: 0.5px; transition: all 0.2s;
  }}
  button:hover {{ background: rgba(201,168,76,0.2); }}
</style>
<button onclick="navigator.clipboard.writeText(`{CODE_SUMMARY_PROMPT}`).then(()=>alert('Copied!'))">
  ⎘ Copy Code Summary Prompt
</button>
""", height=50)

    code_summary = st.text_area("Code Summary", value=default("code_summary"), height=160)
    save_text_file(code_summary, "InputFiles/cs.txt")

    CODE_SUMMARY_WITH_VALUES_PROMPT = "Analyze the given code (~1000 lines) stored in a .txt file. Extract a list of libraries used and segment the code into the following categories, ensuring all details are accurately captured.Required Segments:Statistical Analysis:Identify all functions used for statistical analysis.Provide their purpose and the outcome they generate.Exploratory Data Analysis (EDA):Extract details of each plot, including:Plot Type (e.g., histogram, scatter plot, box plot, etc.).Plot Title and what it represents.X and Y Variables being analyzed.Insights from each visualization, explaining trends, patterns, outliers, and distributions.If there are correlation matrices or summary statistics, include key takeaways.Data Preprocessing:List functions used for preprocessing (e.g., scaling, encoding, missing value treatment).Specify parameters and their values for each function.Do not mention Train-Test-Split hereFeature EngineeringMention all the selected column names if feature selection is done.Train Split InformationModel Details:Identify functions used for model building and training .Mention the name of the tuning method if done.List the models used and their associated parameters.If the code has both a base model (default parameters) and a tuned model (optimized parameters), display them separately.Model Results & Performance Evaluation:First, list the performance metrics used for evaluation.Then, provide a table showing:Algorithm namePerformance values across each metric (e.g., accuracy, precision, recall, RMSE, etc.).If multiple models are compared, highlight which model performed best.Parameters:Format: Structured and well-organized for readability.Conciseness: Extract only relevant details while ensuring completeness.Technical Accuracy: Preserve function names, parameters, and values.Insightful Output: Provide meaningful explanations, especially in the EDA section.Ensure that all extracted details are correctly categorized and that model performance is clearly presented with insightful comparisons."

    components.html(f"""
<style>
  button {{
    background: rgba(201,168,76,0.10); color: #c9a84c; border: 1px solid rgba(201,168,76,0.3);
    border-radius: 8px; padding: 8px 16px; font-size: 12px; font-family: Outfit, sans-serif;
    cursor: pointer; letter-spacing: 0.5px; transition: all 0.2s;
  }}
  button:hover {{ background: rgba(201,168,76,0.2); }}
</style>
<button onclick="navigator.clipboard.writeText(`{CODE_SUMMARY_WITH_VALUES_PROMPT}`).then(()=>alert('Copied!'))">
  ⎘ Copy Code Summary With Values Prompt
</button>
""", height=50)

    code_summary_with_values = st.text_area(
        "Code Summary With Values",
        value=default("code_summary_with_values", transform=_extract_code_summary_with_values),
        height=200
    )
    save_text_file(code_summary_with_values, "InputFiles/csvs.txt")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — WEB APP
# ══════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-card"><div class="section-heading">⑤ &nbsp;Web Application</div>', unsafe_allow_html=True)

    WEBAPP_PROMPT = "Analyze the given web application code and generate a concise summary (150-200 words) covering all key functionalities and technical components. Summary Must Include:Overview: Briefly describe the purpose and functionality of the web app.Python Framework Used: Clearly state the web framework (e.g., Flask, Django, FastAPI, streamlit, etc) used in the application.Libraries & Dependencies: List all major libraries and dependencies.User Input Handling: Explain how user input is collected (e.g., input text box, file upload, dropdown, etc.).Main Functions & Features: Summarize key functions, including API endpoints, data processing, and UI components.Prediction Function: Provide a focused explanation of the core prediction logic, including the model used and how it processes input data.Parameters:Conciseness: Keep the summary within 100-150 words while ensuring completeness.Technical Accuracy: Retain function names and their core purpose.Readability: Ensure the summary is clear and structured for easy understanding.Deliver the summary in a well-structured format while preserving all critical details of the web application."

    components.html(f"""
<style>
  button {{
    background: rgba(201,168,76,0.10); color: #c9a84c; border: 1px solid rgba(201,168,76,0.3);
    border-radius: 8px; padding: 8px 16px; font-size: 12px; font-family: Outfit, sans-serif;
    cursor: pointer; letter-spacing: 0.5px; transition: all 0.2s;
  }}
  button:hover {{ background: rgba(201,168,76,0.2); }}
</style>
<button onclick="navigator.clipboard.writeText(`{WEBAPP_PROMPT}`).then(()=>alert('Copied!'))">
  ⎘ Copy Web App Prompt
</button>
""", height=50)

    webapp_summary = st.text_area("Web App Summary", value=default("web_app_summary"), height=140)
    save_text_file(webapp_summary, "InputFiles/ws.txt")

    WEB_APP_TEST_PROMPT = "Provide me the insight of the web test result in 80 words with mentioning each of the values and don't use parenthesis to mention values'()'"

    components.html(f"""
<style>
  button {{
    background: rgba(201,168,76,0.10); color: #c9a84c; border: 1px solid rgba(201,168,76,0.3);
    border-radius: 8px; padding: 8px 16px; font-size: 12px; font-family: Outfit, sans-serif;
    cursor: pointer; letter-spacing: 0.5px; transition: all 0.2s;
  }}
  button:hover {{ background: rgba(201,168,76,0.2); }}
</style>
<button onclick="navigator.clipboard.writeText(`{WEB_APP_TEST_PROMPT}`).then(()=>alert('Copied!'))">
  ⎘ Copy Web App Testing Prompt
</button>
""", height=50)

    webapp_test = st.text_area("Web App Test Case Results", value=default("web_app_test_cases"), height=140)
    save_text_file(webapp_test, "InputFiles/wat.txt")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — NOVELTY & RESULTS
# ══════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-card"><div class="section-heading">⑥ &nbsp;Novelty & Results</div>', unsafe_allow_html=True)

    NOVELTY_PROMPT = "Analyze the provided code and identify its novelty in depth in 300 words para. Explain the unique aspects, innovations, or optimizations present in the code, including algorithmic improvements, architectural design, efficiency enhancements, and any novel methodologies or techniques applied. Discuss how these aspects contribute to the overall performance, maintainability, and scalability of the system."

    components.html(f"""
<style>
  button {{
    background: rgba(201,168,76,0.10); color: #c9a84c; border: 1px solid rgba(201,168,76,0.3);
    border-radius: 8px; padding: 8px 16px; font-size: 12px; font-family: Outfit, sans-serif;
    cursor: pointer; letter-spacing: 0.5px; transition: all 0.2s;
  }}
  button:hover {{ background: rgba(201,168,76,0.2); }}
</style>
<button onclick="navigator.clipboard.writeText(`{NOVELTY_PROMPT}`).then(()=>alert('Copied!'))">
  ⎘ Copy Novelty Prompt
</button>
""", height=50)

    novelty = st.text_area("Novelty", value=default("novelty"), height=160)
    save_text_file(novelty, "InputFiles/novelty.txt")

    RESULTS_PLOT_PROMPT = "Requirements:1. create a table 2. mention all the plots individually do not write collectively3. mention all plots for all the modelsTable 1- all result plot information table:Title: Title of the plots from codeType of plot: Type of plot [Bar chart, Pie chart, etc]Insights: Insights of the chart from the code which should include the values presentCharts can be considered in Table 1: Explainable AI, ROC, AUC, Training and loss neural network, comparison curve, confusion matrixNote:1. Do not include any plot from data exploration, preprocessing, feature engineering, or data transformation steps.2. For the comparison plots mention insight as 'will be taken from table'"

    components.html(f"""
<style>
  button {{
    background: rgba(201,168,76,0.10); color: #c9a84c; border: 1px solid rgba(201,168,76,0.3);
    border-radius: 8px; padding: 8px 16px; font-size: 12px; font-family: Outfit, sans-serif;
    cursor: pointer; letter-spacing: 0.5px; transition: all 0.2s;
  }}
  button:hover {{ background: rgba(201,168,76,0.2); }}
</style>
<button onclick="navigator.clipboard.writeText(`{RESULTS_PLOT_PROMPT}`).then(()=>alert('Copied!'))">
  ⎘ Copy Results Plot Prompt
</button>
""", height=50)

    result_plot_summary = st.text_area(
        "Result Plot Summary",
        value=default("result_plot_summary", transform=_extract_result_plot_summary),
        height=220
    )

    RESULTS_TABLE_PROMPT = "Generate a table for: Performance Table: Include all models, all metrics (as extracted from the code), and highlight the best-performing model."

    components.html(f"""
<style>
  button {{
    background: rgba(201,168,76,0.10); color: #c9a84c; border: 1px solid rgba(201,168,76,0.3);
    border-radius: 8px; padding: 8px 16px; font-size: 12px; font-family: Outfit, sans-serif;
    cursor: pointer; letter-spacing: 0.5px; transition: all 0.2s;
  }}
  button:hover {{ background: rgba(201,168,76,0.2); }}
</style>
<button onclick="navigator.clipboard.writeText(`{RESULTS_TABLE_PROMPT}`).then(()=>alert('Copied!'))">
  ⎘ Copy Results Table Prompt
</button>
""", height=50)

    result_table_summary = st.text_area(
        "Result Table Summary",
        value=default("result_table", transform=_extract_result_table),
        height=180
    )
    save_text_file(result_plot_summary + "\n\n" + result_table_summary, "InputFiles/rs.txt")

    FAILED_ATTEMPTS_PROMPT = "Discuss any failed attempts. At the beginning, write a short introduction of 25 to 35 words for this section. Add a performance result table if available. Mension why a particular method is suitable than other, as per your analysis. Please modify the subheadings to better suit the research project topic. Use clear, meaningful titles. Word count can go up to 100 words."

    components.html(f"""
<style>
  button {{
    background: rgba(201,168,76,0.10); color: #c9a84c; border: 1px solid rgba(201,168,76,0.3);
    border-radius: 8px; padding: 8px 16px; font-size: 12px; font-family: Outfit, sans-serif;
    cursor: pointer; letter-spacing: 0.5px; transition: all 0.2s;
  }}
  button:hover {{ background: rgba(201,168,76,0.2); }}
</style>
<button onclick="navigator.clipboard.writeText(`{FAILED_ATTEMPTS_PROMPT}`).then(()=>alert('Copied!'))">
  ⎘ Copy Failed Attempts Prompt
</button>
""", height=50)

    failed_attempt_summary = st.text_area("Failed Attempt Summary", value=default("failed_attempts"), height=180)
    save_text_file(result_plot_summary + "\n\n" + failed_attempt_summary, "InputFiles/fa.txt")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG UPDATE  (same fields as original)
# ══════════════════════════════════════════════════════════════════════════════
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

config["TITLE"]              = title
config["FORMAT"]             = format_val
config['RESEARCH_QUESTION']  = question
config['RESEARCH_OBJECTIVES'] = objective
config["BASE_PAPER_CITATION"] = base_paper_citation
config["PROMPT"]             = "ed.txt"

with open("config.yaml", "w") as f:
    yaml.dump(config, f, default_flow_style=False)

# ══════════════════════════════════════════════════════════════════════════════
# EXTRACT DATA PROMPT TAB
# ══════════════════════════════════════════════════════════════════════════════

# Full prompt from ed.txt — DATA_DETAILS_PLACEHOLDER is swapped at runtime
_ED_PROMPT_RAW = (
    "Data Details:\n"
    "DATA_DETAILS_PLACEHOLDER\n\n"
    "Attached files to analyse [ZIP], it will contain:\n"
    "Proposal\n"
    "Literature Review\n"
    "Complete code in ipynb format\n\n"
    "title: Fetch it from the attached proposal\n"
    "Research question: Fetch it from the attached proposal\n"
    "Research objectives: Fetch these from the attached proposal\n"
    "acc_value: best accuracy values achieved\n\n"
    "## LITERATURE REVIEW SUMMARY\n"
    "Analyze the given Literature Review and generate a structured summary while preserving all essential technical content and citations. Before summarization, conduct a background search to understand the topic thoroughly. The summary should be 15-20% of the original length while maintaining clarity, coherence, and completeness. Summary Must Include: Topic Overview, Importance of the Chosen Field (with Citations), Key Technical Content, Findings & Insights, Limitations Identified, Unresolved Issues, Preserve Citations. Parameters: Word Limit 525-700 words for 3,500 words. Technical Accuracy: Maintain integrity of complex concepts. Mention all important values like performance percentage. Citation Integrity: Do not remove or alter any references.\n\n"
    "## RESEARCH GAP\n"
    "Using the literature review that I have already collected and the research pipeline on which I have completed my research code, write a proper research gap. This research gap should be in a way that it points to those methods which I have used in the code and were missing or suggested in the literature. Do not explicitly mention my research. Word count: 300 words.\n\n"
    "## BASE PAPER\n"
    "can you find only one research paper which is based on {title} and having accuracy below {acc_value} research paper should be from the past 2 years.\n"
    "Instructions:\n"
    "1. What is the complete flow or pipeline of research\n"
    "2. Details of the data getting used.\n"
    "3. What is the accuracy of all the algorithms used?\n"
    "4. Which algorithm achieved best accuracy and what is it\n"
    "5. What is the novel or unique element in the research\n"
    "6. What are the future recommendations of the research paper?\n"
    "All in 500 words. Provide reference in Harvard style.\n\n"
    "## CODE SUMMARY\n"
    "Summarize the following code into 2-3 concise paragraphs while preserving all essential technical details. Summary must include: Overview, Key Components, Execution Flow, Core Logic, Web App Elements (if any). Format: Paragraph-based, 15-20% of original length. Word count: 300 words.\n\n"
    "## CODE SUMMARY WITH VALUES\n"
    "Analyze the given code (~1000 lines). Extract a list of libraries used and segment into: Statistical Analysis, Exploratory Data Analysis (EDA) with plot details, Data Preprocessing, Feature Engineering, Train Split Information, Model Details (including layers for deep learning), Model Results & Performance Evaluation table. Format: Structured and well-organized.\n\n"
    "## WEBAPP SUMMARY\n"
    "Analyze the given web application code and generate a concise summary (150-200 words) covering: Overview, Python Framework Used, Libraries & Dependencies, User Input Handling, Main Functions & Features, Prediction Function.\n\n"
    "## WEBAPP TEST CASES\n"
    "Provide me the insight of the web test result in 150 words with mentioning each of the values and don't use parenthesis to mention values'()'\n\n"
    "## NOVELTY\n"
    "You are an elite software researcher. Write a single well-structured paragraph of exactly ~300 words explaining the novelty of the code. Focus on: unique algorithmic improvements, distinctive architectural decisions, efficiency enhancements, novel engineering techniques, scalability/maintainability improvements, trade-offs made. Maintain a formal research-oriented tone similar to a top-tier conference paper (NeurIPS, ICSE, SOSP).\n\n"
    "## RESULTS PLOT SUMMARY\n"
    "Requirements: 1. Create a table. 2. Mention all plots individually. Table columns: Title, Type of plot, Insights. Charts: Explainable AI, ROC, AUC, Training and loss neural network, comparison curve, confusion matrix. Note: Do not include plots from data exploration/preprocessing steps. For comparison plots mention insight as 'will be taken from table'.\n\n"
    "## RESULTS TABLE\n"
    "Generate a table for: Performance Table: Include all models, all metrics (as extracted from the code), and highlight the best-performing model.\n\n"
    "## FAILED ATTEMPT\n"
    "Write a concise section titled 'Failed Attempts and Design Iterations'. Begin with a 25-35 word introduction. Describe unsuccessful/suboptimal methods and why they failed. Provide technical reasoning for each failure.\n\n"
    "## REFERENCES\n"
    "From the research pipeline/code, write approx 15 important keywords. For each keyword find a reference paper related to {title}. Parameters: Keyword, title, reference, citation. Reference in Harvard style.\n\n"
    "## Output format (JSON):\n"
    "{\n"
    "  'title': <title>,\n"
    "  'research_question': <Research question>,\n"
    "  'research_objectives': <Research objectives>,\n"
    "  'data_details': <Data Details>,\n"
    "  'literature_review_summary': <LR summary>,\n"
    "  'research_gap': <research gap>,\n"
    "  'best_accuracy': <acc_value>,\n"
    "  'base_paper_summary': <summary>,\n"
    "  'base_paper_reference': <reference>,\n"
    "  'code_summary': <code summary>,\n"
    "  'code_summary_with_values': <code summary with values>,\n"
    "  'web_app_summary': <web app summary>,\n"
    "  'web_app_test_cases': <web app test cases>,\n"
    "  'novelty': <novelty>,\n"
    "  'result_plot_summary': <result plot summary>,\n"
    "  'result_table': <result table>,\n"
    "  'failed_attempts': <failed attempts>,\n"
    "  'references': <references>\n"
    "}"
)

with tab_eda:
    st.markdown('<div class="section-card"><div class="section-heading">📋 &nbsp;Extract Data Prompt</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size:12px;color:var(--mist);margin:0 0 18px">
      Enter your data details below. They will be injected into the prompt automatically.
      Copy the full prompt and send it together with your ZIP file to an AI tool.
    </p>
    """, unsafe_allow_html=True)

    eda_data_details = st.text_area(
        "Data Details",
        value=data_details,
        height=130,
        key="eda_data_details_input",
        placeholder="e.g. Dataset: Heart disease dataset from Kaggle. 303 rows, 14 columns including Age, Cholesterol, Target..."
    )

    # Inject data_details into the template via plain string replace — no .format() to avoid {} conflicts
    _dd = eda_data_details.strip() if eda_data_details.strip() else "<paste your data details here>"
    full_ed_prompt = _ED_PROMPT_RAW.replace("DATA_DETAILS_PLACEHOLDER", _dd)

    # Save to InputFiles/ed.txt
    save_text_file(full_ed_prompt, "InputFiles/ed.txt")

    st.markdown("<div style='margin-top:18px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-heading" style="font-size:13px;margin-bottom:10px">Full Prompt Preview</div>', unsafe_allow_html=True)

    st.text_area(
        "prompt_preview",
        value=full_ed_prompt,
        height=340,
        key="ed_prompt_preview",
        label_visibility="collapsed"
    )

    # Copy button — write prompt into a hidden textarea then execCommand copy
    # Escape for safe embedding inside an HTML attribute
    _escaped = full_ed_prompt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    components.html(f"""
<style>
  #ed-copy-btn {{
    background: rgba(201,168,76,0.10); color: #c9a84c; border: 1px solid rgba(201,168,76,0.3);
    border-radius: 8px; padding: 10px 22px; font-size: 13px; font-family: Outfit, sans-serif;
    cursor: pointer; letter-spacing: 0.5px; transition: all 0.2s; margin-top: 4px;
  }}
  #ed-copy-btn:hover {{ background: rgba(201,168,76,0.22); box-shadow: 0 0 12px rgba(201,168,76,0.3); }}
</style>
<textarea id="ed-hidden" readonly style="position:fixed;top:-9999px;left:-9999px;opacity:0;">{_escaped}</textarea>
<button id="ed-copy-btn" onclick="
  var el = document.getElementById('ed-hidden');
  el.value = el.textContent;
  el.select();
  el.setSelectionRange(0, 99999);
  try {{
    document.execCommand('copy');
    this.textContent = 'Copied!';
  }} catch(e) {{
    navigator.clipboard.writeText(el.textContent).then(() => {{ this.textContent = 'Copied!'; }});
  }}
  var btn = this;
  setTimeout(function() {{ btn.textContent = 'Copy Full Prompt'; }}, 1800);
">Copy Full Prompt</button>
""", height=56)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# INPUT FILES TAB  — upload LR, Notebook, Web App, Proposal → download as ZIP
# ══════════════════════════════════════════════════════════════════════════════
with tab_files:
    import zipfile

    st.markdown("""
<h2 style="font-family:'Playfair Display',serif;font-size:22px;color:var(--platinum);margin:0 0 6px">
  Input Files
  <span style="color:var(--gold)">Package</span>
</h2>
<p style="font-size:12px;color:var(--mist);margin:0 0 22px">
  Upload the four source files below. Once all are uploaded a ZIP will be
  available for download — ready to attach to any AI prompt tool.
</p>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-heading">◆ &nbsp;Upload Source Files</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<p style="font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:var(--mist);margin:0 0 6px">Literature Review</p>', unsafe_allow_html=True)
        up_lr_pkg = st.file_uploader(
            "Literature Review file",
            type=["pdf", "txt", "docx"],
            label_visibility="collapsed",
            key="pkg_lr"
        )

        st.markdown('<p style="font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:var(--mist);margin:16px 0 6px">Code Notebook</p>', unsafe_allow_html=True)
        up_nb = st.file_uploader(
            "Code notebook file",
            type=["ipynb", "py", "txt"],
            label_visibility="collapsed",
            key="pkg_nb"
        )

    with col_b:
        st.markdown('<p style="font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:var(--mist);margin:0 0 6px">Web Application File</p>', unsafe_allow_html=True)
        up_web = st.file_uploader(
            "Web application file",
            type=["py", "txt", "html", "js"],
            label_visibility="collapsed",
            key="pkg_web"
        )

        st.markdown('<p style="font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:var(--mist);margin:16px 0 6px">Proposal File</p>', unsafe_allow_html=True)
        up_proposal = st.file_uploader(
            "Proposal file",
            type=["pdf", "docx", "txt"],
            label_visibility="collapsed",
            key="pkg_proposal"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Status overview ──
    _pkg_files = {
        "Literature Review":    up_lr_pkg,
        "Code Notebook":        up_nb,
        "Web Application File": up_web,
        "Proposal":             up_proposal,
    }
    _uploaded_count = sum(1 for f in _pkg_files.values() if f is not None)

    st.markdown('<div class="section-card"><div class="section-heading">◆ &nbsp;Files Status</div>', unsafe_allow_html=True)
    status_cols = st.columns(4)
    for idx, (label, ufile) in enumerate(_pkg_files.items()):
        with status_cols[idx]:
            _ok    = ufile is not None
            _color = "var(--emerald)" if _ok else "var(--mist)"
            _icon  = "✓" if _ok else "○"
            _name  = ufile.name if _ok else "—"
            st.markdown(f"""
            <div style="text-align:center;padding:12px 6px;background:var(--raised);border:1px solid var(--rim);
                        border-radius:8px;border-top:2px solid {'var(--emerald)' if _ok else 'var(--rim)'}">
              <div style="font-size:18px;color:{_color}">{_icon}</div>
              <div style="font-size:9px;color:{_color};letter-spacing:1px;text-transform:uppercase;margin-top:4px">{label}</div>
              <div style="font-size:10px;color:var(--mist);margin-top:4px;word-break:break-all">{_name}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Build ZIP and offer download ──
    if _uploaded_count > 0:
        # Map upload object → desired filename inside the ZIP
        _name_map = {
            "Literature Review":    ("lr",       up_lr_pkg),
            "Code Notebook":        ("notebook",  up_nb),
            "Web Application File": ("web_app",   up_web),
            "Proposal":             ("proposal",  up_proposal),
        }

        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for _label, (_base, _uf) in _name_map.items():
                if _uf is not None:
                    _ext  = os.path.splitext(_uf.name)[1]
                    _uf.seek(0)
                    zf.writestr(f"InputFiles/{_base}{_ext}", _uf.read())

        zip_buf.seek(0)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.download_button(
            label=f"⬇  Download ZIP ({_uploaded_count} file{'s' if _uploaded_count != 1 else ''})",
            data=zip_buf.getvalue(),
            file_name="data.zip",
            mime="application/zip"
        )

        _contents = [f"InputFiles/{_base}{os.path.splitext(_uf.name)[1]}"
                     for _, (_base, _uf) in _name_map.items() if _uf is not None]
        st.markdown(
            f"<p style='font-size:11px;color:var(--mist);margin:8px 0 0'>"
            f"ZIP contains: {', '.join(_contents)}</p>",
            unsafe_allow_html=True
        )
    else:
        st.info("Upload at least one file above to enable ZIP download.")

# ══════════════════════════════════════════════════════════════════════════════
# GENERATION PIPELINE TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_gen:
    st.markdown("""
<h2 style="font-family:'Playfair Display',serif;font-size:22px;color:var(--platinum);margin:0 0 6px">
  Document Generation
  <span style="color:var(--gold)">Pipeline</span>
</h2>
<p style="font-size:12px;color:var(--mist);margin:0 0 22px">
  Click <strong>Start</strong> — all sections will be generated automatically in sequence.
</p>
""", unsafe_allow_html=True)

    # ── Step definitions ──
    _step_labels = ["Keywords", "Citations", "Abstract", "Intro", "Method", "Impl.", "Results"]
    _step_keys   = ["keywords", "citations", "abstract", "introduction", "methodology", "implementation", "results"]
    _cur_step    = st.session_state.get("generation_step", 0)
    _is_running  = st.session_state.get("generation_running", False)

    # ── Progress tracker (live per-step rerun) ──
    prog_cols = st.columns(7)
    for i, (lbl, key) in enumerate(zip(_step_labels, _step_keys)):
        with prog_cols[i]:
            done   = st.session_state.sections_generated.get(key, False)
            active = _is_running and (_cur_step == i)
            if done:
                bg      = "rgba(16,185,129,0.10)"
                border  = "#10b981"
                top_clr = "#10b981"
                icon    = "\u2713"
                lbl_clr = "#10b981"
            elif active:
                bg      = "rgba(201,168,76,0.12)"
                border  = "#c9a84c"
                top_clr = "#c9a84c"
                icon    = str(i + 1)
                lbl_clr = "#c9a84c"
            else:
                bg      = "var(--raised)"
                border  = "var(--rim)"
                top_clr = "var(--rim)"
                icon    = str(i + 1)
                lbl_clr = "#6b7280"
            glow = "box-shadow:0 0 14px rgba(201,168,76,0.3);" if active else ""
            st.markdown(f"""
            <div style="text-align:center;padding:10px 4px;background:{bg};
                        border:1px solid {border};border-radius:8px;
                        border-top:2px solid {top_clr};{glow}transition:all 0.3s ease;">
              <div style="font-size:16px;color:{lbl_clr}">{icon}</div>
              <div style="font-size:9px;color:{lbl_clr};letter-spacing:1px;text-transform:uppercase;margin-top:4px">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── LR status row ──
    _lr_done      = st.session_state.get("lr_loaded", False)
    _lr_color     = "rgba(16,185,129,0.12)" if _lr_done else "rgba(239,68,68,0.08)"
    _lr_border    = "rgba(16,185,129,0.35)" if _lr_done else "rgba(239,68,68,0.3)"
    _lr_txt_color = "#10b981" if _lr_done else "#f87171"
    _lr_icon      = "\u2713" if _lr_done else "\u25cb"
    _lr_msg       = "Literature Review uploaded \u2014 will be inserted after Introduction in the final document." if _lr_done else "No Literature Review uploaded \u2014 it will be skipped in the final document."
    st.markdown(f"""
    <div style="margin-top:10px;padding:10px 16px;background:{_lr_color};border:1px solid {_lr_border};
                border-radius:8px;display:flex;align-items:center;gap:10px;">
      <span style="font-size:16px;color:{_lr_txt_color};flex-shrink:0">{_lr_icon}</span>
      <span style="font-size:11px;color:{_lr_txt_color};letter-spacing:0.3px">{_lr_msg}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Step-by-step rerun pattern for live progress ──
    all_done = _cur_step >= 7

    _step_funcs = [
        (generate_keywords,                                                      "keywords",       "Step 1/7 \u00b7 Generating keywords\u2026"),
        (lambda: get_ref_citation(st.session_state["json_data"]["references"]),  "citations",      "Step 2/7 \u00b7 Generating citations\u2026"),
        (generate_abstract,                                                      "abstract",       "Step 3/7 \u00b7 Generating abstract\u2026"),
        (generate_introduction,                                                  "introduction",   "Step 4/7 \u00b7 Generating introduction\u2026"),
        (generate_methodology,                                                   "methodology",    "Step 5/7 \u00b7 Generating methodology\u2026"),
        (generate_implementation,                                                "implementation", "Step 6/7 \u00b7 Generating implementation\u2026"),
        (generate_result_conclusion,                                             "results",        "Step 7/7 \u00b7 Generating results & conclusion\u2026"),
    ]

    if not all_done:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        start_clicked = st.button("\u2726  Start Generation Process")
        st.markdown('</div>', unsafe_allow_html=True)

        # Mid-generation: execute current step then rerun for next
        if _is_running and 0 <= _cur_step < 7:
            fn, key, label = _step_funcs[_cur_step]
            with st.spinner(label):
                fn()
            st.session_state.sections_generated[key] = True
            st.session_state.generation_step = _cur_step + 1
            if _cur_step + 1 >= 7:
                st.session_state.generation_running = False
            st.rerun()

        elif start_clicked and not _is_running:
            st.session_state.generation_running = True
            st.session_state.generation_step    = 0
            # Reset all section flags for a fresh run
            for k in st.session_state.sections_generated:
                st.session_state.sections_generated[k] = False
            st.rerun()


    # ══════════════════════════════════════════════════════════════════════════
    # FINAL DOWNLOAD
    # ══════════════════════════════════════════════════════════════════════════
    if st.session_state.generation_step >= 7:
        st.markdown('<div class="nexus-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
    <div style="text-align:center;padding:28px 0 16px">
      <div style="font-size:32px;margin-bottom:12px">✦</div>
      <h2 style="font-family:'Playfair Display',serif;font-size:24px;color:var(--platinum);margin:0 0 8px">
        Document Generation <span style="color:var(--gold)">Complete</span>
      </h2>
      <p style="font-size:13px;color:var(--mist);margin:0">Your dissertation report is ready for download.</p>
    </div>
    """, unsafe_allow_html=True)

        # ── Section definitions: (filename, heading label) ──
        sections = [
            ("abstract.txt",        "ABSTRACT"),
            ("introduction.txt",    "1. INTRODUCTION"),
            ("lr.txt",              "2. LITERATURE REVIEW"),
            ("methodology.txt",     "3. METHODOLOGY"),
            ("implementation.txt",  "4. IMPLEMENTATION"),
            ("results.txt",         "5. RESULTS AND CONCLUSION"),
            ("conclusion.txt",      "6. CONCLUSION"),
        ]

        doc_title = title.strip().upper() if title.strip() else "DISSERTATION REPORT"
        separator = "=" * 70

        combined_content = f"{separator}\n{doc_title}\n{separator}\n\n"

        for fn, heading in sections:
            fp = os.path.join(directory, fn)
            try:
                section_text = read_file_auto_encoding(fp).strip()
                if section_text:
                    combined_content += f"{separator}\n{heading}\n{separator}\n\n{section_text}\n\n\n"
            except FileNotFoundError:
                if fn != "lr.txt":
                    st.warning(f"{fn} not found — skipping.")

        # ── Collect all references from every source ──
        all_ref_lines = []

        def _parse_refs(raw_text):
            """Split a block of references into individual entries."""
            raw_text = raw_text.strip()
            if not raw_text:
                return []
            # Try double-newline split first (blank line separated)
            entries = [e.strip() for e in re.split(r'\n{2,}', raw_text) if e.strip()]
            # If that gives only 1 entry, split on single newlines where next
            # line starts with a capital letter (Harvard style: Surname, I. ...)
            if len(entries) <= 1:
                entries = [e.strip() for e in re.split(r'\n(?=[A-Z])', raw_text) if e.strip()]
            return entries

        # Source 1: references extracted from uploaded LR file
        lr_refs_fp = os.path.join(directory, "references_lr.txt")
        try:
            all_ref_lines += _parse_refs(read_file_auto_encoding(lr_refs_fp))
        except FileNotFoundError:
            pass

        # Source 2: references from JSON data (used by citations step)
        try:
            json_refs = st.session_state.json_data.get("references", [])
            if isinstance(json_refs, list):
                all_ref_lines += [r.strip() for r in json_refs if isinstance(r, str) and r.strip()]
            elif isinstance(json_refs, str) and json_refs.strip():
                all_ref_lines += _parse_refs(json_refs)
        except Exception:
            pass

        # Source 3: any references files the generation pipeline writes
        for ref_file in ["references.txt", "keywords.txt", "citations.txt"]:
            try:
                all_ref_lines += _parse_refs(read_file_auto_encoding(os.path.join(directory, ref_file)))
            except FileNotFoundError:
                pass

        # Deduplicate by first 80 chars lowercased, then sort A-Z by surname
        seen_keys = set()
        unique_refs = []
        for r in all_ref_lines:
            key = r.lower()[:80].strip()
            if key and key not in seen_keys:
                seen_keys.add(key)
                unique_refs.append(r)

        unique_refs.sort(key=lambda x: re.sub(r'^[\d\.\s\[\]]+', '', x).lower())

        if unique_refs:
            refs_block = "\n\n".join(unique_refs)
            combined_content += f"{separator}\nREFERENCES\n{separator}\n\n{refs_block}\n"
        else:
            combined_content += f"{separator}\nREFERENCES\n{separator}\n\n[No references found]\n"

        safe_title = "".join(c for c in title if c.isalnum() or c in [' ', '_', '-']).strip().replace(" ", "_")
        dl_name = f"dissertation_({safe_title}).txt"

        st.download_button(
            label="⬇  Download Final Dissertation Document",
            data=combined_content.encode("utf-8"),
            file_name=dl_name,
            mime="text/plain"
        )

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
        if st.button("↺  Start New Document"):
            st.session_state.generation_step = 0
            st.session_state.generation_running = False
            st.session_state.sections_generated = {k: False for k in st.session_state.sections_generated}
            st.session_state.json_loaded = False
            st.session_state.json_data = {}
            st.session_state.lr_loaded = False
            st.session_state.lr_filename = ""
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close content-wrap