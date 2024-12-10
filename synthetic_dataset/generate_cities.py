import csv
import random

def generate_city_name():
    syllables = ['ka', 'ma', 'ni', 'ta', 'so', 'po', 'la', 'bu', 're', 'shi', 'zu', 'mo', 'da', 'ke', 'te', 'va', 'se']
    name = ''.join(random.choice(syllables) for _ in range(random.randint(2, 4)))
    return name.capitalize()

def generate_state_name():
    states = ['Urbia', 'Landsworth', 'Bayshire', 'Vanguard', 'Mireford', 'Argon', 'Harrington', 'Talsin', 'Almera', 'Nendora']
    return random.choice(states)

def generate_country_name():
    countries = ['Kandara', 'Zelphar', 'Tirania', 'Balandia', 'Sundarim', 'Voltria', 'Calinth', 'Vekharia', 'Meridia', 'Goshan']
    return random.choice(countries)

def generate_continent_name():
    continents = ['Ardia', 'Eura', 'Vallora', 'Yenith', 'Xylandia', 'Ziratha']
    return random.choice(continents)

def generate_data():
    cities = []
    seen_cities = {}  
    all_city_names = [] 

    for _ in range(800):
        city_name = generate_city_name()
        state_name = generate_state_name()
        country_name = generate_country_name()
        continent_name = generate_continent_name()

        while city_name in seen_cities:
            city_name = generate_city_name()
        seen_cities[city_name] = 1
        all_city_names.append(city_name)

        cities.append([city_name, state_name, country_name, continent_name, 'No'])

    shared_cities = random.sample(all_city_names, 200) 
    for city_name in shared_cities:
        state_name_1 = generate_state_name()
        country_name_1 = generate_country_name()
        continent_name_1 = generate_continent_name()

        state_name_2 = generate_state_name()
        country_name_2 = generate_country_name()
        continent_name_2 = generate_continent_name()

        cities.append([city_name, state_name_1, country_name_1, continent_name_1, 'Yes'])

        cities.append([city_name, state_name_2, country_name_2, continent_name_2, 'Yes'])

    return cities

def write_csv(data):
    with open('imaginary_cities_with_duplicates.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['City Name', 'State Name', 'Country Name', 'Continent Name', 'Duplicate Flag'])
        writer.writerows(data)

if __name__ == "__main__":
    city_data = generate_data()

    write_csv(city_data)

    print("CSV file 'imaginary_cities_with_duplicates.csv' has been generated.")
