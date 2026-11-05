from curriculum.visuals import visual_cues


def test_visuals_only_match_the_reference_and_disclose_review_status():
    cues = visual_cues("My name is Alex")
    assert cues["target"] == "/m/ in “My”" and cues["mouth"] == "closed-lips"
    assert [s["text"] for s in cues["syllables"] if s["stress"]] == ["Al"]
    assert cues["review_status"] == "illustrative-unreviewed"
    assert visual_cues("unrelated text") == {}
