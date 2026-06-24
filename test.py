from chatbot.rag_engine import ask_rtc

result = ask_rtc(
"Who founded RTC?"
)

print(result["answer"])

print("\nSources:")

for source in result["sources"]:
    print(source)
