import joblib
from sentence_transformers import SentenceTransformer

model_embedding = SentenceTransformer('all-MiniLM-L6-v2')  
model_classification = joblib.load("log_classifier_svm.joblib")   #NLP_Log_Classification\

def classify_with_bert(log_message):
    embeddings = model_embedding.encode([log_message])
    probabilities = model_classification.predict_proba(embeddings)
    #print(probabilities)
    if max(probabilities[0]) < 0.5:
        return "Unclassified"
    predicted_label = model_classification.predict(embeddings)[0]
    #print(model_classification.predict(embeddings))
    
    return predicted_label


if __name__ == "__main__":
    logs = [
        "alpha.osapi_compute.wsgi.server - 12.10.11 - API returned 404 not found error",
        "GET /v2/3454/servers/detail HTTP/1.1 RCODE   404 len: 1583 time: 0.1878400",
        "System crashed due to drivers errors when restarting the server",
        "Multiple login failures occurred on user 6454 account",
        "Server A790 was restarted unexpectedly during the process of data transfer",
        "Hello Good Morning!",
    ]
    for log in logs:
        label = classify_with_bert(log)
        print(log, "->", label)