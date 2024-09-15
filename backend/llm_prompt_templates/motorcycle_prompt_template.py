MOTORCYCLE_LLM_PROMPT_TEMPLATE: str = """
Your response should follow this exact format:

MAKE: [Motorcycle Make]
MODEL: [Motorcycle Model]
COLOR: [Motorcycle Color]
DESCRIPTION:
[Motorcycle Description]

Instructions for the description:
0. All written text should be in Polish, but the keys (MAKE, MODEL, COLOR, DESCRIPTION, etc.) should be in English
1. Start with a brief, catchy opening sentence that highlights the motorcycle's key appeal.
2. Include information in this order: year, condition, mileage (in Miles, not KM), key features, and any unique selling points.
3. Use formal yet engaging tone appealing to enthusiasts.
4. Use appropriate Polish terminology for motorcycle parts and features.
5. Explain any technical terms used.
6. Use vivid adjectives to describe the motorcycle's appearance and performance.
7. If any input data is missing, creatively work around it without mentioning the missing information.
8. Ensure all provided input data (year, make, model, mileage) is accurately incorporated into the description.
9. Do not include pricing, company details, or contact information.

Example output structure:
MAKE: Harley Davidson
MODEL: Fat Boy
COLOR: Czerwony/Czarny
DESCRIPTION:
Ten wyjątkowy Harley Davidson Fat Boy z 2003 roku to prawdziwa perła dla miłośników klasycznych cruiserów. Motocykl, z przebiegiem zaledwie 15,000 kilometrów, prezentuje się w nienagannym stanie technicznym i wizualnym. Wyposażony w potężny silnik Twin Cam 88B o pojemności 1450 cm³, zapewnia imponującą moc i charakterystyczny dźwięk. Chromowane wykończenia i masywna sylwetka podkreślają jego majestatyczny wygląd. Komfort jazdy zapewniają szerokie siedzenie i ergonomicznie umieszczone kontrolki. To nie tylko środek transportu, ale prawdziwa ikona stylu i amerykańskiej motoryzacji.

Input for this request:
Year: {year}
Make: {make}
Model: {model}
Color: {color}
Odometer: {odometer_miles} Miles

Polish description to revise:
{current_description}
"""