import SECRETS as secrets
import json
import requests as r
import datetime
import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'
    BOLD = '\033[1m'


def main():
    check_secrets()
    print(f"{bcolors.HEADER}{bcolors.BOLD}Space Facts {bcolors.ENDC}")

    iss_location = get_iss_location()
    print(f"{bcolors.BOLD}ISS Location:{bcolors.ENDC}")
    print(f"Location is {iss_location}, which is above {geo_coding(iss_location)}\n")

    print(f"{bcolors.BOLD}Nasa Picture of the day:{bcolors.ENDC}")
    print(get_nasa_picture_of_day() + '\n')

    people_in_space = get_people_in_space()
    print(f"{bcolors.BOLD}Currently there are {people_in_space[0]} people in space:{bcolors.ENDC}")
    print(people_in_space[1])

    get_photos_from_mars_rover()


# Returns a tuple of longitude and latitude
def get_iss_location():
    api_url = "http://api.open-notify.org/iss-now.json"
    location = json.loads(r.get(api_url).text)["iss_position"]
    return location["latitude"], location["longitude"]


# Returns the location of the coordinates
def geo_coding(coords):
    lat = coords[0]
    long = coords[1]
    end_point = f"http://api.positionstack.com/v1/reverse?" \
                f"access_key={secrets.position_stack_api_key}" \
                f"&query={lat},{long}"
    obj = json.loads(r.get(end_point).text)["data"][0]
    name = obj["name"]
    country = obj["country"]
    if obj["country"] is None:
        return f"the {name}"
    else:
        return f"{name} in {country}"


def get_nasa_picture_of_day():
    end_point = f"https://api.nasa.gov/planetary/apod?api_key={secrets.nasa_api_key}"
    obj = json.loads(r.get(end_point).text)
    return f"Titled: {obj['title']}\nUrl: {obj['hdurl']}"


def get_people_in_space():
    end_point = "http://api.open-notify.org/astros.json"
    obj = json.loads(r.get(end_point).text)["people"]
    formatted_string = ""
    for person in obj:
        formatted_string += f"{person['name']} in the {person['craft']}\n"
    return len(obj), formatted_string


def check_secrets():
    position_stack_url = "https://positionstack.com/"
    position_stack_end_point = f"http://api.positionstack.com/v1/forward?" \
                               f"access_key={secrets.position_stack_api_key}" \
                               f"&query=1600%20Pennsylvania%20Ave%20NW,%20Washington%20DC"

    nasa_url = "https://api.nasa.gov/"
    nasa_end_point = f"https://api.nasa.gov/planetary/apod?" \
                     f"api_key={secrets.nasa_api_key}"

    # Check keys exist
    if secrets.position_stack_api_key == "ADD POSITION STACK KEY HERE":
        print(f"{bcolors.WARNING}Please add a position stack api key\nYou can generate one here: {position_stack_url}")
        exit(1)

    if secrets.nasa_api_key == "ADD NASA API KEY HERE":
        print(f"{bcolors.WARNING}Please add a nasa api key\nYou can generate one here: {nasa_url}")
        exit(1)

    # Check if api keys are valid
    if "error" in r.get(position_stack_end_point).text:
        print(f"{bcolors.FAIL}Position Stack api key is invalid\nYou can generate one here: {position_stack_url}")
        exit(1)

    if "API_KEY_INVALID" in r.get(nasa_end_point).text:
        print(f"{bcolors.FAIL}Nasa api key is invalid\nYou can generate one here: {nasa_url}")
        exit(1)
    print(f"{bcolors.OKGREEN}Api keys are working{bcolors.ENDC}")


def get_photos_from_mars_rover():
    obj = get_photos_obj()
    print(f"{bcolors.BOLD}Photos from the {obj[0]['rover']['name']} on the date {obj[0]['earth_date']}{bcolors.ENDC}")
    sample = 5
    if len(obj) < sample:
        sample = len(obj)
    for photo in random.sample(obj, sample):
        print(f"Photo from the {photo['camera']['full_name']}: {photo['img_src']}")


def get_photos_obj():
    for i in range(0, 20):
        date_to_check = datetime.date.today() - datetime.timedelta(days=i)
        end_point = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?" \
                    f"earth_date={date_to_check}" \
                    f"&api_key={secrets.nasa_api_key}"
        obj = r.get(end_point).json()["photos"]
        if len(obj) != 0:
            return obj


if __name__ == '__main__':
    main()
