from utils.youtube import parse_duration, extract_video_id

def test_parse_duration():
    duration = "PT1H23M45S"
    result = parse_duration(duration)
    assert result == 5025

def test_extract_video_id_url():
    url = "https://www.youtube.com/watch?v=abcdefghijk"
    video_id = extract_video_id(url)
    assert video_id == "abcdefghijk"

    wrong_url = "https://www.ddwer.com/watch?v=rwrwreq"
    assert extract_video_id(wrong_url) == None

    short_url = "https://youtu.be/abcdefghijk"
    video_id = extract_video_id(short_url)
    assert video_id == "abcdefghijk"

