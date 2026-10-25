# 🎭 Emotion Detection NLP (Rule-Based & Explainable)

A fast, transparent, and explainable rule-based Natural Language Processing (NLP) system and interactive Streamlit web dashboard for detecting emotions in textual input and emojis.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.40%2B-red.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 📖 Overview

Unlike "black-box" machine learning models, this system provides **100% deterministic, explainable emotion classification**. It pinpoints exactly which words or emojis triggered an emotion, which keywords were suppressed due to preceding negation words, and how contrast words (such as *"but"* or *"however"*) shift the emotional context.

---

## ✨ Features

- **6 Primary Emotion Categories:** `Happy`, `Sad`, `Angry`, `Fear`, `Love`, `Surprise` (along with `Neutral` and `Mixed / Ambiguous`).
- **Rich Emotion Lexicon:** Curated base words, common inflections (`loving`, `crying`, `depressed`, `terrifying`), and emotional synonyms.
- **Emoji Parsing:** Recognizes Unicode emojis (`😊`, `❤️`, `😭`, `😡`, `😱`, `🎉`, `💔`, etc.) directly in sequence.
- **Context-Aware Negation Handling:** 3-token lookback window detects negative qualifiers (`not`, `never`, `isn't`, `didn't`, `can't`, `hardly`, etc.) and suppresses false positive matches.
- **Contrast Word Resets:** Conjunctions like `but`, `however`, and `although` reset the negation window so post-contrast emotions are properly registered (e.g. *"I am not happy but excited"* ➔ `Happy`).
- **Interactive Streamlit UI:** Includes 1-click test examples, real-time bar charts of score distributions, and linguistic breakdown metrics.
- **Automated Test Suite:** Comprehensive unit tests covering inflections, emojis, edge cases, and ties using Python's standard `unittest`.

---

## 🧠 How the Algorithm Works

```
                     Input Text
                         │
                         ▼
           ┌───────────────────────────┐
           │ Tokenization & Lowercase  │  (Words + Emojis extracted)
           └─────────────┬─────────────┘
                         │
                         ▼
        ┌─────────────────────────────────┐
        │     Token-by-Token Matching     │
        └────────────────┬────────────────┘
                         │
               Keyword / Emoji Found?
              ┌──────────┴──────────┐
             YES                    NO
              │                      │
              ▼                      ▼
  ┌───────────────────────┐     Ignore Token
  │   Negation Check      │
  │ (3-token lookback +   │
  │  contrast word reset) │
  └───────────┬───────────┘
              │
        Is Negated?
       ┌──────┴──────┐
      YES            NO
       │              │
       ▼              ▼
  Add to Negated   Increment Emotion
    Keywords         Counter Score
       │              │
       └──────┬───────┘
              │
              ▼
   ┌───────────────────────┐
   │ Final Decision Logic  │
   │ - Max Score Winner    │
   │ - Tie ➔ Mixed         │
   │ - 0 Matches ➔ Neutral │
   └───────────────────────┘
```

---

## 📂 Project Structure

```text
emotion-detection-nlp/
├── app.py                     # Interactive Streamlit web application
├── emotion_detector.py        # Core NLP logic, lexicon, negation & contrast handling
├── test_emotion_detector.py   # Unit test suite (14 test cases)
├── requirements.txt           # Python dependencies
├── .gitignore                 # Files excluded from version control
└── README.md                  # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
Ensure you have Python 3.10 or higher installed.

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/your-username/emotion-detection-nlp.git
cd emotion-detection-nlp

# (Optional) Create and activate a virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch the Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 4. Run the Unit Tests
```bash
python test_emotion_detector.py
```
Or run with verbose output:
```bash
python -m unittest -v test_emotion_detector.py
```

---

## 🧪 Example Test Scenarios

| Input Sentence | Predicted Emotion | Matched Keywords / Emojis | Negated Keywords |
| :--- | :---: | :--- | :--- |
| `"I am happy and excited today! 😊"` | **Happy** | `happy`, `excited`, `😊` | *None* |
| `"I was crying all night and feel heartbroken 😭"` | **Sad** | `crying`, `heartbroken`, `😭` | *None* |
| `"I am not happy but feeling excited! 🥳"` | **Happy** | `excited`, `🥳` | `happy` |
| `"I am furious and hate this delay! 😡"` | **Angry** | `furious`, `hate`, `😡` | *None* |
| `"I love and adore my friends ❤️"` | **Love** | `love`, `adore`, `❤️` | *None* |
| `"I am terrified and nervous about the dark 😨"` | **Fear** | `terrified`, `nervous`, `😨` | *None* |
| `"I am not sad 😭"` | **Neutral** | *None* | `sad`, `😭` |
| `"The book is on the desk near the window."` | **Neutral** | *None* | *None* |
| `"I am happy and angry"` | **Mixed / Ambiguous** | `happy`, `angry` | *None* |

---

## 🔮 Future Roadmap

- **Level 2 (Machine Learning):** Train a TF-IDF + Logistic Regression / Naive Bayes baseline on the GoEmotions dataset.
- **Level 3 (Transformer Models):** Integrate Hugging Face `transformers` (e.g. `distilbert-base-uncased-emotion`) with a toggle switch to compare rule-based vs. deep learning inferences side-by-side.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
