# pycrowdspider

#### Description
every one whole use the program can collect data from websites fast, and also help other to collect data. 

#### Software Architecture
Software architecture description

###  MongoDB
#### backup(run in the root directory of the project)
    mongodump -h 127.0.0.1 -d py_crowd_spider -o mongodb
#### restore(run in the root directory of the project)
    mongorestore -h 127.0.0.1 -d mongodb/py_crowd_spider
#### mongoexport
    mongoexport -h 127.0.0.1 -d py_crowd_spider -c proxies -o D:/proxies.json
#### mongoimport
     mongoimport --db py_crowd_spider --collection proxies --file D:/proxies.json
#### freeze
pip freeze > requirements.txt

#### Installation

1. pip install -r requirements.txt
2. download Tesseract: https://github.com/tesseract-ocr/tesseract/wiki
3. 

