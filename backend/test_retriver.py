from services.retriver import get_relevant_chunks

results = get_relevant_chunks("your test question here", k=3)
for chunk in results:
    print(chunk[:100], "\n---")