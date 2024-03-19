import pandas as pd
import csv
import json

def get_restaurant_data(filename):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def calculate_distance(column_name, filename, x_coord, y_coord):
    table = get_restaurant_data(filename)

    if table is not None:
        restaurants_with_coords = table.dropna(subset=[column_name])

        distances = {}
        for index, row in restaurants_with_coords.iterrows():
            restaurant_name = row['Name']
            restaurant_coords = row[column_name].split(",")
            restaurant_x = float(restaurant_coords[0])
            restaurant_y = float(restaurant_coords[1])

            distance_to_restaurant = distance(x_coord, y_coord, restaurant_x, restaurant_y)
            distances[restaurant_name] = distance_to_restaurant

        return distances
    else:
        return {'message': f"Error: File '{filename}' not found."}

def normalize_distance(distances):
    min_distance = min(distances.values())
    max_distance = max(distances.values())
    
    normalized_distances = {}
    for restaurant, distance in distances.items():
        normalized_distance = (distance - min_distance) / (max_distance - min_distance)
        normalized_distances[restaurant] = float(normalized_distance)
    
    return normalized_distances

def get_restaurant_prices(filename):
    restaurant_prices = {}

    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            restaurant_name = row['Name']
            price = row['Price']
            restaurant_prices[restaurant_name] = float(price)

    return restaurant_prices

def get_restaurant_ratings(filename):
    rating = {}

    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            restaurant_name = row['Name']
            r = row['Rating']
            rating[restaurant_name] = round(float(r) / 10, 2)  # Format to two decimal places

    return rating

def get_restaurant_coordinates(filename):
    coordinates = {}

    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            restaurant_name = row['Name']
            c = row['Coordinates']
            coordinates[restaurant_name] = c

    return coordinates

def get_restaurant_address(filename):
    addresses = {}

    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            restaurant_name = row['Name']
            a = row['Address']
            addresses[restaurant_name] = a

    return addresses

def calcequation(nD, nP, nR):
    Wr = 0.5
    Wp = 0.25
    Wd = 0.25
    
    pf = (Wd * (1 - nD) + (Wp * (1 - nP)) + (Wr * nR)) * 10
    return round(pf, 1)  # Format to one decimal place

# Example usage
filename = 'foodmaps.csv'
column_name = 'Coordinates'
user_x = 37.806959540228256
user_y = -122.431905446027

distances = calculate_distance(column_name, filename, user_x, user_y)

if isinstance(distances, dict) and 'message' not in distances:
    normalized_distances = normalize_distance(distances)
    prices = get_restaurant_prices(filename)
    ratings = get_restaurant_ratings(filename)
    coordinates = get_restaurant_coordinates(filename)
    addresses = get_restaurant_address(filename)
    
    # Export to CSV
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = ['Restaurant',  'Address', 'Relative Rating', 'Objective Rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for restaurant, distance in distances.items():
            dist = normalized_distances[restaurant]
            price = prices[restaurant]
            rating = ratings[restaurant]
            coordinate = coordinates[restaurant]
            address = addresses[restaurant]
            rr = calcequation(dist, price, rating)
            rating = round(rating * 10, 1)

            writer.writerow({'Restaurant': restaurant,  'Address': address, 'Relative Rating': rr, 'Objective Rating': rating})
    
    # Export to JSON
    output_data = []
    for restaurant, distance in distances.items():
        dist = normalized_distances[restaurant]
        price = prices[restaurant]
        rating = ratings[restaurant]
        coordinate = coordinates[restaurant]
        address = addresses[restaurant]
        rr = calcequation(dist, price, rating)
        rating = round(rating * 10, 1)

        output_data.append({
            'Restaurant': restaurant,
            'Address': address,
            'Relative Rating': rr,
            'Objective Rating': rating
        })

    with open('output.json', 'w') as jsonfile:
        json.dump(output_data, jsonfile, indent=4)
else:
    print(distances['message'])
