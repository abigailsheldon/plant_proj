#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 11:18:01 2024

@author: pocketpuppy
"""

import json
import requests
import sqlite3
import os
import openai
from openai import OpenAI


USER_KEY = 'sk-proj-l9zydIhqqCjdi8wrz9MYT3BlbkFJO1rbX8CEx48OmxTOVuBB'
PROJ_API_KEY = 'sk-proj-B5fkI6Yc6kAIbrn9qvPxT3BlbkFJfPSV3pbaA2wpbbxLNna2'


# Create an OpenAPI client
client = OpenAI(
    api_key=USER_KEY,
    )


astro_decriptions = {
    "aries": ("An Aries was born within March 21-April 20. "
              "Aries are natural born leaders. They are tenacious and "
              "like taking risks. They enjoy new experiences and are very "
              "passionate. They are energetic, creative, caring, and generous."
              "Aries are fiery, passionatd, determined, and courageous."),

    "taurus": ("A Taurus was born within April 21-May 21. "
               "Taurus is loyal, generous, kind, and patient."),

    "gemini": ("A Gemini was born within May 22-June 21. "
               "Gemini are independent, curious, charming, and gentle."),

    "cancer": ("A Cancer was born within June 22-July 23. "
               "Cancer are compassionate, sentimental, protective, and "
               "emotional."),

    "leo": ("A Leo was born within July 24-Aug 23. "
            "Leo are charismatic, dramatic, confident, and fun."),

    "libra": ("A Libra was born within Sept 24-Oct 23. "
              "Libra are romantic, artistic, friendly, and persuasive."),

    "scorpio": ("A Scorpio was born within Oct 24-Nov 22. "
                "Scorpio are mysterious, powerful, brave, and resourceful."),

    "aquarius": ("An Aquarius was born within Jan 21-Feb 19. "
                 "Aquarius are humanitarian, eccentric, individualistic, "
                 "and cool."),

    "pisces": ("A Pisces was born within Feb 20-March 20. "
               "Pisces are creative, easy-going, faithful, and sensitive."),

    "capricorn": ("A Capricorn was born within Dec 22-Jan 20. "
                  "Capricorn are traditional, disciplined, ambitious, "
                  "and independent."),

    "sagittarius": ("A Sagittarius was born within Nov 23-Dec 21. "
                    "Sagittarius are philosophical, optimistic, "
                    "adventurous, and free-spirited."),

    "virgo": ("A Virgo was born within Aug 24-Sept 23. "
              "Virgo are humble, practical, organized, and "
              "patient. They are reliable and clever.")
            }


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
            {"role": "system", "content": ("You are a houseplant and "
                                           "astrology expert.")},
            {"role": "user", "content": prompt}
            ]
    )
    
    message = response.choices[0].message.content
    return message


def main():
    bday = validate_date_input()
    bday_month = retrieve_bday_month(bday)
    sun_sign = get_astrological_sign(bday[0], bday[1])
    
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
        (
            "Preferred sunlight (e.g., 'full sun', 'part shade', "
            "'full shade','part sun/part shade'): "
            ),
    sunlight_options)
    
    # Take watering freq. preferences
    watering_pref = validate_str_input(
        "Preferred watering (e.g., 'frequent', 'minimum', 'average'): ",
        watering_options)
    
    # Take maintenance level pref.
    maintenance_pref = validate_str_input(
    "Preferred maintenance level (e.g., 'low', 'moderate', 'high'): ",
    maintenance_options)    
    
    
    print(f"\nYour birthday is {bday_month} {bday[1]}. Your sun sign is {sun_sign.capitalize()}.\n")
    
    prompt = (f"My birthday is {bday_month} {bday[1]} and my star sign is {sun_sign.capitalize()}."
              f"Name a plant that meets my preferences and astrology sign. Just give me the plant name."
              f"Say nothing other than the plant name. Do not use punctuation.")
    
    print(get_chatgpt_response(prompt))

    
main()


'''
completion = client.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages=[
        
        {"role": "system", "content": ("You are a houseplant expert and can explain plant care instructions"
                                       " clearly in a few words. You are also an astrology expert. "
                                       " You know all the astrological signs very well.")
         },
        {"role": "user", "content": (f"My birthday is {bday_month} {bday[1]} and my star sign is {sun_sign.capitalize()}. "
                                     f" I prefer a plant that needs {sunlight_pref}, {watering_pref} watering, and "
                                     f" requires {maintenance_pref} maintenance. "
                                     f"What is the best housplant for me based on my sign and preferences and why?")
                                     }
    ]
)
print(completion.choices[0].message.content) 
'''
