import unittest

from emotion_detector import detect_emotion


class TestEmotionDetector(unittest.TestCase):

    def test_happy_sentence(self):
        result = detect_emotion("I am happy and excited")
        self.assertEqual(result["emotion"], "Happy")

    def test_sad_sentence(self):
        result = detect_emotion("I feel lonely and disappointed")
        self.assertEqual(result["emotion"], "Sad")

    def test_angry_sentence(self):
        result = detect_emotion("I am angry and frustrated")
        self.assertEqual(result["emotion"], "Angry")

    def test_fear_sentence(self):
        result = detect_emotion("I am terrified and anxious")
        self.assertEqual(result["emotion"], "Fear")

    def test_love_sentence(self):
        result = detect_emotion("I adore and cherish my family")
        self.assertEqual(result["emotion"], "Love")

    def test_surprise_sentence(self):
        result = detect_emotion("Wow, this is astonishing and unexpected")
        self.assertEqual(result["emotion"], "Surprise")

    def test_neutral_sentence(self):
        result = detect_emotion("The table is near the window")
        self.assertEqual(result["emotion"], "Neutral")

    def test_negated_keyword(self):
        result = detect_emotion("I am not happy")
        self.assertEqual(result["emotion"], "Neutral")
        self.assertIn("happy", result["negated_keywords"])

    def test_contrast(self):
        result = detect_emotion("I am not happy but excited")
        self.assertEqual(result["emotion"], "Happy")

    def test_inflections_and_variations(self):
        # Tests previously failing morphological forms
        res_loving = detect_emotion("I am loving this so much")
        self.assertEqual(res_loving["emotion"], "Love")

        res_crying = detect_emotion("I was crying all night")
        self.assertEqual(res_crying["emotion"], "Sad")

        res_depressed = detect_emotion("I feel depressed and hopeless")
        self.assertEqual(res_depressed["emotion"], "Sad")

    def test_emoji_detection(self):
        res_heart = detect_emotion("I appreciate this ❤️")
        self.assertEqual(res_heart["emotion"], "Love")

        res_happy = detect_emotion("Good morning 😊")
        self.assertEqual(res_happy["emotion"], "Happy")

        res_sad = detect_emotion("Feeling heartbroken 😭")
        self.assertEqual(res_sad["emotion"], "Sad")

    def test_negated_emoji(self):
        result = detect_emotion("I am not 😭")
        self.assertEqual(result["emotion"], "Neutral")
        self.assertIn("😭", result["negated_keywords"])

    def test_mixed_ambiguous_tie(self):
        result = detect_emotion("I am happy and angry")
        self.assertEqual(result["emotion"], "Mixed / Ambiguous")

    def test_empty_and_whitespace(self):
        self.assertEqual(detect_emotion("")["emotion"], "Neutral")
        self.assertEqual(detect_emotion("   ")["emotion"], "Neutral")


if __name__ == "__main__":
    unittest.main()
