"""Four concurrent synthetic typed journeys against loopback only; not a production benchmark."""

import concurrent.futures
import http.cookiejar
import json
import secrets
import time
import urllib.request
import uuid

BASE = "http://127.0.0.1:8000/api/v1"


def journey(_):
    start = time.monotonic()
    jar = http.cookiejar.CookieJar()
    client = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    def request(path, data=None, method=None):
        headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": next((c.value for c in jar if c.name == "csrftoken"), ""),
        }
        payload = json.dumps(data).encode() if data is not None else None
        with client.open(
            urllib.request.Request(BASE + path, data=payload, headers=headers, method=method),
            timeout=30,
        ) as response:
            body = response.read()
            return json.loads(body) if body else None

    request("/auth/csrf/")
    username = "load-" + uuid.uuid4().hex
    password = secrets.token_urlsafe(32)
    request(
        "/auth/register/",
        {
            "username": username,
            "email": username + "@example.test",
            "display_name": "Synthetic load learner",
            "password": password,
            "eligible": True,
        },
    )
    try:
        courses = request("/courses/")["results"]
        lesson = next(
            lesson
            for c in courses
            for u in c["units"]
            if u["level"] == "A1"
            for lesson in u["lessons"]
        )
        session = request("/lesson-sessions/", {"lesson_version": lesson["id"]})
        for answer in ["am", "I am learning English"]:
            session = request(
                "/lesson-sessions/" + session["id"] + "/turns/",
                {
                    "activity_id": session["activity"]["id"],
                    "answer": answer,
                    "request_id": str(uuid.uuid4()),
                },
            )["session"]
        assert session["completed"]
        assert request("/learners/me/summary/")["completed_lessons"] == 1
        return time.monotonic() - start
    finally:
        request(
            "/learners/me/data/", {"password": password, "confirmation": "DELETE"}, method="DELETE"
        )


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(journey, range(4)))
    print(
        f"4/4 concurrent synthetic typed journeys passed; slowest journey {max(results):.2f}s. Synthetic accounts deleted. No production capacity claim."
    )
