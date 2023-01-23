# Welcome to the project directory

To run the server, you need to type 

<!-- insert a code block -->
```bash
uvicorn app.index:app --reload
```

#### To add new routes, you need to add a new file in the app/api/v1 folder and add the route in the index.py file

#### To add new models, you need to add a new file in the app/core folder and add the model in the index.py file

#### To add new tests, you need to add a new file in the tests folder and add the test in the index.py file

#### To add new dependencies, you need to add a new file in the requirements folder and add the dependency in the index.py file

#### To add new utils, you need to add a new file in the utils folder and add the util in the index.py file

<!-- instructions for creating .env file -->
#### To create a .env file, you need to create a .env file in the root directory and add the following variables
    - MONGO_URL

Please contact [Jazlan](mailto:24100022@lums.edu.pk) for the MONGO_URL. You will ***not*** be able to connect to the DB without the URL.