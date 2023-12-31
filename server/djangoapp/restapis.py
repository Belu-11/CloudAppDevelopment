import requests
import json
from django.conf import settings
from datetime import datetime
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


def post_request(url, json_payload, **kwargs): 
    print(kwargs)
    print("POST from {} ".format(url))
    response = {}
    params = dict()
    params['db_name'] = kwargs.get('db_name')
    params['dealer_id'] = kwargs.get('dealer_id')
    review_data = json_payload.get("review", {})
    cloudant = settings.CLOUDANT_DB
    
    if kwargs.get('db_name') == None:
        return response
    
    
    date_string = review_data["purchase_date"] # 2023-12-07
    try:
        date_object = datetime.strptime(date_string, "%Y-%m-%d")
        formatted_date = date_object.strftime("%m/%d/%Y")
    except Exception as e:
        formatted_date = date_string
        print(f"Exception while getting date occured: {e}")

    try:
        new_document: Document = Document() 
        new_document.dealership = params["dealer_id"]
        new_document.name = review_data["name"]
        new_document.purchase = review_data["purchase"]
        new_document.purchase_date = formatted_date
        new_document.car_make = review_data["car_make"]
        new_document.car_model = review_data["car_model"]
        new_document.review = review_data["review"]

        response = cloudant.post_document(
            db=params["db_name"],
            document=new_document
        ).get_result()
    except ApiException as ae:
        print("Method failed")
        print(" - status code: " + str(ae.code))
        print(" - error message: " + ae.message)
        if ("reason" in ae.http_response.json()):
            print(" - reason: " + ae.http_response.json()["reason"])
    

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


def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    db_name = kwargs.get('db_name')
    dealer_id = kwargs.get('dealer_id')

    if db_name == None and dealer_id == None:
        return result
	
    json_result = get_request(url, db_name=db_name, dealer_id=dealer_id)

    if json_result:
        reviews_doc = json_result["docs"]
        for review in reviews_doc:
            sentiment_label = str(analyze_review_sentiments(review.get("review", "")))
            date_str = review.get("purchase_date", "") 

            print(f"review {review}")

            review_obj = DealerReview(
                dealership=review.get("dealership", ""), name=review.get("name", ""), purchase=review.get("purchase", ""),
                review=review.get("review", ""), purchase_date=date_str, 
                car_make=review.get("car_make", ""), car_model=review.get("car_model", ""),
                car_year=review.get("car_year", ""), sentiment=sentiment_label, id=review.get("_id", "")
            )
            results.append(review_obj)
    return results


def analyze_review_sentiments(dealer_review):
    nlu = settings.NLU_INSTANCE
    try:
        response = nlu.analyze(
            text=dealer_review,
            features=Features(sentiment=SentimentOptions())
        ).get_result()
        print(f"sentiment {json.dumps(response)}")
        sentiment_label = response["sentiment"]["document"]["label"]
    except Exception as e:
        print(f"Error during NLU analysis: {e}")
        sentiment_label = "neutral"
    return sentiment_label


def get_dealer_carmodels(**kwargs):
    results = []
    db_name = kwargs.get('db_name')
    dealer_id = kwargs.get('dealer_id')

    if db_name == None and dealer_id == None:
        return result
	
    json_result = get_request("dealer models", db_name=db_name, dealer_id=dealer_id)

    if json_result:
        dealer_doc = json_result["docs"]
        for dealer in dealer_doc:
            dealer_obj = CarDealer(address=dealer.get("address", ""), city=dealer.get("city", ""), full_name=dealer.get("full_name", ""),
								id=dealer.get("id", ""), lat=dealer.get("lat", ""), long=dealer.get("long", ""),
								short_name=dealer.get("short_name", ""),
								state=dealer.get("state", ""), zip=dealer.get("zip", ""))
            results.append(dealer_obj)
    return results

