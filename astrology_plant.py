#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 11:18:01 2024

@author: pocketpuppy
"""

import json
import requests
import sqlite3
import openai
from openai import OpenAI
import pandas as pd
from tabulate import tabulate


USER_KEY = 'KEY'

# Create an OpenAPI client
client = OpenAI(
    api_key=USER_KEY,
    )


conn = sqlite3.connect('plants.db')
cursor = conn.cursor()


# Create table to hold data from API
def create_table():
    # cursor.execute('DROP TABLE IF EXISTS plant_star_rec')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS plant_star_rec (
        plant_name TEXT,
        birthday TEXT,
        star_sign TEXT
    )
    ''')
    conn.commit()


def store_plant_rec(plant,bday,star_sign):
    cursor.execute('''
    INSERT INTO plant_star_rec (
        plant_name, birthday, star_sign
    ) VALUES (?, ?, ?)
    ''', (plant, bday, star_sign)
    )
    conn.commit()


def validate_str_input(prompt, options):
    while True:
        user_input = input(prompt).lower()
        if user_input in options:
            return user_input
        else:
            print(f"Invalid input. Please use the examples given and"
                  f" enter one of the following options: "
                  f"{', '.join(options)}")


def validate_date_input():
    while True:
        bday_input = str(input("Please enter bday MM/DD (e.g. 07/14): "))
        try:
            month = int(bday_input[:2])
            day = int(bday_input[3:])
            if month == 2 and 1 <= day <= 28:
                return [month, day]
            elif month in {4, 6, 9, 11} and 1 <= day <= 30:
                return [month, day]
            elif month in {1, 3, 5, 7, 8, 10, 12} and 1 <= day <= 31:
                return [month, day]
            else:
                print(f"\nInvalid input. Please enter your bday as MM/DD"
                      " and ensure you enter accurate dates.\n")

        except ValueError:
            print("Invalid input. Please ensure you enter "
                  "numeric values for month and day.")


def retrieve_bday_month(bday_input):
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    for i in range(13):
        if (bday_input[0]-1) == i:
            return months[i]


# Returns sun sign based on month and day parameters
def get_astrological_sign(month, day):
    if (month == 3 and day >= 21) or (month == 4 and day <= 20):
        return "aries"
    elif (month == 4 and day >= 21) or (month == 5 and day <= 21):
        return "taurus"
    elif (month == 5 and day >= 22) or (month == 6 and day <= 21):
        return "gemini"
    elif (month == 6 and day >= 22) or (month == 7 and day <= 23):
        return "cancer"
    elif (month == 7 and day >= 24) or (month == 8 and day <= 23):
        return "leo"
    elif (month == 9 and day >= 24) or (month == 10 and day <= 23):
        return "libra"
    elif (month == 10 and day >= 24) or (month == 11 and day <= 22):
        return "scorpio"
    elif (month == 1 and day >= 21) or (month == 2 and day <= 19):
        return "aquarius"
    elif (month == 2 and day >= 20) or (month == 3 and day <= 20):
        return "pisces"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 20):
        return "capricorn"
    elif (month == 11 and day >= 23) or (month == 12 and day <= 21):
        return "sagittarius"
    elif (month == 8 and day >= 24) or (month == 9 and day <= 23):
        return "virgo"


def get_chatgpt_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": (f"You are a houseplant and "
                                           f"astrology expert. You can describe"
                                           f"both topics well in few words.")},
            {"role": "user", "content": prompt}
            ]
    )

    message = response.choices[0].message.content
    return message


def main():
    bday = validate_date_input()
    bday_month = retrieve_bday_month(bday)
    sun_sign = get_astrological_sign(bday[0], bday[1])
    birthday_formatted = (f"{bday_month} {bday[1]}")
    create_table()

    sunlight_options = [
                'full sun',
                'part shade',
                'full shade',
                'part sun/part shade'
                ]

    watering_options = [
        'frequent',
        'minimum',
        'average'
        ]

    maintenance_options = [
        'low',
        'moderate',
        'high'
        ]

    print("\nPlease enter your plant preferences:\n")

    # Take sunlight preferences
    sunlight_pref = validate_str_input(
        ("Preferred sunlight "
         "(e.g., 'full sun', 'part shade', 'full shade','part sun/part shade'): "
        ),
        sunlight_options)

    # Take watering freq. preferences
    watering_pref = validate_str_input(
        "Preferred watering "
        "(e.g., 'frequent', 'minimum', 'average'): ",
        watering_options)

    # Take maintenance level pref.
    maintenance_pref = validate_str_input(
        "Preferred maintenance level "
        "(e.g., 'low', 'moderate', 'high'): ",
        maintenance_options)
    
    print(f"\nYour birthday is {bday_month} {bday[1]}. "
          f"Your sun sign is {sun_sign.capitalize()}.\n")
    print(f"\nYou prefer a plant that needs {sunlight_pref}, "
          f"{watering_pref} watering, and is {maintenance_pref} maintenance.")
    
    
    prompt1 = (f"Name a houseplant that matches {sun_sign.capitalize()}, "
              f"is {maintenance_pref} maintenance, and needs {sunlight_pref}, "
              f"{watering_pref} watering."
              f"Only reply with the common name and scientific name, "
              f"formatted like: Common Name (Scientific Name)")

    plant_rec = get_chatgpt_response(prompt1)

    store_plant_rec(plant_rec,birthday_formatted,sun_sign)

    prompt2 = (f"Please give me brief plant care instructions for {plant_rec} "
               f"and explain why it matches my star sign.")
    print(f"\n{get_chatgpt_response(prompt2)}\n")


    cursor.execute('SELECT * FROM plant_star_rec')
    plant_rec_list = cursor.fetchall()

    #df = pd.DataFrame(plant_rec_list, columns = ["Plant", "B-day", "Sign"])
    #print(df)

    tbl_columns = ["Plant", "B-day", "Sign"]
    print(tabulate(plant_rec_list, headers = tbl_columns, tablefmt='fancy_grid'))


main()
