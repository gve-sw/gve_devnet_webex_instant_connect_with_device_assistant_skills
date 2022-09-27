# Scripts

This directory contains scripts to start a local Mongo DB server and initialize it with data. Below you'll find a short description of each script and how to use it.

**Note**: You must have Mongo DB installed and configured on your local machine for these scripts to work. 

## Bash Scripts

There are two bash scripts to start and stop a local Mongo DB server:

* To start the server run `bash mongo-start.sh`
* To stop the server run `bash mongo-stop.sh`

Once the server is running, use the command `mongo` to access the Mongo Shell. Here's a guide on how to intereact with the Mongo Shell: [Mongo Shell Quick Reference](https://www.mongodb.com/docs/v4.4/reference/mongo-shell/).

## Python Scripts

There are two python scripts; one to initialize the DB with data, and one to clear the data in the DB:

* To initialize the DB with data, run the command `python3 init_db.py`
* To clear the data in the DB, run the command `python3 clear_db.py`

**Note**: The initial data can be found in the files `patient_data.py` and `provider_data.py`.