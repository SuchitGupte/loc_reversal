# Requirements
# pip install accelerate peft bitsandbytes transformers trl

# All imports
import torch
from datasets import load_dataset, Dataset
from peft import LoraConfig, AutoPeftModelForCausalLM
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from trl import SFTTrainer
import os
from transformers import GenerationConfig
import pandas as pd
from tqdm import tqdm
import ast

import argparse

parser = argparse.ArgumentParser(description="Process user input from the command line.")
parser.add_argument("--model", type=str, help="Model to test", default="meta-llama/Meta-Llama-3.1-8B-Instruct")
parser.add_argument("--test", type=str, required=True, help="Path to testing data")
parser.add_argument("--save", type=str, required=True, help="Path to save response data")

args = parser.parse_args()

# specify the model 
model_id=args.model

def get_model_and_tokenizer(model_id):
  tokenizer = AutoTokenizer.from_pretrained(model_id)
  tokenizer.pad_token = tokenizer.eos_token
  bnb_config = BitsAndBytesConfig(
      load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype="float16", bnb_4bit_use_double_quant=True
  )
  model = AutoModelForCausalLM.from_pretrained(
      model_id, quantization_config=bnb_config, device_map="auto"
  )
  model.config.use_cache=False
  model.config.pretraining_tp=1
  return model, tokenizer

# Load model 
model, tokenizer = get_model_and_tokenizer(model_id)

def generate_response(user_input):
  prompt = formatted_prompt(user_input)
  inputs = tokenizer([prompt], return_tensors="pt")
  generation_config = GenerationConfig(penalty_alpha=0.6,do_sample = True,
      top_k=2,temperature=0.9,repetition_penalty=1.2,
      max_new_tokens=100,pad_token_id=tokenizer.eos_token_id
  )
  inputs = tokenizer(prompt, return_tensors="pt").to('cuda')
  outputs = model.generate(**inputs, generation_config=generation_config)
  theresponse = (tokenizer.decode(outputs[0], skip_special_tokens=True))
  return theresponse

def formatted_prompt(question)-> str:
    return f"<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant:"

def parse_response(response):
  answer = response.split("<|im_start|>assistant:")[1].split("<|im_end|>")[0]
  if "\n" in answer:
    answer = answer.split("\n")[0]
  answer = answer.replace("(", "").replace(")", "").replace(".", "").strip()
  answer = answer.split(" ")[0]
  try:
    answer = int(answer)
  except:
    answer = None
  return answer

def calculate_accuracy(response_data):
  correct = 0
  total = 0
  
  for row in response_data:
    total += 1
    if row['model_answer'] == row['gt_option']:
      correct += 1

  print(f"Correct: {correct}/{total}")
  print(f"Accuracy: {correct/total}")
  
def save_responses(response_data, path):
  response_data_df = pd.DataFrame(response_data)
  response_data_df.to_csv(path)
  

# load and read the testing csv
testing = pd.read_csv(args.test)
  
# test on the dataset, save responses and get model answers 
instruction = "Select the correct option and answer in one word without any explanation."
response_data = []
for index, row in tqdm(testing.iterrows()):
  ques = row["question"]
  options = ast.literal_eval(row['options'])
  question = f'{instruction}\n{ques}\n'
  for i, option in enumerate(options):
      question += f'({i+1}) {option} '
  response = generate_response(user_input=question)
  row["response"] = response
  row["model_answer"] = parse_response(response)
  response_data.append(row)
  
calculate_accuracy(response_data)

save_responses(response_data, args.save)
