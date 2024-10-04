import json

# Load JSON data
def load_questions(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Function to ask questions and collect responses
def conduct_interview(questions):
    responses = []
    print("Starting the interview...")
    for question_data in questions:
        question = question_data['question']
        print(f"Question: {question}")
        answer = input("Your answer: ")
        responses.append(answer)
    return responses

# Function to score the answers
def score_answers(questions, responses):
    total_score = 0
    for idx, question_data in enumerate(questions):
        possible_answers = question_data['answers']
        candidate_answer = responses[idx]
        # Compare answer with available answers and assign score
        best_match_score = 0
        for answer_data in possible_answers:
            if candidate_answer.lower() in answer_data['response'].lower():
                best_match_score = max(best_match_score, answer_data['score'])
        total_score += best_match_score
    return total_score

# Function to rank candidates
def rank_candidates(candidate_scores):
    return sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)

# Main process
def interview_process(json_file):
    questions = load_questions(json_file)
    candidates = {}
    while True:
        candidate_name = input("Enter candidate name (or 'exit' to finish): ")
        if candidate_name.lower() == 'exit':
            break
        responses = conduct_interview(questions)
        score = score_answers(questions, responses)
        candidates[candidate_name] = score
        print(f"Candidate {candidate_name} scored: {score}")
    
    # Ranking candidates
    ranked_candidates = rank_candidates(candidates)
    print("\nFinal Ranking:")
    for idx, (name, score) in enumerate(ranked_candidates):
        print(f"{idx+1}. {name}: {score} points")

# Run the interview process
if __name__ == "__main__":
    interview_process('questions.json')
