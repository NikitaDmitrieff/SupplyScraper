SELECT_CORRECT_FILTERS = """
Given a product, choose the most appropriate filters from the provided list to narrow down the search. Respect the format perfectly.

Available filter types:
bakery
grocery
supermarket
cafe
restaurant

Choose for the product "bread":
[
  "bakery",
  "grocery"
]

Available filter types:
pharmacy
beauty_salon
supermarket
convenience_store
drugstore

Choose for the product "white coco shampoo":
[
  "pharmacy",
  "drugstore",
  "supermarket"
]

Available filter types:
shoe_store
sporting_goods_store
department_store
supermarket
fashion_store

Choose for the product "red running shoes":
[
  "shoe_store",
  "sporting_goods_store"
]

Available filter types:
{filter_types}

Choose for the product "{product}":
"""


FILTER_TYPES_PROMPT = """
store
establishment
point_of_interest

restaurant
cafe
bakery
bar
night_club

clothing_store
convenience_store
department_store
electronics_store
furniture_store
grocery_or_supermarket
jewelry_store
liquor_store
shoe_store
shopping_mall

pharmacy
doctor
hospital
dentist
veterinary_care

movie_theater
museum
park
zoo
casino
amusement_park

bank
atm
car_rental
car_repair
car_wash
laundry

bus_station
subway_station
train_station
airport
taxi_stand

lodging
campground
rv_park
"""


def format_select_type_filters_prompt(query: str) -> str:

    prompt = SELECT_CORRECT_FILTERS.format(
        product=query, filter_types=FILTER_TYPES_PROMPT
    )

    return prompt
