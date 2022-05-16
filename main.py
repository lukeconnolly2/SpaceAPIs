import SECRETS as secrets
import json
import requests as r


def main():
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


if __name__ == '__main__':
    main()
