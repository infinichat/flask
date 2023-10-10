##########################################
###### Automatically upload new data   #######
#### Development Started 23.09.23 ####
### Author: Anzhelika Bielintseva ###
##  Org: Shibot                ##
#########################################

import os
import requests
import schedule
import time
import concurrent.futures

API_URL = "http://localhost:3000/api/v1/prediction/9b576a1b-66ec-4d47-97c5-d53842072d39"
product_url = 'https://openapi.keycrm.app/v1/products'
offer_url = 'https://openapi.keycrm.app/v1/offers'
statement = "Ви можете зв'язатись з нами за такими контактим менеджера Viber, Telegram +380 98 764 54 44. Умови доставки: доставляємо на протязі 2 днів. Повернення товару в перші 14 днів після замовлення. Доставка здійснюється Новою Поштою. Компанія Gamanzi - це вибір справді якісних гаманців з дизайном, які довго прослужать вам. Ми існуємо вже 3 роки та за цей час багато людей встигли придбати наші товари."
params = {}

api_key = 'ZjBjNDFhN2M4YjJjNjM5NzU1MGVhMTcxZjhjYzNhNDU3ZTAwMTIwMA'

headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

def query(payload):
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        json_response = response.json()
        return json_response
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except ValueError as e:
        print(f"JSON decoding error: {e}")
        return None
    
def get_offer_details(product_id, filename):
    try:
        offer_params = {'filter[product_id]': product_id}
        offer_response = requests.get(offer_url, params=offer_params, headers=headers)
        offer_response.raise_for_status()
        offer_data = offer_response.json()
        
        # Append offer data to the specified file
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(f'Offer details for product ID {product_id}:\n')
            file.write(str(offer_data))
            file.write('\n\n')
    except requests.exceptions.RequestException as e:
        print(f'Error getting offer details for product ID {product_id}:', e)

def execute_query(url, filename):
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()

        with open(filename, 'a', encoding='utf-8') as file:
            file.write(str(statement))
            file.write(str(data))
            file.write('\n\n')

        for product in data.get('data', []):
            quantity = product.get('quantity', 0)
            product['availability'] = quantity > 0

            if 'has_offers' in product and product['has_offers']:
                product_id = product.get('id')
                get_offer_details(product_id, filename)

        print(f'Response from {url} appended to {filename}')
    except requests.exceptions.RequestException as e:
        print(f'Error for {url}:', e)

# Create a ThreadPoolExecutor to run the requests concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit(execute_query, product_url, 'response.txt')

output = query({
    "question": "які умови доставки",
})

if output is not None:
    print("Query executed successfully.")
    print("API Response:")
    print(output)
else:
    print("Query failed.")

# Schedule the job to run at a specific time (e.g., 11:05 AM)
schedule.every().day.at("12:08").do(execute_query, offer_url, 'response.txt')

# Run the scheduling loop
while True:
    schedule.run_pending()
    time.sleep(1)










