asdf
poetry



add typing
views.py GET and POST request
Add docstrings


 curl -X GET http://localhost:8000/insurance/quote/1/
 curl -X POST http://localhost:8000/insurance/quote/ -H "Content-Type: application/json" -d '{"buyer_name": "John Doe", "coverage_type": "Basic", "state": "California", "has_pet": true, "coverage": {"flood":true}}' 



improvements:
handle for same user multiple quotes