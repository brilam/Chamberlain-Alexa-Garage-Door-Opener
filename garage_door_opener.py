import requests

# Endpoint URLS (the base API endpoint, login endpoint, expand account endpo
API_ENDPOINT = "https://api.myqdevice.com/api/v5/"
LOGIN_ENDPOINT = API_ENDPOINT + "/Login"
EXPAND_ACCOUNT_ENDPOINT = API_ENDPOINT + "/My?expand=account"

# This ID seems to be static
application_id = "NWknvuBd7LoFHfXmKNMBcgajXtZEgKUh4V7WNzMidrpUUluDpVYVZx+xT4PCM5Kx"

security_token = "00000000-0000-0000-0000-00000000"

login_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "br, gzip, deflate",
    "Accept-Language": "en-ca",
    "User-Agent": "Chamberlain/9273 CFNetwork/974.2.1 Darwin/18.0.0",
    "MyQApplicationId": application_id
}


authenticated_login_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "br, gzip, deflate",
    "Accept-Language": "en-ca",
    "User-Agent": "Chamberlain/9273 CFNetwork/974.2.1 Darwin/18.0.0",
    "MyQApplicationId": application_id,
    "SecurityToken": security_token,
    "Connection": "keep-alive"

}


def login(username, password):
    print("Original Security Token: " + security_token)
    login_data = {"Password": password,
                  "UserName": username}

    login_post = requests.post(url=LOGIN_ENDPOINT, json=login_data, headers=login_headers)

    # This should be logged rather than printed
    if login_post.status_code != 200:
        print("Error logging in!")
    else:
        print("Successfully logged in!")

    response = login_post.json()
    print("The security token is now: ", response["SecurityToken"])
    return response["SecurityToken"]


def update_security_token():
    authenticated_login_headers["SecurityToken"] = security_token


def get_devices_endpoint():
    account_request = requests.get(EXPAND_ACCOUNT_ENDPOINT, headers=authenticated_login_headers)

    # This should be logged rather than printed
    if account_request.status_code != 200:
        print("ERROR!")
    else:
        print("Successfully expanded account.")

    response = account_request.json()
    devices_endpoint = response["Account"]["Devices"]["href"]
    return devices_endpoint


def get_door_state(devices_endpoint):
    devices_request = requests.get(devices_endpoint, headers=authenticated_login_headers)

    # This should be logged rather than printed
    if devices_request.status_code != 200:
        print("ERROR!")
    else:
        print("Successfully reached devices endpoint.")

    response = devices_request.json()
    door_state = response["items"][0]["state"]["door_state"]
    return door_state

def is_door_open():
    return get_door_state is "closed"


security_token = login("email@email.com", "password")
update_security_token()
devices_endpoint = get_devices_endpoint()
get_door_state(devices_endpoint)
