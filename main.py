"""
Room Allotment algorithm
Given a list of room data and a list of person preferences, Allot the rooms to the people according to their preferences
as best as we can and each room has capacity of 3.

TODO:
- [ ] need to compromise between avg. room-person match and variance to make this algorithm fair
- [ ] take preferred roommates into account
- [ ] any alternative to brute force approach ?
- [ ] anything else need to be added ?
"""

# sample data
rooms_data = [
    {
        "wifi": 34,
        "privacy": 0.5,
        "sim_coverage": {
            "jio": 12,
            "airtel": 12,
            "vodafone": 12,
            "idea": 12,
            "bsnl": 12,
        },
        "floor": 1,
        "landmark_access": {
            "gym": 1,
            "mess": 20,
            "common_room": 3,
            "entrance": 23,
            "volley ball court": 1,
        }
    },
]

person_data = [
    {
        "wifi_pref": 0.8,
        "privacy_pref": 0.01,
        "sim_pref": {
            "jio": 0,
            "airtel": 0.09,
            "vodafone": 0,
            "idea": 0,
            "bsnl": 0,
        },
        "floor_pref": 0,
        "preferred_floors": [],
        "landmark_pref": {
            "gym": 0,
            "mess": 0.01,
            "common_room": 0,
            "entrance": 0.03,
            "volley ball court": 0.06,
        }
    }
]


def normalize_dict(rooms, dict_key):
    dicts = map(lambda x: x[dict_key], rooms)
    max_dict = {}
    min_dict = {}
    for dictionary in dicts:
        for key in dictionary:
            max_dict[key] = max(max_dict.get(key, False) or dictionary[key], dictionary[key])
            min_dict[key] = min(min_dict.get(key, False) or dictionary[key], dictionary[key])

    for room in rooms:
        for key in room[dict_key]:
            if (max_dict[key] - min_dict[key]) == 0:
                room[dict_key][key] = int(max_dict[key] > 0)
            else:
                room[dict_key][key] = (room[dict_key][key] - min_dict[key]) / (max_dict[key] - min_dict[key])


def normalize_rooms_data(rooms):
    # normalize wifi of rooms
    wifis = list(map(lambda x: x["wifi"], rooms))
    max_wifi = max(wifis)
    min_wifi = min(wifis)

    if (max_wifi - min_wifi) == 0:
        for room in rooms:
            room["wifi"] = int(max_wifi > 0)
    else:
        for room in rooms:
            room["wifi"] = (room["wifi"] - min_wifi) / (max_wifi - min_wifi)

    # normalize sim coverage of rooms
    normalize_dict(rooms, "sim_coverage")

    # normalize landmark_access of rooms
    normalize_dict(rooms, "landmark_access")


def compute_match(room, person):
    sim_coverage = {}
    for key in room["sim_coverage"]:
        sim_coverage[key] = room["sim_coverage"][key] * person["sim_pref"][key]
    landmark_access = {}
    for key in room["landmark_access"]:
        landmark_access[key] = room["landmark_access"][key] * person["landmark_pref"][key]

    t = {
        "wifi": room["wifi"] * person["wifi_pref"],
        "privacy": room["privacy"] * person["privacy_pref"],
        "sim_coverage": sim_coverage,
        "floor": int(room["floor"] in person["preferred_floors"]) * person["floor_pref"],
        "landmark_access": landmark_access,
    }

    return t["wifi"] + t["privacy"] + sum(t["sim_coverage"].values()) + t["floor"] + sum(t["landmark_access"].values())


normalize_rooms_data(rooms_data)

dataset = [[compute_match(room, person) for room in rooms_data] for person in person_data]
persons_per_room = 3


# checking all possible allotments
def dfs(person_index, allotment):
    if person_index == len(person_data):
        return 0, allotment

    max_allot = None
    max_match_value = -1

    for room_index in range(len(rooms_data)):
        if len(allotment[room_index]) == persons_per_room:
            continue
        allotment[person_index] += [room_index]
        match_value, a = dfs(person_index + 1, allotment.copy())
        match_value += dataset[person_index][room_index]
        if match_value > max_match_value:
            max_match_value = match_value
            max_allot = a

    return max_match_value, max_allot


empty_allotments = [[] for _ in range(len(rooms_data))]
match, allot = dfs(0, empty_allotments)
print(match)
print(allot)
