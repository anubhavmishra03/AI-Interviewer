from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

# Load pre-trained Sentence-BERT model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Function to load questions from a JSON file
def load_questions(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Function to embed sentences using SBERT
def embed_sentence(sentence):
    return model.encode([sentence])[0]

# Function to compute cosine similarity between two sentence embeddings
def compute_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

# Function to conduct interview and collect answers
def conduct_interview(questions):
    responses = []
    print("Starting the interview...")
    for question_data in questions:
        question = question_data['question']
        print(f"Question: {question}")
        answer = input("Your answer: ")
        responses.append(answer)
    return responses

# Function to evaluate candidate answers using cosine similarity
def score_answers(questions, responses):
    total_score = 0
    max_score_per_question = 10  # Max score for each question
    
    for idx, question_data in enumerate(questions):
        candidate_answer = responses[idx]
        candidate_embedding = embed_sentence(candidate_answer)
        
        possible_answers = question_data['answers']
        best_match_score = 0
        
        # Compare candidate's response with all possible answers
        for answer_data in possible_answers:
            correct_answer = answer_data['response']
            correct_embedding = embed_sentence(correct_answer)
            similarity = compute_similarity(candidate_embedding, correct_embedding)
            normalized_score = similarity * answer_data['score']  # Score weighted by similarity
            best_match_score = max(best_match_score, normalized_score)
        
        total_score += best_match_score
    
    return total_score

# Function to rank candidates
def rank_candidates(candidate_scores):
    return sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)

# Main interview process
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
    
    # Rank candidates
    ranked_candidates = rank_candidates(candidates)
    print("\nFinal Ranking:")
    for idx, (name, score) in enumerate(ranked_candidates):
        print(f"{idx+1}. {name}: {score} points")

# Run the interview process
if __name__ == "__main__":
    interview_process('questions.json')
