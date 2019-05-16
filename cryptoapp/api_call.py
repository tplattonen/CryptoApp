import requests

# Make a get request to coinmarketcap.com
response = requests.get("https://api.coinmarketcap.com/v1/ticker/")
# Print the status code of the response.
print(response.status_code)
# Called json
coin_json = response.json()


