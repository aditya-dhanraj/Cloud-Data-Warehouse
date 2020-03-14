# Sparkify Cloud Data Warehouse

This project extract, transform and loads 5 main informations into redshift DB from the song and event datasets(json Files) uploaded in s3 bucket:

### staging tables
- staging_events
- staging_songs

### Analytical tables
- fact_songplays
- dim_users
- dim_songs
- dim_artists
- dim_time - (timestamps breakdown into comprehensible columns)

With this structured Star Schema redshift database we can extract several insightful informations and can find several hidden patterns in listeners data.

## Objective 
You will learn Five most useful concepts from this project

* IAC(Infrastructure as Code) for AWS
* Database star schema creation - basically naive ETL process
* Building DataWarehouse in AWS
* Building ETL PipeLine for cloud database using python.
* HandsOn for Redshift DB

# Running the Project
First you must enter the required Details in config (dwh.cfg) file:

    [AWS]
    key = <Your AWS user ID>
    secret = <AWS secret Key>
    
Run All the steps involved in **cluster_creation.ipynb** :
    
    check your AWS account : the Redshift cluster is Available now and DB is connected...

Now create required tables in redshift, by doing :
    
    python3 create_tables.py
    
After Creation load data into tables through etl script, by doing :

    python3 etl.py
 
Check your results by running analytical queries :

    python3 results.py

Finally run last 3 steps of **cluster_creation.ipynb** to close redshift cluster and delete IAM Role and Policies.

# Database Schema

The schema used for this exercise is the Star Schema: " One Fact Table surround by 4 Dimension Table "

[Database Schema!](img/StarSchema.PNG "Star Schema")

## The project file structure

We have a small list of files, easy to maintain and understand the Concept:

**sql_queries.py**         -  Contains all your sql queries to use throughout the ETL process 
**create_tables.py**       -  File reponsible to create the schema structure/tables into the redshift database
**etl.py**                 -  Reads and processes files from song_data and log_data stored in s3, and load them into the 
                              staging tables. Finally data will load from staging tables to analytical tables.
**cluster_creation.ipynb** -  The python notebook that was written to develop the logic behind the etl.py process.
**results.py**             -  Displays the Total count of rows of each table, to certify if our ETL process was being
                              successful (or not).
**dwh.cfg**                -  Contains all AWS and DB configuration details and S3 bucket location.

## Author
**Aditya Dhanraj** - [Linkedin Profile](https://www.linkedin.com/in/aditya-dhanraj).