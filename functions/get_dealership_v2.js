const config = require('./config');

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {

    const authenticator = new IamAuthenticator({ apikey: config.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    const dbname = "dealerships";
    cloudant.setServiceUrl(config.COUCH_URL);
    
	let selector = {};
    if (params.state)
        selector.state =  params.state
    if (params.id)
        selector.id = params.id;

	console.info('selector', selector);
	
    if (Object.keys(selector).length > 0)
        result = await getRecordsBySelection(cloudant, dbname, selector);
    else
        result = await getAllRecords(cloudant, dbname);

    return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(result)
    };
}

// async function dbCloudantConnect() {
// 	/* Initializes a connection to the Cloudant database using IAM authentication.*/
//     try {
// 		// Create a new instance of CloudantV1 with IAM authentication
// 		const authenticator = new IamAuthenticator({ apikey: config.IAM_API_KEY })
// 		const cloudant = CloudantV1.newInstance({
// 			authenticator: authenticator
// 		});
// 		cloudant.setServiceUrl(config.COUCH_URL);
//         console.info('Connect success! Connected to DB');

//         return cloudant;
//     } catch (err) {
//         console.error('Connect failure: ' + err.message + ' for Cloudant DB');
//         throw err;
//     }
// }

// async function main() {
// 	console.info('In Main');
// 	let db = await dbCloudantConnect();
//     return db
// }


function getAllRecords(cloudant,dbname) {
     return new Promise((resolve, reject) => {
         cloudant.postAllDocs({ db: dbname, includeDocs: true })
             .then((result)=>{
               resolve({result:result.result.rows});
             })
             .catch(err => {
                console.log(err);
                reject({ err: err });
             });
         })
}


async function getRecordsBySelection(cloudant, dbname, selector) {
    // return new Promise((resolve, reject) => {
    //     cloudant.postFind({ db: dbname, selector: selector })            
    //         .then((result)=>{
    //           resolve({result:result.result.docs});
    //         })
    //         .catch(err => {
    //            console.log(err);
    //            reject({ err: err });
    //         });
    // })
	const queryOptions = {
        selector,
    };

	const response = await cloudant.postFind({
		db: dbname, // Replace with your database name
		...queryOptions,
	});

	console.info('response', response);

	return response
}

let sampleParams = {
	"state":"California",
}

main(sampleParams)
  .then(result => {
    console.log(result);
  })
  .catch(error => {
    console.error(error);
  });

// exports main to be able to use in other class
// module.exports = main;