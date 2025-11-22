import json
import re

# Load FAQs
# Corrected load_faqs function
def load_faqs():
    try:
        with open('faqs.json', 'r', encoding='utf-8') as f:
            # The 'faqs' key is accessed correctly
            return json.load(f)['faqs'] 
    except FileNotFoundError:
        print("Error: 'faqs.json' not found. Please ensure it is in the same directory.")
        # Return an empty list or raise an error to stop execution
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode 'faqs.json'. Please check file content for valid JSON structure.")
        return []

# OPTIONAL: A more robust scoring system
def find_match(user_input, faqs):
    user_lower = user_input.lower()
    best_match = None
    best_score = 0
    
    for faq in faqs:
        # Base score from keyword matches (e.g., 1 point per keyword)
        score = sum(1 for kw in faq['keywords'] if re.search(r'\b' + re.escape(kw) + r'\b', user_lower))
        
        # Add a bonus point for a high-confidence match (e.g., user input is very close to the question)
        if user_lower == faq['question'].lower():
            score += 10 # Assign a high bonus to override keyword scores

        if score > best_score: # Use STRICTLY greater-than here to favor higher-scoring FAQs
            best_score = score
            best_match = faq

    return best_match if best_score > 0 else None

# Chatbot loop
def run_mepco_bot():
    faqs = load_faqs()
    print("🤖 Mepco Assistant: Hi! I'm your campus guide. Ask anything about Mepco (type 'quit' to exit)")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Mepco Assistant: See you on campus! 🌟")
            break
        
        match = find_match(user_input, faqs)
        if match:
            print(f"Mepco Assistant: {match['answer']}")
        else:
            print("Mepco Assistant: Hmm, I don't have that info yet. Try asking about placements, hostel, Fiesta, or departments!")

if __name__ == "__main__":
    run_mepco_bot()