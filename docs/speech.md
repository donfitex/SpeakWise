# Speech services

Free default: scripted teacher, typed exercises, local recording preview, and optional browser model speech. Server transcription, synthesis, alignment, and pronunciation are separate interfaces in `speech/providers.py`. Default server providers are disabled and return uncertainty, not invented results.

An optional OpenAI transcription adapter uses `SPEECH_PROVIDER=openai`, secure `SPEECH_API_KEY`, and `SPEECH_TRANSCRIPTION_MODEL`. This is not free; configure billing limits and review provider processing/retention before enabling it. Required HTTPS destination: api.openai.com. No credential is necessary for local typed practice. Do not add an API key to frontend variables. Transcription is supporting text evidence and never a phoneme evaluator. No calibrated pronunciation service is included yet.

The mock transcriber requires ALLOW_MOCK_SPEECH in test configuration; it emits visibly simulated text, must not update mastery, and is not accepted as live speech validation. Provider failures use safe fallback messages and do not log recordings, keys, or full transcripts.
