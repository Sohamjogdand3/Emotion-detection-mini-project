import re
from collections import Counter, defaultdict

# Comprehensive emotion keyword and emoji lexicons for 6 primary emotions.
EMOTION_KEYWORDS = {
    "Happy": {
        # Base words & synonyms
        "happy", "happier", "happiest", "happiness", "happily",
        "joy", "joyful", "joyfully", "joyous", "enjoy", "enjoying", "enjoyed", "enjoyable",
        "excited", "exciting", "excitement", "glad", "gladly", "gladness",
        "delighted", "delight", "delightful", "delightfully",
        "cheerful", "cheer", "cheering", "cheered", "cheery",
        "awesome", "great", "ecstatic", "thrilled", "thrilling", "bliss", "blissful",
        "content", "contented", "contentment", "pleased", "pleasant",
        "celebrate", "celebrating", "celebration", "triumph", "triumphant",
        "smiling", "smile", "smiles", "smiled", "laugh", "laughing", "laughed", "laughter",
        "wonderful", "fantastic", "fabulous", "amazing", "amazingly", "fun",
        "euphoric", "euphoria", "radiant", "grateful", "gratitude",
        # Emojis
        "😊", "😀", "😃", "😄", "😁", "😆", "🥳", "🎉", "✨", "🙌", "😎", "😋", "🤩"
    },
    "Sad": {
        # Base words & synonyms
        "sad", "sadder", "saddest", "sadly", "sadness",
        "lonely", "loneliness", "alone", "isolated", "isolation", "abandoned",
        "unhappy", "unhappiness", "unhappily",
        "upset", "upsetting",
        "disappointed", "disappointing", "disappointment",
        "miserable", "misery",
        "heartbroken", "heartbreak", "brokenhearted",
        "depressed", "depressing", "depression",
        "sorrow", "sorrowful", "despair", "hopeless", "hopelessness",
        "crying", "cry", "cries", "cried", "wept", "weeping", "tear", "tears", "tearful",
        "grieving", "grief", "mourn", "mourning", "mournful",
        "hurt", "hurting", "pain", "painful", "agony", "gloomy", "gloom", "glum",
        "melancholy", "downhearted", "regret", "regretful", "gloomy",
        # Emojis
        "😢", "😭", "😞", "😔", "🥺", "💔", "😿", "😩", "😫", "🌧️", "🥀"
    },
    "Angry": {
        # Base words & synonyms
        "angry", "angrier", "angriest", "angrily", "anger",
        "furious", "furiously", "fury",
        "annoyed", "annoying", "annoyance",
        "irritated", "irritating", "irritation",
        "hate", "hating", "hated", "hatred", "hateful",
        "mad", "madness",
        "frustrated", "frustrating", "frustration",
        "outraged", "outrage", "outrageous",
        "rage", "raging", "bitter", "bitterness",
        "resentful", "resentment", "offended", "offensive",
        "hostile", "hostility", "disgusted", "disgust", "wrath", "fuming",
        # Emojis
        "😡", "😠", "🤬", "💢", "👿", "😤", "🖕"
    },
    "Fear": {
        # Base words & synonyms
        "scared", "scary", "scarier", "scariest",
        "afraid",
        "terrified", "terrifying", "terrifyingly", "terrify", "terror",
        "nervous", "nervously", "nervousness",
        "anxious", "anxiously", "anxiety",
        "frightened", "frightening", "fright",
        "worried", "worrying", "worry", "worries",
        "panicked", "panic", "panicking",
        "fearful", "fear", "fearing", "dread", "dreading", "dreadful",
        "alarmed", "alarming", "intimidated", "horror", "horrified", "spooked",
        # Emojis
        "😨", "😱", "😰", "😬", "🫣", "💀"
    },
    "Love": {
        # Base words & synonyms
        "love", "loved", "loving", "lovingly", "lover", "loves", "lovely",
        "adore", "adored", "adoring", "adoration",
        "affection", "affectionate", "affectionately",
        "caring", "cared", "care", "cares",
        "cherish", "cherished", "cherishing",
        "fond", "fondness", "devoted", "devotion",
        "passionate", "passion", "infatuated", "infatuation",
        "romantic", "romance", "cuddle", "hugging", "hugs", "hug",
        "sweetheart", "darling",
        # Emojis
        "❤️", "❤", "💖", "💕", "😍", "🥰", "😘", "💗", "💓", "💞", "💌"
    },
    "Surprise": {
        # Base words & synonyms
        "shocked", "shocking", "shock",
        "amazed", "amazing", "amazement",
        "astonished", "astonishing", "astonishment",
        "unexpected", "unexpectedly",
        "wow", "whoa", "omg",
        "surprised", "surprising", "surprise",
        "stunned", "stunning", "startled", "startling",
        "speechless", "bewildered", "flabbergasted", "mindblowing",
        # Emojis
        "😲", "😮", "🤯", "😯", "😳", "🙀"
    }
}

NEGATION_WORDS = {
    "not", "never", "no", "isn't", "wasn't",
    "weren't", "don't", "doesn't", "didn't",
    "can't", "cannot", "won't", "hardly", "barely",
    "scarcely", "neither", "nor"
}

CONTRAST_WORDS = {"but", "however", "although", "yet", "still"}


def preprocess_text(text):
    """Convert text to lowercase and extract words and emojis."""
    text = text.lower()
    # Match words (including contractions) and unicode emoji characters
    raw_tokens = re.findall(r"\b[\w']+\b|[^\x00-\x7F](?:\ufe0f)?", text)
    return [t.strip() for t in raw_tokens if t.strip() and t.strip() != "\ufe0f"]


def is_negated(tokens, index):
    """Check whether a keyword is preceded by negation within a 3-token window."""
    previous_words = tokens[max(0, index - 3):index]

    # Negation does not carry across a contrast word.
    last_contrast = -1
    for i, word in enumerate(previous_words):
        if word in CONTRAST_WORDS:
            last_contrast = i

    relevant_words = previous_words[last_contrast + 1:]

    return any(
        word in NEGATION_WORDS
        for word in relevant_words
    )


def detect_emotion(text):
    """Detect emotion using keyword and emoji matching, negation, and scoring."""
    tokens = preprocess_text(text)

    scores = Counter()
    matched_keywords = defaultdict(list)
    negated_keywords = []

    for index, word in enumerate(tokens):
        for emotion, keywords in EMOTION_KEYWORDS.items():
            if word not in keywords:
                continue

            if is_negated(tokens, index):
                negated_keywords.append(word)
            else:
                scores[emotion] += 1
                matched_keywords[emotion].append(word)

    if not scores:
        predicted_emotion = "Neutral"
    else:
        highest_score = max(scores.values())

        # A tie means the rule-based system cannot select one emotion unambiguously.
        winners = [
            emotion
            for emotion, score in scores.items()
            if score == highest_score
        ]

        predicted_emotion = (
            winners[0] if len(winners) == 1
            else "Mixed / Ambiguous"
        )

    return {
        "emotion": predicted_emotion,
        "scores": dict(scores),
        "matched_keywords": dict(matched_keywords),
        "negated_keywords": negated_keywords,
        "total_matches": sum(scores.values())
    }
