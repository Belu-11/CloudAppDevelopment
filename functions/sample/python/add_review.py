"""
IBM Cloud Functions action.
This function adds a review to the Cloudant database.
"""

from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def main(param_dict):
    """Add a review to the Cloudant database"""
    authenticator = IAMAuthenticator(param_dict["IAM_API_KEY"])
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(param_dict["COUCH_URL"])

    new_review = client.post_document(
        db="reviews", document=param_dict["review"])
    if new_review.exists():
        result = {
            "headers": {"Content-Type": "application/json"},
            "body": {"message": "Review posted successfully."}
        }
        print(new_review)
        return result
    error_json = {
        "statusCode": 500,
        "message": "Could not post review due to server error."
    }
    return error_json