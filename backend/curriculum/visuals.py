"""Illustrative sample cues; qualified educator review is still required."""


def visual_cues(reference):
    if reference == "My name is Alex":
        return {
            "target": "/m/ in “My”",
            "syllables": [
                {"text": "My", "stress": False},
                {"text": "name", "stress": False},
                {"text": "is", "stress": False},
                {"text": "Al", "stress": True},
                {"text": "ex", "stress": False},
            ],
            "tip": "For /m/, gently close your lips and let your voice hum through your nose. Do not force the sound.",
            "mouth": "closed-lips",
            "intonation": "A gentle falling voice can finish a statement.",
            "review_status": "illustrative-unreviewed",
        }
    if reference == "My name is Alex. I am learning English.":
        return {
            "target": "Pause between ideas",
            "syllables": [],
            "tip": "Pause briefly after “Alex”, then begin the next idea. Aim for an easy pace rather than copying an accent.",
            "pause_after": "Alex",
            "intonation": "Finish each statement with a comfortable falling tone.",
            "review_status": "illustrative-unreviewed",
        }
    return {}
