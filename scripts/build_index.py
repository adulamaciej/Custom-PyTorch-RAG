from app.rag import PyTorchRAG

# For quick test - runs entire pipeline on documentation

rag = PyTorchRAG()

query = "How do I disable gradient computation?"

results = rag.retrieve(query)


print("\nQUERY:")
print(query)


for i, result in enumerate(results, start=1):
    print("\n----------------------")
    print(f"RESULT {i}")
    print("Score:", result.score)
    print("Source:", result.chunk.source)
    print("Section:", result.chunk.section)
    print()
    print(result.chunk.content[:500])


context, sources = rag.context_builder.build(results)

print("\nCONTEXT:\n")
print(context[:5000])

print("\nSOURCES:")

for source in sources:
    print(source)


    result = rag.ask(
    "How do I disable gradient computation?"
)

print("\nANSWER:\n")
print(result["answer"])

print("\nSOURCES:\n")
for source in result["sources"]:
    print(source)