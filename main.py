import SECRETS as secrets
import json
import requests as r


def main():
    iss_location = get_iss_location()
    print("ISS Location:")
    print(f"Location is {iss_location}, which is above {geo_coding(iss_location)}")


# Returns a tuple of longitude and latitude
def get_iss_location():
    api_url = "http://api.open-notify.org/iss-now.json"
    location = json.loads(r.get(api_url).text)["iss_position"]
    return location["latitude"], location["longitude"]


# Returns the location of the coordinates
def geo_coding(coords):
    lat = coords[0]
    long = coords[1]
    end_point = f"http://api.positionstack.com/v1/reverse?access_key={secrets.position_stack_api_key}&query={lat},{long}"
    return json.loads(r.get(end_point).text)["data"][0]["name"]


if __name__ == '__main__':
    main()
