## Installation

Create and activate virtual environment in project directory 

```shell
python -m venv venv
# on windows 
.\venv\Scripts\activate
# on unix 
source venv/lib/activate
```

Install dependencies from `requirements.txt`

```shell
pip3 install -r requirements.txt
```

## Run the application

Run uvicorn server and open localhost on port 8000

```
uvicorn main:app --reload
```

## Search thumbnails

```
http://localhost:8000/search/ships
```

