import requests
import json

# Endpoint URLS (the base API endpoint, login endpoint, expand account endpo
API_V5_ENDPOINT = "https://api.myqdevice.com/api/v5/"
API_V51_ENDPOINT = "https://api.myqdevice.com/api/v5.1/"
LOGIN_ENDPOINT = API_V5_ENDPOINT + "Login"
EXPAND_ACCOUNT_ENDPOINT = API_V5_ENDPOINT + "/My?expand=account"
GARAGE_DOOR_DEVICE_INDEX = 0

# This ID seems to be static
application_id = "NWknvuBd7LoFHfXmKNMBcgajXtZEgKUh4V7WNzMidrpUUluDpVYVZx+xT4PCM5Kx"

security_token = "00000000-0000-0000-0000-00000000"
# security_token = "83c3aae2-1e6d-43b6-9100-6f9db39fddd5"

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
    "Connection": "keep-alive",
    "Content-Type": "application/json"
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

    # Form your own device endpoint URL rather than get it from ["Devices"]["href"] since that has a URL to v5 API
    return API_V51_ENDPOINT + "/Accounts/" + response["Account"]["Id"] + "/Devices"


def get_door_state(devices_endpoint):
    devices_request = requests.get(devices_endpoint, headers=authenticated_login_headers)

    # This should be logged rather than printed
    if devices_request.status_code != 200:
        print("ERROR!")
    else:
        print("Successfully reached devices endpoint.")

    response = devices_request.json()
    door_state = response["items"][GARAGE_DOOR_DEVICE_INDEX]["state"]["door_state"]
    return door_state


def is_door_closed(devices_endpoint):
    return get_door_state(devices_endpoint) == "closed"


def is_door_opening(devices_endpoint):
    return get_door_state(devices_endpoint) == "opening"


def is_door_closing(devices_endpoint):
    return get_door_state(devices_endpoint) == "closing"


def get_device_sn_endpoint(devices_endpoint):
    devices_request = requests.get(devices_endpoint, headers=authenticated_login_headers)

    # This should be logged rather than printed
    if devices_request.status_code != 200:
        print("ERROR!")
    else:
        print("Successfully reached devices endpoint.")

    response = devices_request.json()
    device_sn = response["items"][GARAGE_DOOR_DEVICE_INDEX]["serial_number"]
    device_sn_endpoint = devices_endpoint + "/" + device_sn
    return device_sn_endpoint


def do_door_action(devices_endpoint, door_action):
    device_sn_endpoint = get_device_sn_endpoint(devices_endpoint)

    actions_endpoint = device_sn_endpoint + "/actions"
    print("The actions endpoint is:", actions_endpoint)

    if is_door_opening(devices_endpoint):
        print("Please wait. The garage door is opening.")
        return
    elif is_door_closing(devices_endpoint):
        print("Please wait. The garage door is closing.")
        return

    # If the door action is open, open the garage door if it is closed
    if door_action == "open":
        if is_door_closed(devices_endpoint):
            open_data = {"action_type" : door_action}
            open_door_request = requests.put(actions_endpoint, headers=authenticated_login_headers, data=json.dumps(open_data))
            # This should be logged rather than printed
            if open_door_request.status_code == 204:
                print("Opening the garage door")
            else:
                print("Error opening the garage door")
    # If the door is close, close the garage door if it is open
    elif door_action == "close":
        if is_door_closed(devices_endpoint) is False:
            close_data = {"action_type": door_action}
            close_door_request = requests.put(actions_endpoint, headers=authenticated_login_headers, data=json.dumps(close_data))
            # This should be logged rather than printed
            if close_door_request.status_code == 204:
                print("Closing the garage door")
            else:
                print("Error closing the garage door")


if __name__ == "__main__":
    # Just some sample code to illustrate how this works (login, open and close)
    security_token = login("email@email.com", "password")
    update_security_token()
    devices_endpoint = get_devices_endpoint()
    get_door_state(devices_endpoint)
    do_door_action(devices_endpoint, "open")
    do_door_action(devices_endpoint, "close")
