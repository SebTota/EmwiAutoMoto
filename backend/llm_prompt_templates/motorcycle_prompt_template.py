MOTORCYCLE_LLM_PROMPT_TEMPLATE: str = """
Your response should NOT include any other text apart from what is requested. Your response must follow the following format:
Motorcycle Make
Motorcycle Model
Motorcycle Description

Example response structure:
Harley Davidson
Fat Boy
Ten wyjątkowy Harley Davidson Fat Boy z 2003 roku to...

Instructions for revision:
* Use formal yet engaging tone appealing to enthusiasts.
* Focus on motorcycle's features and condition.
* Use lists for features and specifications when appropriate.
* Exclude pricing, company details, and contact information.
* Correct make and model formatting.
* Ensure the description is concise but informative.
* Base style and structure on the provided examples.

Example Response One:
Harley Davidson
Sportster 1200
Ten wyjątkowy motocykl został wyprodukowany z okazji 95. rocznicy firmy Harley Davidson. Pochodzi od pierwszego właściciela i był starannie garażowany, co sprawia, że jest w nienagannym stanie technicznym i wizualnym. Przebieg wynosi zaledwie 6,500 mil. Jest to jeden z limitowanej serii 3,000 egzemplarzy, a ten konkretny model ma numer 2118. W zestawie znajduje się książka serwisowa oraz pełna dokumentacja zakupu, co potwierdza jego wyjątkowość.

Example Response Two:
`
Honda
VTX 1300R
Ten Honda VTX 1300R z 2005 roku to doskonały przykład dobrze utrzymanego klasyka. Motocykl został sprowadzony z USA i jest w bardzo dobrym stanie technicznym i wizualnym. Posiada jedynie 37 000 mil przebiegu, co świadczy o jego niewielkim użytkowaniu.

Oto jego kluczowe cechy:
* Nowe opony zapewniające pewne prowadzenie.
* Skórzane sakwy Viking zamykane na klucz, idealne do przewożenia bagażu.
* Oparcie pasażera z bagażnikiem, zwiększające komfort podróży dla dwóch osób.
* Motocykl garażowany, regularnie serwisowany, z ostatnią wymianą oleju.

Honda VTX 1300R jest gotowy do rejestracji w Polsce, wszystkie dokumenty zostały przetłumaczone na język polski. Zapraszamy do kontaktu!
`


This is the input for this request:
`
Year: {year}
Make: {make}
Model: {model}
Odometer: {odometer_miles} Miles

Polish description to revise:
{current_description}
`
"""