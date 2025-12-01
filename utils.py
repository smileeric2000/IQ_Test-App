import time
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from io import BytesIO

#Define the question bank. Each question has: text, category
QUESTIONS = [
    #Analytical (multiple-choice numeric)
    {
        "text": " If a pattern is 2, 4, 8, 16, what comes next?",
        "category": "Analytical",
        "type": "numeric_choice",
        "options": [32, 34, 36, 40]   # number-only options
    },

    {"text": " I can solve logic puzzles quickly.",
     "category": "Analytical", "type": "likert"},

    {
        "text": " The series has numbers 3, 8, 18, 35, 61, __, __. Find the missing two.",
        "category": "Analytical",
        "type": "numeric_choice_multi",
        "options_1": [92, 95, 101, 105],   #first missing number
        "options_2": [150, 161, 175, 180]  #second missing number
    },

    #Social
    {"text": " I feel comfortable understanding how others feel.", "category": "Social", "type": "likert"},
    {"text": " I often help friends navigate social problems.", "category": "Social", "type": "likert"},
    {"text": " I prefer working in teams rather than alone.", "category": "Social", "type": "likert"},

    #Moral
    {"text": " I consider ethical consequences before making decisions.", "category": "Moral", "type": "likert"},
    {"text": " I stand up for what I believe is right.", "category": "Moral", "type": "likert"},
    {"text": " I often think about fairness and justice.", "category": "Moral", "type": "likert"},

    #Symbolic
    {"text": " I enjoy puzzles that use symbols and codes.", "category": "Symbolic", "type": "likert"},
    {"text": " I can interpret maps, charts and abstract diagrams easily.", "category": "Symbolic", "type": "likert"},
    {"text": " I like to work with languages or symbolic systems.", "category": "Symbolic", "type": "likert"},

    #Creative-Technical
    {"text": " I enjoy making things and fixing mechanical problems.", "category": "Creative-Technical", "type": "likert"},
    {"text": " I come up with novel solutions to technical problems.", "category": "Creative-Technical", "type": "likert"},
    {"text": " I like designing or building prototypes.", "category": "Creative-Technical", "type": "likert"},
]

DEFAULT_OPTIONS = [
    "Strongly disagree",
    "Disagree",
    "Neutral",
    "Agree",
    "Strongly agree"
]

#Session initialization
def init_session_state():
    if "user" not in st.session_state:
        st.session_state.user = {}
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "progress" not in st.session_state:
        st.session_state.progress = {"current_q": 0}
    if "scores" not in st.session_state:
        st.session_state.scores = {}
    if "submitted" not in st.session_state:
        st.session_state.submitted = False

#Typing/printing effect: prints line by line with small delay
def typing_print_lines(lines, delay=0.03):
    """
    lines: list of strings
    delay: seconds per character (keeps small to avoid long waits)
    """
    for line in lines:
        placeholder = st.empty()
        txt = ""
        for ch in line:
            txt += ch
            placeholder.markdown(txt + "\n")
            time.sleep(delay)
        #small pause at the end of each line
        time.sleep(0.15)

#Score calculation: aggregate answers by category
def calculate_scores(answers, questions):
    """
    answers: dict { 'q_0': answer_value, 'q_1': answer_value, ... }
    questions: list of question dicts
    Returns: dict {category: total_score}
    """
    cat_scores = {}

    for i, q in enumerate(questions):
        q_key = f"q_{i}"
        score = answers.get(q_key, 0)

        # Convert types safely
        if isinstance(score, tuple):
            # Multi-part numeric: sum of correct parts
            score = sum(int(s) for s in score if str(s).isdigit())
        elif isinstance(score, str):
            # Likert or numeric-choice: try convert to int
            try:
                score = int(score)
            except ValueError:
                score = 0
        elif score is None:
            score = 0

        cat = q["category"]
        cat_scores[cat] = cat_scores.get(cat, 0) + score

    return cat_scores

#Generate a PDF certificate and return bytes(using reportlab)
#def generate_certificate_bytes(name: str, scores: dict):
#buffer = BytesIO()
def generate_certificate_bytes(name: str, scores: dict):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from io import BytesIO

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    #Certificate content
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 1.5 * 72, "Certificate of Assessment")
    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 1.9 * 72, "Awarded to")
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 2.4 * 72, name)
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 2.8 * 72, "Tested with Streamlit IQ Test App")

    #Draw scores
    y = height - 3.4 * 72
    for cat, val in scores.items():
        c.drawString(72, y, f"{cat}: {val:.2f} / 5")
        y -= 0.3 * 72

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()  #Make sure to return bytes