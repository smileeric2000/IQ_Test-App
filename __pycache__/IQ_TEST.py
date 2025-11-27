import streamlit as st
from utils import (
    QUESTIONS,
    init_session_state,
    typing_print_lines,
    calculate_scores,
    generate_certificate_bytes,
)
import io

st.set_page_config(page_title="Streamlit IQ Test App", layout="centered")

# Initialize session state
init_session_state()

PAGES = ["Introduction", "Register", "Test", "Results"]
page = st.sidebar.selectbox("Navigate", PAGES)

# --- Page 1: Introduction ---
if page == "Introduction":
    st.title("Streamlit IQ Test App")
    st.markdown(
        "This app measures five aspects of intelligence: **Analytical**, **Social**, **Moral**, **Symbolic**, and **Creative-Technical**.\n\n"
        "You'll register your details, answer a short set of questions (one per page) and receive a friendly results summary and downloadable certificate."
    )
    st.markdown("---")
    st.write("**How it works**")
    st.write(
        "You will see one question per page. Use the `Back` and `Next` buttons to move. Your progress is saved in the session so you can come back to where you left off."
    )
    st.write(
        "The test includes questions that target: Analytical, Social, Moral, Symbolic, and Creative-Technical intelligence."
    )
    st.info("When you're ready, go to 'Register' in the sidebar to begin.")

#Page 2: Registration ---
elif page == "Register":
    st.header("User Registration")
    with st.form("reg_form"):
        name = st.text_input("Full name", value=st.session_state.user.get("name", ""))
        age = st.number_input("Age", min_value=6, max_value=120, value=st.session_state.user.get("age", 18))
        gender = st.selectbox("Gender", ["Prefer not to say", "Female", "Male", "Non-binary", "Other"], index=0)
        email = st.text_input("Email", value=st.session_state.user.get("email", ""))
        submitted = st.form_submit_button("Save")
        if submitted:
            st.session_state.user.update({"name": name, "age": int(age), "gender": gender, "email": email})
            st.success("Saved to session — proceed to the Test page when ready.")

    if st.session_state.user.get("name"):
        st.markdown("**Saved user:**")
        st.write(st.session_state.user)

#Page 3: Test ---
elif page == "Test":
    st.header("IQ Test — One question at a time")
    q_index = st.session_state.progress.get("current_q", 0)
    total_q = len(QUESTIONS)

    # Allow quick navigation bar for progress
    st.write(f"Question {q_index+1} of {total_q}")
    q = QUESTIONS[q_index]

    # Typing effect for question text
    placeholder = st.empty()
    if not st.session_state.get("typed_" + str(q_index), False):
        with placeholder.container():
            typing_print_lines(q["text"].split("\n"))
        st.session_state["typed_" + str(q_index)] = True
    else:
        placeholder.write(q["text"])

    #Show options (Likert style)
    options = q.get("options", ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"])
    answer_key = f"q_{q_index}"
    prev = st.session_state.answers.get(answer_key, 3)
    ans = st.radio("Your answer:", options, index=prev-1, key=answer_key+"_radio")

    #Map selection to score 1-5
    score = options.index(ans) + 1

    #Save the score into session
    st.session_state.answers[answer_key] = score

    cols = st.columns([1, 1, 1])
    if cols[0].button("Back"):
        if q_index > 0:
            st.session_state.progress["current_q"] = q_index - 1
            st.rerun()
    if cols[2].button("Next"):
        if q_index < total_q - 1:
            st.session_state.progress["current_q"] = q_index + 1
            st.rerun()
        else:
            #Final submission
            st.session_state.submitted = True
            st.session_state.scores = calculate_scores(st.session_state.answers, QUESTIONS)
            st.success("Test submitted — opening results...")
            st.rerun()

#Page 4: Results ---
elif page == "Results":
    if not st.session_state.get("submitted", False):
        st.info("You haven't submitted the test yet. Go to 'Test' and finish to see results.")
    else:
        st.header("Results")
        # Simple blossom animation using HTML/CSS + balloons
        st.markdown("""
        <div style='text-align:center;'>
        <div class='flower'></div>
        </div>
        <style>
        .flower{margin:20px auto;width:120px;height:120px;border-radius:50%;position:relative;}
        .flower:before,.flower:after{content:'';position:absolute;width:60px;height:60px;border-radius:50%;background: radial-gradient(circle at 30% 30%, #ff9a9e, #fad0c4);opacity:0.9;animation:blossom 1.8s ease-in-out infinite;}
        .flower:before{left:0;transform-origin:60px 30px}
        .flower:after{right:0;transform-origin:0px 30px}
        @keyframes blossom{0%{transform:scale(0.2) rotate(0)}50%{transform:scale(1.02) rotate(10deg)}100%{transform:scale(0.95) rotate(0deg)}}
        </style>
        """, unsafe_allow_html=True)
        st.balloons()

        # Show computed scores
        scores = st.session_state.scores
        st.subheader(f"Hi {st.session_state.user.get('name', 'Tester')} — here are your scores")
        for cat, val in scores.items():
            st.metric(label=cat, value=f"{val:.1f}")

        # Short personalized analysis
        strongest = max(scores, key=scores.get)
        weakest = min(scores, key=scores.get)
        st.markdown("**Summary**")
        st.write(
            f"Nice work, {st.session_state.user.get('name', 'friend')}! You show strong {strongest} intelligence — that's a natural strength. "
            f"You may want to focus on improving {weakest} through targeted activities. Overall, keep exploring and building on your strengths."
        )

        # Suggest careers (basic rule-based suggestions)
        st.markdown("**Suggested career paths**")
        suggestions = {
            "Analytical": ["Data Scientist", "Engineer", "Research Analyst"],
            "Social": ["Counselor", "Teacher", "PR Specialist"],
            "Moral": ["Social Worker", "Ethics Officer", "NGO Coordinator"],
            "Symbolic": ["Designer", "Mathematician", "Cryptographer"],
            "Creative-Technical": ["Product Designer", "Inventor", "Creative Technologist"],
        }
        st.write(", ".join(suggestions.get(strongest, [])))

        # Download certificate
        st.markdown("---")
        st.write("Download your certificate below")
        pdf_bytes = generate_certificate_bytes(
            name=st.session_state.user.get("name", "Tester"), scores=scores
        )
        st.download_button(
            label="Download Certificate (PDF)",
            data=pdf_bytes,
            file_name=f"IQ_Certificate_{st.session_state.user.get('name','Tester').replace(' ','_')}.pdf",
            mime="application/pdf",
        )