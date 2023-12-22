// import * as data from './creds-sample.json';
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
// const Cloudant = require('@cloudant/cloudant');
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

const config = require('./config');


// async function main(params) {
// 	const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
// 	const cloudant = CloudantV1.newInstance({
// 		authenticator: authenticator
// 	});
// 	cloudant.setServiceUrl(params.COUCH_URL);
	
// 	try {
// 	  let dbList = await cloudant.getAllDbs();
// 	  return { "dbs": dbList.result };
// 	} catch (error) {
// 		return { error: error.description };
// 	}
// }


// Initialize Cloudant connection with IAM authentication
// async function dbCloudantConnect() {
//     try {
//         const cloudant = Cloudant({
//             plugins: { iamauth: { iamApiKey: '' } }, // Replace with your IAM API key
//             url: '', // Replace with your Cloudant URL
//         });
//         const db = cloudant.use('dealerships');
//         console.info('Connect success! Connected to DB');
//         return db;
//		   The cloudant.use method is specific to the older version of the @cloudant/cloudant library. In the updated version (@ibm/cloudant), you don't need to use the use method.
//     } catch (err) {
//         console.error('Connect failure: ' + err.message + ' for Cloudant DB');
//         throw err;
//     }
// }

async function dbCloudantConnect() {
	/* Initializes a connection to the Cloudant database using IAM authentication.*/
    try {
		// Create a new instance of CloudantV1 with IAM authentication
		const authenticator = new IamAuthenticator({ apikey: config.IAM_API_KEY })
		const cloudant = CloudantV1.newInstance({
			authenticator: authenticator
		});
		cloudant.setServiceUrl(config.COUCH_URL);
        console.info('Connect success! Connected to DB');

		// const db = cloudant.use('dealerships');
		// The cloudant.use method is specific to the older version of the @cloudant/cloudant library. In the updated version (@ibm/cloudant), you don't need to use the use method.
        return cloudant;
    } catch (err) {
        console.error('Connect failure: ' + err.message + ' for Cloudant DB');
        throw err;
    }
}

let db;

(async () => {
	// Initialize the Cloudant connection on application startup
    db = await dbCloudantConnect();
})();

/* Express Middleware: 
	This line adds middleware to parse JSON requests. 
	It allows the application to handle JSON-encoded data.
*/
app.use(express.json());


app.get('/', (req, res) => {
    res.send('Welcome to the Dealerships API');
});

// Define a route to get all dealerships with optional state and ID filters
// app.get('/dealerships/get', (req, res) => {
//     const { state, id } = req.query;

//     // Create a selector object based on query parameters
//     const selector = {};
//     if (state) {
//         selector.state = state;
//     }
    
//     if (id) {
//         selector.id = parseInt(id); // Filter by "id" with a value of 1
//     }

//     const queryOptions = {
//         selector,
//         limit: 10, // Limit the number of documents returned to 10
//     };

//     db.find(queryOptions, (err, body) => {
//         if (err) {
//             console.error('Error fetching dealerships:', err);
//             res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
//         } else {
//             const dealerships = body.docs;
//             res.json(dealerships);
//         }
//     });
// });


/*
	Define a route to get all dealerships with optional state and ID filters
	
	Defines a route for "/dealerships/get" that handles GET requests.
	Retrieves optional query parameters (state and id) from the request.
	Creates a selector object based on the query parameters.
	Uses the Cloudant postFind method to perform a find operation with the specified query options.
	Handles the response by sending the retrieved dealerships as JSON or an error response if there's an issue.
*/
app.get('/dealerships/get', async (req, res) => {
    const { state, id } = req.query;

    // Create a selector object based on query parameters
    const selector = {};
    if (state) {
        selector.state = state;
        console.info('selector state ==>', selector);
    }
    
    if (id) {
        selector.id = parseInt(id); // Filter by "id" with a value of 1
        console.info('selector id ==>', selector);
    }

    const queryOptions = {
        selector,
        limit: 10, // Limit the number of documents returned to 10
    };

	try {
        const response = await db.postFind({
            db: 'dealerships', // Replace with your database name
            ...queryOptions,
        });

		const dealerships = response.result.docs;
        res.json(dealerships);
    } catch (err) {
        console.error('Error fetching dealerships:', err);
        res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
    }
});


app.get('/api/dealership', async (req, res) => {
    const { state, id } = req.query;

    const selector = {};
    if (state) {
        selector.state = state;
    }
    
    if (id) {
        selector.id = parseInt(id);
    }

    const queryOptions = {
        selector,
        // limit: 10, // Limit the number of documents returned to 10
    };

	try {
        const response = await db.postFind({
            db: 'dealerships',
            ...queryOptions,
        });

		const dealerships = response.result.docs;
        res.json(dealerships);
    } catch (err) {
        console.error('Error fetching dealerships:', err);
        res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
    }
});

app.get('/api/review', async (req, res) => {
    const { dealerId } = req.query;

    // Create a selector object based on query parameters
    const selector = {};
    if (dealerId) {
        selector.dealership = parseInt(dealerId); // Filter by "id" with a value of 1
    }

    const queryOptions = {
        selector,
        // limit: 10, // Limit the number of documents returned to 10
    };

	try {
        const response = await db.postFind({
            db: 'reviews',
            ...queryOptions,
        });

		const reviews = response.result.docs;
        res.json(reviews);
    } catch (err) {
        console.error('Error fetching dealerships:', err);
        res.status(500).json({ error: 'An error occurred while fetching reviews.' });
    }
});


/*
	Starts the Express server, listening on the specified port.
*/
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});