import csv
import random

def generate_random_first_name():
    first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Hank', 'Ivy', 'Jack', 'Kara', 'Leo', 'Mona', 'Nate', 'Olivia', 'Paul', 'Quincy', 'Rita', 'Steve', 'Tracy']
    return random.choice(first_names)

def read_input_csv(input_file):
    city_data = []
    with open(input_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            city_data.append({
                'city': row['city'],
                'state': row['state'],
                'country': row['country'],
                'continent': row['continent']
            })
    return city_data

def generate_sentences(city_data):
    sentences = []
    used_combinations = set()  

    for entry in city_data:
        city_state_pair = (entry['city'], entry['state'])
        if city_state_pair not in used_combinations:
            first_name = generate_random_first_name()
            sentence = f"If {first_name} lives in {entry['city']} city, then {first_name} lives in {entry['state']} state."
            sentences.append([sentence, first_name])
            used_combinations.add(city_state_pair)

        state_country_pair = (entry['state'], entry['country'])
        if state_country_pair not in used_combinations:
            first_name = generate_random_first_name()
            sentence = f"If {first_name} lives in {entry['state']} state, then {first_name} lives in {entry['country']} country."
            sentences.append([sentence, first_name])
            used_combinations.add(state_country_pair)

        country_continent_pair = (entry['country'], entry['continent'])
        if country_continent_pair not in used_combinations:
            first_name = generate_random_first_name()
            sentence = f"If {first_name} lives in {entry['country']} country, then {first_name} lives in {entry['continent']} continent."
            sentences.append([sentence, first_name])
            used_combinations.add(country_continent_pair)

    return sentences

def write_output_csv(sentences, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Sentence', 'First Name'])
        writer.writerows(sentences)

def main():
    input_file = 'imaginary_cities_with_duplicates.csv'  
    output_file = 'train.csv'  

    city_data = read_input_csv(input_file)

    sentences = generate_sentences(city_data)

    write_output_csv(sentences, output_file)

    print(f"CSV file '{output_file}' has been generated.")

if __name__ == "__main__":
    main()
