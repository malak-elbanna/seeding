import pandas as pd
import glob
import json
import os

def process_csv_files(csv_folder_path, output_json_path):
    country_data = {}

    visa_file = os.path.join(csv_folder_path, "VISA.csv")
    if os.path.exists(visa_file):
        visa_df = pd.read_csv(visa_file)
        for _, row in visa_df.iterrows():
            country = row["Country"].strip()
            if country not in country_data:
                country_data[country] = {"countryName": country, "Seasonal": [], "Transportation": [], "Visa": [], "cities": []}
            country_data[country]["Visa"].append({"question": row["Question"], "answer": row["Answer"]})

    seasonal_file = os.path.join(csv_folder_path, "Seasonal.csv")
    if os.path.exists(seasonal_file):
        seasonal_df = pd.read_csv(seasonal_file)
        for _, row in seasonal_df.iterrows():
            country = row["Country"].strip()
            if country not in country_data:
                country_data[country] = {"countryName": country, "Seasonal": [], "Transportation": [], "Visa": [], "cities": []}
            country_data[country]["Seasonal"].append({"question": row["Question"], "answer": row["Answer"]})

    transportation_file = os.path.join(csv_folder_path, "Transportation.csv")
    if os.path.exists(transportation_file):
        transportation_df = pd.read_csv(transportation_file)
        for _, row in transportation_df.iterrows():
            country = row["Country"].strip()
            if country not in country_data:
                country_data[country] = {"countryName": country, "Seasonal": [], "Transportation": [], "Visa": [], "cities": []}
            country_data[country]["Transportation"].append({
                "from": row["From"],
                "to": row["To"],
                "transportMode": row["Transport Mode"],
                "provider": row["Provider"],
                "schedule": row["Schedule"],
                "routeInfo": row["Route Info"],
                "durationHours": row["Duration in hours"],
                "priceRangeUSD": row["Price Range in USD"],
                "costDetails": row["Cost Details and Options"],
                "additionalInfo": row["Additional Info"]
            })

    def get_or_create_city(country, city_name):
        if country not in country_data:
            country_data[country] = {"countryName": country, "Seasonal": [], "Transportation": [], "Visa": [], "cities": []}
        city_list = country_data[country]["cities"]
        city = next((c for c in city_list if c["name"] == city_name), None)
        if not city:
            city = {"name": city_name, "activities": [], "restaurants": [], "dishes": [], "accommodations": [], "scams": []}
            city_list.append(city)
        return city

    restaurants_file = os.path.join(csv_folder_path, "Restaurants.csv")
    if os.path.exists(restaurants_file):
        restaurants_df = pd.read_csv(restaurants_file)
        for _, row in restaurants_df.iterrows():
            city = get_or_create_city(row["Country"].strip(), row["City"].strip())
            city["restaurants"].append({
                "name": row["Restaurant Name"],
                "cuisineType": row["Type of Cuisine"],
                "mealsServed": row["Meals Served"],
                "recommendedDish": row["Recommended Dish"],
                "mealDescription": row["Meal Description"],
                "avgPriceUSD": row["Avg Price per Person (USD)"],
                "budgetRange": row["Budget Range"],
                "suitability": row["Suitability"]
            })

    activity_file = os.path.join(csv_folder_path, "Activity.csv")
    if os.path.exists(activity_file):
        activity_df = pd.read_csv(activity_file)
        for _, row in activity_df.iterrows():
            city = get_or_create_city(row["Country"].strip(), row["City"].strip())
            city["activities"].append({
                "activity": row["Activity"],
                "description": row["Description"],
                "travelerType": row["Type of Traveler"],
                "duration": row["Duration"],
                "budgetUSD": row["Budget (USD)"],
                "budgetDetails": row["Budget details"],
                "tips": row["Tips and Recommendations"],
                "familyFriendly": row["Family friendly"],
                "category": row["CATEGORY"]
            })

    accommodations_file = os.path.join(csv_folder_path, "Accomodations.csv")
    if os.path.exists(accommodations_file):
        accommodations_df = pd.read_csv(accommodations_file)
        for _, row in accommodations_df.iterrows():
            city = get_or_create_city(row["Country"].strip(), row["City"].strip())
            city["accommodations"].append({
                "name": row["Accommodation Name"],
                "details": row["Accommodation Details"],
                "type": row["Type"],
                "avgNightPriceUSD": row["Avg Night Price (USD)"]
            })

    dishes_file = os.path.join(csv_folder_path, "Dishes.csv")
    if os.path.exists(dishes_file):
        dishes_df = pd.read_csv(dishes_file)
        for _, row in dishes_df.iterrows():
            city = get_or_create_city(row["Country"].strip(), row["City"].strip())
            city["dishes"].append({
                "name": row["Dish Name"],
                "details": row["Dish Details"],
                "type": row["Type"],
                "avgPriceUSD": row["Avg Price (USD)"],
                "bestFor": row["Best For"]
            })

    scams_file = os.path.join(csv_folder_path, "Scams.csv")
    if os.path.exists(scams_file):
        scams_df = pd.read_csv(scams_file)
        for _, row in scams_df.iterrows():
            city = get_or_create_city(row["Country"].strip(), row["City"].strip())
            city["scams"].append({
                "type": row["Scam Type"],
                "description": row["Description"],
                "location": row["Location"],
                "preventionTips": row["Prevention Tips"]
            })

    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(list(country_data.values()), json_file, indent=4, ensure_ascii=False)

    print("data has been successfully processed")

if __name__ == "__main__":
    process_csv_files("D:/year 3/s2/seeding/csv", "D:/year 3/s2/seeding/cleaned_data.json")
