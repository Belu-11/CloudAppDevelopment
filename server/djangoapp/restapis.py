import requests
import base64
import json
from django.conf import settings
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from decouple import config
from cloudant.query import Query
from ibmcloudant.cloudant_v1 import Document
from ibm_cloud_sdk_core import ApiException
# from cloudant.client import Cloudant
# from cloudant.error import CloudantException
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    response = {}
    params = dict()
    params['db_name'] = kwargs.get('db_name')
    params['dealer_id'] = kwargs.get('dealer_id')
    params['state'] = kwargs.get('state')
    
    try:
        # Call get method of requests library with URL and parameters
		### ERROR: AUTHENTICATION IS NOT WORKING
        # response = requests.get(
		# 	url, 
		# 	params=kwargs, 
		# 	headers={'Content-Type': 'application/json'},
		# 	auth=HTTPBasicAuth('apikey', config('IAM_API_KEY')))

		## selector get string that matches column
		# response = CLOUDANT_DB.post_find(
        #     db='dealership',
        #     selector={'dealership': {'$eq': int(param_dict['dealerId'])}},
        # ).get_result()

        # Set your Cloudant credentials and database URL
        # cloudant_username = config('DB_USER')
        # cloudant_password = config('IAM_API_KEY')
        # cloudant_database = db_name
        # cloudant_url = f'https://{cloudant_username}.cloudant.com/{cloudant_database}'

        # Construct the URL for retrieving documents
        # url = f'{cloudant_url}/_all_docs'


        # Make a GET request to retrieve all documents
        # response = requests.get(url, headers=headers)
        selector = {}
        if params["dealer_id"] != None:
            selector={'id': {'$eq': int(params["dealer_id"])}}
            if params["db_name"] == 'reviews':
                selector={'dealership': {'$eq': int(params["dealer_id"])}}
        
        if params["state"] != None:
            selector = {'state': {'$eq': params["state"]}}
        
        cloudant = settings.CLOUDANT_DB
        try:
            response = cloudant.post_find(
				db=params["db_name"],
				selector=selector,
				# fields=["_id", "id", "city", "state", "lat", "long"],
				# # limit=3
			).get_result()
            
            # print(f"response {str(response)}")
        except ApiException as ae:
            print("Method failed")
            print(" - status code: " + str(ae.code))
            print(" - error message: " + ae.message)
            if ("reason" in ae.http_response.json()):
                print(" - reason: " + ae.http_response.json()["reason"])
        
        result = {
            'headers': {'Content-Type': 'application/json'},
            'statusCode': 200,
            'body': {'data': response}
        }

        # print(f"response {str(response)}")
    except Exception as e:
        print("Network exception occurred")
        print(e)

    return response


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    db_name = kwargs.get('db_name')
    if db_name == None:
        return {}
    
    json_result = get_request(url, db_name=db_name)
    
    if json_result:
        dealer_doc = json_result["docs"]
        for dealer in dealer_doc:
            dealer_obj = CarDealer(address=dealer.get("address", ""), city=dealer.get("city", ""), full_name=dealer.get("full_name", ""),
								id=dealer.get("id", ""), lat=dealer["lat"], long=dealer.get("long", ""),
								short_name=dealer.get("short_name", ""),
								state=dealer.get("state", ""), zip=dealer.get("zip", ""))
            results.append(dealer_obj)
    return results


def get_dealer_by_id(url, **kwargs):
    results = []
    db_name = kwargs.get('db_name')
    dealer_id = kwargs.get('dealer_id')
    
    if db_name == None and dealer_id == None:
        return result
	
    json_result = get_request(url, db_name=db_name, dealer_id=dealer_id)
    
    if json_result:
        dealer_doc = json_result["docs"]
        for dealer in dealer_doc:
            dealer_obj = CarDealer(address=dealer.get("address", ""), city=dealer.get("city", ""), full_name=dealer.get("full_name", ""),
								id=dealer.get("id", ""), lat=dealer.get("lat", ""), long=dealer.get("long", ""),
								short_name=dealer.get("short_name", ""),
								state=dealer.get("state", ""), zip=dealer.get("zip", ""))
            results.append(dealer_obj)
    return results


def get_dealers_by_state(url, **kwargs):
    results = []
    db_name = kwargs.get('db_name')
    state = kwargs.get('state')
    
    if db_name == None and state == None:
        return result
	
    json_result = get_request(url, db_name=db_name, state=state)
    
    if json_result:
        dealer_doc = json_result["docs"]
        for dealer in dealer_doc:
            dealer_obj = CarDealer(address=dealer.get("address", ""), city=dealer.get("city", ""), full_name=dealer.get("full_name", ""),
								id=dealer.get("id", ""), lat=dealer.get("lat", ""), long=dealer.get("long", ""),
								short_name=dealer.get("short_name", ""),
								state=dealer.get("state", ""), zip=dealer.get("zip", ""))
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    # - Call get_request() with specified arguments
    # - Parse JSON results into a DealerView object list
    results = []
    db_name = kwargs.get('db_name')
    dealer_id = kwargs.get('dealer_id')

    if db_name == None and dealer_id == None:
        return result
	
    json_result = get_request(url, db_name=db_name, dealer_id=dealer_id)

    if json_result:
        reviews_doc = json_result["docs"]
        for review in reviews_doc:
            print("---------review here 111--------")
            sentiment_label = str(analyze_review_sentiments(review.get("review", "")))
            
            review_obj = DealerReview(
                dealership=review.get("dealership", ""), name=review.get("name", ""), purchase=review.get("purchase", ""),
                review=review.get("review", ""), purchase_date=review.get("purchase_date", ""), 
                car_make=review.get("car_make", ""), car_model=review.get("car_model", ""),
                car_year=review.get("car_year", ""), sentiment=sentiment_label, id=review.get("id", "")
            )
            print("---------review here 2222--------")
            results.append(review_obj)
    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealer_review):
    print("---------seentiment 111")
    nlu = settings.NLU_INSTANCE
    print(f"dealer_review: {dealer_review}")

    try:
        response = nlu.analyze(
            text=dealer_review,
            features=Features(sentiment=SentimentOptions())
        ).get_result()
        print(f"sentiment {json.dumps(response)}")
        sentiment_label = response["sentiment"]["document"]["label"]
    except:
        sentiment_label = "neutral"
    
    print(f"sentiment label ==> {sentiment_label}")

    print("---------seentiment 222")
    return str(sentiment_label)


