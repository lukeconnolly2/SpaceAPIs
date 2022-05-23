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

    get_space_news()

    print_earth_image()


# Returns a tuple of longitude and latitude
def get_iss_location():
    api_url = "http://api.open-notify.org/iss-now.json"
    location = json.loads(r.get(api_url).text)["iss_position"]
    return location["latitude"], location["longitude"]


# Returns the location of the coordinates
def geo_coding(coords):
    lat, long = coords
    end_point = f"http://api.positionstack.com/v1/reverse?" \
                f"access_key={secrets.position_stack_api_key}" \
                f"&query={lat},{long}"
    obj = r.get(end_point).json()["data"][0]
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


def get_earth_image_object():
    date = datetime.date.today()

    end_point = f" https://api.nasa.gov/EPIC/api/natural/" \
                f"date/{date}" \
                f"?api_key={secrets.nasa_api_key}"

    obj = r.get(end_point).json()

    if len(obj) == 0:
        date = datetime.date.today() - datetime.timedelta(1)
        end_point = f" https://api.nasa.gov/EPIC/api/natural/" \
                    f"date/{date}" \
                    f"?api_key={secrets.nasa_api_key}"
        obj = r.get(end_point).json()

    sample = 3

    if len(obj) < sample:
        sample = len(obj)

    list_of_photos = []
    list_coords = []
    for photo in random.sample(obj, sample):
        list_coords.append(photo["coords"]["centroid_coordinates"])
        list_of_photos.append(photo["image"])

    return date, list_of_photos, list_coords


def print_earth_image():
    date, list_of_photos, list_coords = get_earth_image_object()

    print(f"\n{bcolors.BOLD}Photos of Earth taken on {date} from the ISS :{bcolors.ENDC}")

    for img, coords in zip(list_of_photos, list_coords):
        url = f"https://epic.gsfc.nasa.gov/archive/natural" \
              f"/{date.year}/{date.month:02d}/{date.day}" \
              f"/png" \
              f"/{img}.png"
        print(f"{url}")
        print(f"This photo was taken over {geo_coding(coords.values())}")


def get_space_news():
    url = "https://space-news.p.rapidapi.com/news/guardian"

    headers = {
        "X-RapidAPI-Host": "space-news.p.rapidapi.com",
        "X-RapidAPI-Key": "67167d2a9cmshc58048f31e25f90p1e5d4cjsn132ef897bf0f"
    }

    obj = r.request("GET", url, headers=headers).json()
    print(obj)

    news = 3
    if len(obj) / 2 < news:
        news = len(obj)
    print(f"\n{bcolors.HEADER}{bcolors.BOLD}{news} Pieces of Space News!{bcolors.ENDC}\n")
    for news in random.sample(obj[::2], news):
        print(f"{bcolors.BOLD}{news['title'].strip()}  : \n{news['url'].strip()}{bcolors.ENDC} \n")



if __name__ == '__main__':
    main()
