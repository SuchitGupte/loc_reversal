import csv
import random
import string
# Prepapre data to improve finetuning

def generate_name(prefix_length=3, suffixes=None):
    prefixes = ['Monaga', 'Suchi', 'Hannam', 'Sriji', 'Huana', 'Sachi', 'Advi', 'Vikram', 'Sarve', 'Nimi']
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes) if suffixes else ''
    return prefix.capitalize() + suffix

def main():
    continent_suffixes = ['ia', 'ica', 'oria']
    country_suffixes = ['stan', 'land', 'nia']
    state_suffixes = ['ria', 'sia', 'berg', 'rashtra']
    city_suffixes = ['ville', 'burg', 'giri', 'pur', 'bad']

    data = []
    used_names = set()

    for _ in range(2):  # 2 continents
        continent = generate_name(suffixes=continent_suffixes)
        while continent in used_names:
            continent = generate_name(suffixes=continent_suffixes)
        used_names.add(continent)

        for _ in range(3):  # 3 countries per continent
            country = generate_name(suffixes=country_suffixes)
            while country in used_names:
                country = generate_name(suffixes=country_suffixes)
            used_names.add(country)

            for _ in range(3):  # 3 states per country
                state = generate_name(suffixes=state_suffixes)
                while state in used_names:
                    state = generate_name(suffixes=state_suffixes)
                used_names.add(state)

                for _ in range(3):  # 3 cities per state
                    city = generate_name(suffixes=city_suffixes)
                    while city in used_names:
                        city = generate_name(suffixes=city_suffixes)
                    used_names.add(city)

                    data.append([city, state, country, continent])

    # Write to CSV
    with open('synthetic_locations.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['City', 'State', 'Country', 'Continent'])
        writer.writerows(data)

    print("CSV file 'synthetic_locations.csv' has been generated.")
    print(f"Total entries: {len(data)}")

if __name__ == "__main__":
    main()