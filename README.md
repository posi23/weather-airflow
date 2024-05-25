# weather-airflow
"Weather-Airflow" is a data pipeline solution designed to fetch weather reports from the openweathermap API for specified cities. This data is then meticulously transformed into a user-friendly format, ensuring easy comprehension. Leveraging the power of Airflow, this pipeline is orchestrated and managed efficiently, guaranteeing seamless execution and scheduling.

Built with Python scripts, the entire application is encapsulated within Docker containers, ensuring portability and consistency across environments. Upon transformation, the data is securely stored in a designated S3 bucket in the widely accessible '.csv' file format, facilitating easy access and analysis.

With a focus on scalability, reliability, and maintainability, "Weather-Airflow" streamlines the process of gathering and processing weather data, making it an indispensable tool for any data-driven application or analysis workflow.

**Steps on how to run this project:**
1. Run *./build-image.sh* on your terminal.
2. Create an .env file in the root directory of the project.
    - Populate the *.env* file with all these variables:
        - POSTGRES_USER=<your_postgres_username>
        - POSTGRES_PASSWORD=<your_postgres_password>
        - IMAGE_PREFIX=<any_prefix_of_your_choice> (This will be the prefix that would be appended to the name of the image to be built e.g. if *IMAGE_PREFIX=posi*, the image name will be *posi-airflow:latest*)
        - AWS_ACCESS_KEY_ID=<your_aws_access_key_id>
        - AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key>
        - AWS_DEFAULT_REGION=<your_aws_default_region> (e.g. ca-central-1)
        - AWS_S3_BUCKET_NAME=<your_aws_s3_bucket_name> (Make sure to have created this s3 bucket in your AWS account under the region that would be used for the above variable)
        - WEATHERMAP_API_KEY=<your_weathermap_api_key> (See section below for details on how to obtain this)
        - WEATHERMAP_CITY=<city_to_query> (This is the city that the weathermap api will query and display weather results for. Make sure to capitalize the first letter)
        - AIRFLOW_USERNAME=<your_airflow_username> (This would be the username that would be used to login to the Airflow UI)
        - AIRFLOW_PASSWORD=<your_airflow_password> (This would be the password that would be used to login to the Airflow UI)
        - AIRFLOW_FIRSTNAME=<your_airflow_firstname> (This would be the first name that would be associated with your Airflow UI account)
        - AIRFLOW_LASTNAME=<your_airflow_lastname> (This would be the last name that would be associated with your Airflow UI account)
        - AIRFLOW_EMAIL=<your_airflow_email_address> (This would be the email address that would be associated with your Airflow UI account)  
3. Run *docker compose up -d* on your terminal
4. Go to http://localhost:8000 and sign in to Airflow using your airflow username and airflow password
5. Search for *weather_dag* under *DAGs* in the Airflow UI
6. Play/Start/Run the DAG.
7. Once successful, go to your AWS S3 console, under your bucket used, check the for the new csv files created from this application.


**Steps on getting *your_weathermap_api_key***