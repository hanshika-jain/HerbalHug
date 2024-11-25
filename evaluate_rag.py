
import numpy as np
from sklearn.metrics import precision_score, recall_score

# Example logs (replace with your data)
questions = [
    "What are the uses of Aloe Vera?",
    "Where can I find Neem?",
    "What is the scientific name of Tulsi?",
]

retrieved_contexts = [
    {"Uses": "Skin treatment, digestive health"},  # Example retrieved data
    {"Location": "India, Sri Lanka"},             # Retrieved locations
    {"Scientific_Name": "Ocimum tenuiflorum"},    # Retrieved scientific name
]

generated_responses = [
    "The medicinal uses of Aloe Vera 🌿 are: Skin treatment, digestive health.",
    "📍 Neem is commonly found in India, Sri Lanka.",
    "The scientific name of Tulsi is 🌱 Ocimum tenuiflorum.",
]

# Ground truth for evaluation (expected answers for the questions)
ground_truths = [
    {"Uses": "Skin treatment, digestive health"},  # Correct uses
    {"Location": "India, Sri Lanka"},             # Correct location
    {"Scientific_Name": "Ocimum tenuiflorum"},    # Correct scientific name
]


def evaluate_faithfulness(retrieved_contexts, generated_responses):
    """
    Faithfulness checks if generated responses stay true to retrieved context.
    """
    faithfulness_scores = []
    for retrieved, response in zip(retrieved_contexts, generated_responses):
        if all(value in response for key, value in retrieved.items()):
            faithfulness_scores.append(1)  # Faithful
        else:
            faithfulness_scores.append(0)  # Not faithful
    return np.mean(faithfulness_scores)


def evaluate_context_precision_recall(ground_truths, retrieved_contexts):
    """
    Precision: Proportion of retrieved data that's relevant.
    Recall: Proportion of relevant data that's retrieved.
    """
    precisions = []
    recalls = []

    for ground_truth, retrieved in zip(ground_truths, retrieved_contexts):
        retrieved_keys = set(retrieved.keys())
        ground_truth_keys = set(ground_truth.keys())

        # Calculate precision and recall for keys
        precision = len(retrieved_keys & ground_truth_keys) / len(retrieved_keys) if retrieved_keys else 0
        recall = len(retrieved_keys & ground_truth_keys) / len(ground_truth_keys) if ground_truth_keys else 0

        precisions.append(precision)
        recalls.append(recall)

    return np.mean(precisions), np.mean(recalls)


def evaluate_relevance(questions, retrieved_contexts, ground_truths):
    """
    Relevance evaluates if retrieved contexts align with user intent.
    """
    relevance_scores = []
    for question, retrieved, ground_truth in zip(questions, retrieved_contexts, ground_truths):
        # Check if retrieved context contains key information based on the question type
        if any(keyword in question.lower() for keyword in ["use", "uses"]):
            relevant = "Uses" in retrieved and retrieved["Uses"] == ground_truth.get("Uses", "")
        elif any(keyword in question.lower() for keyword in ["where", "location"]):
            relevant = "Location" in retrieved and retrieved["Location"] == ground_truth.get("Location", "")
        elif "scientific name" in question.lower():
            relevant = "Scientific_Name" in retrieved and retrieved["Scientific_Name"] == ground_truth.get("Scientific_Name", "")
        else:
            relevant = False  # Question type not covered explicitly

        relevance_scores.append(1 if relevant else 0)
    return np.mean(relevance_scores)


# Run evaluations
faithfulness = evaluate_faithfulness(retrieved_contexts, generated_responses)
context_precision, context_recall = evaluate_context_precision_recall(ground_truths, retrieved_contexts)
relevance = evaluate_relevance(questions, retrieved_contexts, ground_truths)

# Print metrics
print(f"Faithfulness: {faithfulness:.2f}")
print(f"Context Precision: {context_precision:.2f}")
print(f"Context Recall: {context_recall:.2f}")
print(f"Relevance: {relevance:.2f}")
