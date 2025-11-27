import time
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from io import BytesIO

#Define the question bank. Each question has: text, category
QUESTIONS = [
    {"text": "(Analytical) If a pattern is 2, 4, 8, 16, what comes next? 36 ?", "category": "Analytical"},
    {"text": "(Analytical) I can solve logic puzzles quickly.", "category": "Analytical"},
    {"text": "(Analytical) I serie has numbers 3,8 , 18, 35, 61, __, __. find the missing two.", "category": "Analytical" },


    {"text": "(Social) I feel comfortable understanding how others feel.", "category": "Social"},
    {"text": "(Social) I often help friends navigate social problems.", "category": "Social"},
    {"text": "(Social) I prefer working in teams rather than alone.", "category": "Social"},

    {"text": "(Moral) I consider ethical consequences before making decisions.", "category": "Moral"},
    {"text": "(Moral) I stand up for what I believe is right.", "category": "Moral"},
    {"text": "(Moral) I often think about fairness and justice.", "category": "Moral"},

    {"text": "(Symbolic) I enjoy puzzles that use symbols and codes.", "category": "Symbolic"},
    {"text": "(Symbolic) I can interpret maps, charts and abstract diagrams easily.", "category": "Symbolic"},
    {"text": "(Symbolic) I like to work with languages or symbolic systems.", "category": "Symbolic"},

    {"text": "(Creative-Technical) I enjoy making things and fixing mechanical problems.", "category": "Creative-Technical"},
    {"text": "(Creative-Technical) I come up with novel solutions to technical problems.", "category": "Creative-Technical"},
    {"text": "(Creative-Technical) I like designing or building prototypes.", "category": "Creative-Technical"},
]

#default options (Likert)
DEFAULT_OPTIONS = ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]

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
def calculate_scores(answers: dict, questions: list):
    #Build mapping from q index to category
    cat_scores = {}
    cat_counts = {}
    for idx, q in enumerate(questions):
        key = f"q_{idx}"
        score = answers.get(key, 3)  #default neutral if missing
        cat = q["category"]
        cat_scores[cat] = cat_scores.get(cat, 0) + score
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    #average per category
    avg_scores = {cat: (cat_scores[cat] / cat_counts[cat]) for cat in cat_scores}
    return avg_scores

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
