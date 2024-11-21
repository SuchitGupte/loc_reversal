from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd
import torch

# Load dataset
file_path = "data/toy_dataset.csv" 
data = pd.read_csv(file_path)

# List of LLaMA models
models = [
    'meta-llama/Llama-3.2-1B',
]

device = "cuda"
def evaluate_model(model_name, data):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    correct_predictions = 0
    results = []
    for _, row in data.iterrows():
        question = row["Question"]
        options = [
            row["Option 1"], row["Option 2"], row["Option 3"],
            row["Option 4"], row["Option 5"], row["Option 6"]
        ]
        correct_answer = row["Correct answer"]

        # Prompt format
        prompt = f"Question: {question}\nOptions: {', '.join(options)}\nAnswer:"
        
        # Tokenize the prompt and generate the output
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        outputs = model.generate(**inputs, max_new_tokens=20)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Model prediction
        predicted_option = next((opt for opt in options if opt in generated_text), None)

        results.append({
            "Question": question,
            "Predicted Answer": predicted_option,
            "Correct Answer": correct_answer,
            "Correct": predicted_option == correct_answer
        })
        if predicted_option == correct_answer:
            correct_predictions += 1
    accuracy = correct_predictions / len(data)
    return results, accuracy

for model_name in models:
    print(f"Evaluating {model_name}...")
    results, accuracy = evaluate_model(model_name, data)
    print(f"Accuracy for {model_name}: {accuracy:.2f}")
    output_file = f"{model_name.replace('/', '_')}_results.csv"
    pd.DataFrame(results).to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")
