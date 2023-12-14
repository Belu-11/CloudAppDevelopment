/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {

  // OLD
  // const cloudant = Cloudant({
  //   url: params.COUCH_URL,
  //   plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
  // });

  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
  const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
  });
  cloudant.setServiceUrl(params.COUCH_URL);
  
  try {
    let dbList = await cloudant.getAllDbs();
    return { "dbs": dbList.result };
  } catch (error) {
      return { error: error.description };
  }
}

