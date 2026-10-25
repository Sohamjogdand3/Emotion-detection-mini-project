import streamlit as st
import pandas as pd

from emotion_detector import detect_emotion

st.set_page_config(
    page_title="Emotion Detection NLP",
    page_icon="🎭",
    layout="centered"
)

EMOTION_ICONS = {
    "Happy": "😊",
    "Sad": "😢",
    "Angry": "😡",
    "Fear": "😨",
    "Love": "❤️",
    "Surprise": "😲",
    "Neutral": "😐",
    "Mixed / Ambiguous": "🎭"
}

st.title("🎭 Emotion Detection NLP")

st.write(
    "Enter a sentence with words or emojis to detect emotions "
    "using an explainable rule-based NLP system with negation handling."
)


# Initialize session state keys
if "text_input_area" not in st.session_state:
    st.session_state["text_input_area"] = "I am happy and excited today! 😊"
    st.session_state["should_detect"] = True

# Quick Example Buttons
st.subheader("💡 Try Quick Examples")
st.caption("Click any example to instantly load it and run emotion detection:")

examples = [
    "I am happy and excited today! 😊",
    "I was crying all night and feel heartbroken 😭",
    "I am not happy but feeling excited! 🥳",
    "I am furious and hate this delay! 😡",
    "I love and adore my friends ❤️",
    "Wow, this is shocking and unexpected! 😲",
    "I am terrified and nervous about the dark 😨",
    "The book is on the desk near the window."
]

cols = st.columns(2)
for idx, example in enumerate(examples):
    col = cols[idx % 2]
    if col.button(example, key=f"example_{idx}", use_container_width=True):
        st.session_state["text_input_area"] = example
        st.session_state["should_detect"] = True
        st.rerun()

user_text = st.text_area(
    "Enter your sentence or paste text:",
    key="text_input_area",
    height=120
)

detect_clicked = st.button("Detect Emotion", type="primary", use_container_width=True)

# Trigger detection if user clicks the detect button or if an example was selected
if detect_clicked or st.session_state.get("should_detect", False):
    st.session_state["should_detect"] = False
    current_input = st.session_state.get("text_input_area", "").strip()
    if not current_input:
        st.warning("Please enter a sentence first.")
        st.session_state["latest_result"] = None
    else:
        st.session_state["latest_result"] = detect_emotion(current_input)

# Display detection result if available
if st.session_state.get("latest_result"):
    result = st.session_state["latest_result"]
    predicted = result["emotion"]
    icon = EMOTION_ICONS.get(predicted, "🎭")

    st.divider()
    st.subheader("Detection Result")

    col_res1, col_res2, col_res3 = st.columns(3)
    col_res1.metric("Predicted Emotion", f"{icon} {predicted}")
    col_res2.metric("Matched Keywords", result["total_matches"])
    col_res3.metric("Negated Words", len(result["negated_keywords"]))

    if predicted in ["Neutral", "Mixed / Ambiguous"]:
        st.info(f"**Outcome:** {icon} {predicted}")
    else:
        st.success(f"**Dominant Emotion:** {icon} {predicted}")

    # Linguistic breakdown
    st.write("### 🔍 Linguistic Breakdown")

    if result["matched_keywords"]:
        for emotion, words in result["matched_keywords"].items():
            e_icon = EMOTION_ICONS.get(emotion, "")
            st.markdown(f"- **{e_icon} {emotion}:** `{'`, `'.join(words)}`")
    else:
        st.caption("No positive emotion keywords or emojis matched.")

    if result["negated_keywords"]:
        st.markdown(f"- **🚫 Negated (Suppressed):** `{'`, `'.join(result['negated_keywords'])}`")

    # Bar chart
    st.write("### 📊 Emotion Scores Distribution")
    all_emotions = ["Happy", "Sad", "Angry", "Fear", "Love", "Surprise"]
    score_data = {
        emotion: result["scores"].get(emotion, 0)
        for emotion in all_emotions
    }

    score_df = pd.DataFrame(
        list(score_data.items()),
        columns=["Emotion", "Score"]
    )
    st.bar_chart(score_df.set_index("Emotion"))

    st.caption(
        "ℹ️ Scores represent keyword and emoji counts matched in the text, "
        "accounting for negation windows and contrast conjunctions."
    )
