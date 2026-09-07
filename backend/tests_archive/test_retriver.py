from services.retriver import retrieve_chunks


question = "What is ergodic and mixed sourecs?"

results = retrieve_chunks(
    question,
    k=3
)

print("Retrieved chunks:")
print(results["documents"])