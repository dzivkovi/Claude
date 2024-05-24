curl -H 'Content-Type: application/json' \
    -d '{"contents":[{"parts":[{"text":"Explain how AI works"}]}]}' \
    -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=$GOOGLE_API_KEY"
