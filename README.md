# musical-broccoli
UMT Coding Assignment - URL Shortener

This is a URL Shortening service written in Python using Flask and SQLAlchemy.

## Setup/Installation
1) Clone repo ```git clone https://github.com/ishan22/musical-broccoli.git```
2) Run ```pip install -r requirements.txt``` to install necessary libraries


## To Run
1) Run ```python3 main.py``` to build and start server on ```http://127.0.0.1:5000```

    ### To Shorten a URL
    1) Make a POST request of the following schema
        ```{'url': '<insert url to shorten here>'}```
        **Example Request:** 
        ```curl -X POST http://127.0.0.1:5000/shortenUrl -H "Content-Type: application/json" -d '{"url": "https://news.unitedmasters.com/blog/brent-faiyaz-billboard"}'```
        **Example Response:** 
        ```{ "shortened_url" : "http://127.0.0.1:5000/BlQBJh"}```

        #### How do I use the URL??
        To use a shortened URL simply enter the shortened URL path into the
        browser and it will redirect you to the original page.
    


