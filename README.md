# Car Dealership Application
This project is the final submission for the "Full Stack Cloud Application Development" course offered by IBM. The Car Dealership Application is a comprehensive solution that covers user management, dynamic pages, and backend services. It leverages IBM Cloud services and integrates the Watson Natural Language Understanding API to analyze user comments' sentiment.

All the high-level steps are listed below:
**Prework: Sign up for IBM Cloud account and create a Watson Natural language Understanding service**
1. Create an IBM cloud account if you don't have one already.
2. Create an instance of the Natural Language Understanding (NLU) service.

**Fork the project Github repository with a project then build and deploy the template project**
1. Fork the repository in your account
2. Clone the repository in the theia lab environment
3. Create static pages to finish the user stories
4. Deploy the application on IBM Cloud

**Add user management to the application**
1. Implement user management using the Django user authentication system.
2. Set up continuous integration and delivery

**Implement backend services**
1. Create cloud functions to manage dealers and reviews
2. Create Django models and views to manage car model and car make
3. Create Django proxy services and views to integrate dealers, reviews, and cars together
 
**Add dynamic pages with Django templates**
1. Create a page that shows all the dealers
2. Create a page that show reviews for a selected dealer
3. Create a page that let's the end user add a review for a selected dealer

**Containerize your application**
1. Add deployment artifacts to your application
2. Deploy your application


## Dependencies
Install the required dependencies using the following commands:

navigate to the 'server' flder and run: python3 -m pip install -U -r requirements.txt
pip install --upgrade cloudant
pip install --upgrade "ibmcloudant>=0.0.27"

After installing dependencies, perform migration by executing the following commands:
python3 manage.py makemigrations
python3 manage.py migrate
Environment Variables

To maintain security and protect sensitive information, this project uses environment variables. Ensure that you set the following environment variables and make sure to configure these environment variables before running the application:

SECRET_KEY: Secret key for Django application
DB_NAME: Cloudant name
DB_USER: Cloudant database username
DB_PASSWORD: Cloudant database password
DB_HOST: Cloudant database host
COUCH_URL: cloudant database url
IAM_API_KEY: Cloudant database API key
COUCH_USERNAME: Cloudant datase unique username

NLU_API_KEY: API key for Watson Natural Language Understanding
NLU_URL: URL for Watson Natural Language Understanding API
BASE_URL: Base URL for Watson Natural Language Understanding API


## Usage
To run the Car Dealership Application, use the following command:
python3 manage.py runserver
This will start the development server, and you can access the application by navigating to http://localhost:8000/ in your web browser.

## Contributions
Contributions to this project are welcome. If you find any issues or have suggestions for improvement, please create a new issue or submit a pull request.

## License
This project is licensed under the terms of the LICENSE file. Feel free to use and modify the code as needed.
