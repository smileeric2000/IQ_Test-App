# 🌟 Streamlit IQ Test App

Welcome to the **Streamlit IQ Test App**, a modern, interactive web application designed to measure five key aspects of intelligence:

- **Analytical** 🧠  
- **Social** 🤝  
- **Moral** ⚖️  
- **Symbolic** 🔣  
- **Creative-Technical** 🛠️  

The app is built using **Streamlit** for a responsive and user-friendly experience, and **ReportLab** to generate downloadable PDF certificates.

---

## 🚀 Major Functionality

1. **User Registration**
   - Users can enter their **name, age, gender, and email**.
   - Information is saved in **Streamlit session state**, ensuring progress is not lost if the page is refreshed.

2. **IQ Test**
   - Presents **one question at a time** with dynamic typing effects.
   - Supports **different question types**:
     - Likert scale (`Strongly Disagree → Strongly Agree`)
     - Single numeric choice
     - Multi-part numeric choice
   - Tracks user progress with **Back** and **Next** navigation buttons.
   - Stores answers safely in session state.

3. **Score Calculation**
   - Aggregates answers by category to calculate **total scores**.
   - Multi-part numeric answers are summed, Likert scores are converted to numeric values.

4. **Results & Feedback**
   - Displays **category-wise scores** using Streamlit metrics.
   - Highlights the **strongest and weakest intelligence types**.
   - Suggests **career paths** based on results.
   - Generates a **personalized certificate (PDF)** that users can download.

5. **Interactive Visuals**
   - Includes a simple **blossom animation** and **balloons** for celebration.
   - Typing animation for question text for a fun, dynamic experience.

---

## 🎨 Areas for Future Scaling

As this app grows, here are some areas I would love to enhance:

- **Dynamic Question Bank**
  - Pull questions from a **database or JSON file** to allow easy updates.
  - Support for **image-based or interactive questions**.

- **Advanced Scoring**
  - Introduce **weighting** for questions.
  - Normalize scores to a **percentile system**.

- **User Profiles**
  - Allow returning users to **track progress over time**.
  - Option to **store results in a database** for analytics.

- **Responsive UI Enhancements**
  - Add **themes**, **progress bars**, and **mobile-friendly layouts**.
  - Improve animations and visual feedback.

- **Social Features**
  - Share results on social media.
  - Compare with **average scores** from other users.

- **Security & Validation**
  - Email validation and optional login for a **secure experience**.

---

## 🛠️ Tech Stack

- **Frontend & App**: [Streamlit](https://streamlit.io/)  
- **PDF Generation**: [ReportLab](https://www.reportlab.com/)  
- **Python Libraries**: `time`, `io`, `reportlab`, `streamlit`  

---

## 📁 File Structure

