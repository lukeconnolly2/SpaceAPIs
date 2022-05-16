import SECRETS as secrets
import json
import requests as r


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    check_secrets()
    iss_location = get_iss_location()
    print("ISS Location:")
    print(f"Location is {iss_location}, which is above {geo_coding(iss_location)}\n")

    print("Nasa Picture of the day:")
    print(get_nasa_picture_of_day())


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
        print(f"{bcolors.WARNING}Position Stack api key is invalid\nYou can generate one here: {position_stack_url}")
        exit(1)

    if "API_KEY_INVALID" in r.get(nasa_end_point).text:
        print(f"{bcolors.WARNING}Nasa api key is invalid\nYou can generate one here: {nasa_url}")
        exit(1)


if __name__ == '__main__':
    main()
