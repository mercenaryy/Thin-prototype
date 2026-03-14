"""
main.py — CLI chat interface for the Personal Intelligence AI Agent.
Run this file in VS Code terminal: python main.py
"""

from agent import ask, data_summary

WELCOME = """
╔══════════════════════════════════════════════════════════╗
║         PERSONAL INTELLIGENCE AI — PROTOTYPE            ║
║  Your behavioral data has been loaded and analysed.     ║
║  Ask anything about your week, patterns, or habits.     ║
║  Type  'quit'  or  'exit'  to stop.                     ║
║  Type  'verbose'  to toggle detailed tool-call logs.    ║
╚══════════════════════════════════════════════════════════╝
"""

SAMPLE_QUESTIONS = [
    "What were my most common emotions this week?",
    "What habits did I repeat every day?",
    "Tell me about my relationship with family this week.",
    "When do I tend to feel stressed? What triggers it?",
    "What decisions did I make when I was tired?",
    "Summarize my open loops this week.",
    "What does my social life look like? Am I an introvert or extrovert?",
    "What are my top 3 behavioral patterns?",
    "Did I take care of my health this week?",
    "What are some patterns related to procrastination?",
]


def main():
    print(WELCOME)
    print("💡 Sample questions you can ask:")
    for i, q in enumerate(SAMPLE_QUESTIONS, 1):
        print(f"   {i:2}. {q}")
    print()

    verbose = False

    while True:
        try:
            user_input = input("You ▶  ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye! 👋")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("\nGoodbye! 👋")
            break

        if user_input.lower() == "verbose":
            verbose = not verbose
            print(f"[Verbose mode: {'ON' if verbose else 'OFF'}]\n")
            continue

        if user_input.lower() == "data":
            print("\n" + "─" * 60)
            print(data_summary[:3000] + "\n... (truncated)")
            print("─" * 60 + "\n")
            continue

        print("\nThinking…\n")
        response = ask(user_input, verbose=verbose)
        if response:
            print(f"Agent ▶  {response}\n")
        print("─" * 60)


if __name__ == "__main__":
    main()
