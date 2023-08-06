# sign_in_app
Unofficial Python library for the [Sign In App API](https://backend.signinapp.com/client-api/docs/1.0/overview).

Before you do anything, you'll need to create a client for the Sign In App's API on their website.

Next, install the sign-in-app library.
```bash
pip install sign-in-app
```

Then you can use the boiler plate code below to interact with the API.

 ## Create API object
```python
def create_api_obj():
	from sign_in_app.sign_in_app import sign_in_app
	
	#These options match up with the terminology of the Sign In App.
	#Once you've created your client, it should be straight forward.
	
	base_url="your_base_url"
	client_key="your_client_key"
	connection_name="your_connection_name"
	secret_key="your_secret_key"
	
	#Instructs which sites to look at. You will need to specify this.
	# Locate Site IDs:
	#	Go to Manage
	#	Click on Sites
	#	Click on a site and check out the URL. There will be an ID there.
	
	site_ids=[1,2,3]#list of integers

	#Instructs which user groups to look at. You will need to specify this.
	# Locate Group IDs:
	#	Go to Manage
	#	Click on Groups
	#	Click on a group and check out the URL. There will be an ID there.
	
	group_ids=[1,2,3]#list of integers

	#Create api object.
	api=sign_in_app(
		site_ids=site_ids,
		base_url=base_url,
		connection_name=connection_name,
		client_key=client_key,
		secret_key=secret_key,
		group_ids=group_ids
		)
  ```
  
    
  ## Visitor Objects
  ### Once you've created an api object, you can call functions with it to return lists of visitor objects.
  ### The visitor object has these attributes available:
  
  ```python
  {
  #These are parent objects for the visitor object.
  'site': <sign_in_app.site object at 0x01EC62C8>, 
  'sign_in_app': <sign_in_app.sign_in_app object at 0x01EA0C10>, 
  
  #This is the data the API returns.
  'id': some_integer, #This is the id for the visit.
  'group_id': some_integer, 
  'returning_visitor_id': some_integer, #This is basically the user's ID.
  'name': "Someone's Full Name", 
  'photo_url': None, 
  'badge_url': None, 
  'status': 'signed_in', 
  'in_datetime': '2021-04-29T13:39:57Z', 
  'out_datetime': None, 
  'expected_datetime': None, 
  'additional_fields': {"Question 1":"Answer", "Question 2", "Answer"}, 
  'role': None, 
  'email': 'somebody@domain.com', 
  'mobile': None, 
  'c3YQ5d9wQi': "User's Department", 
  'fQHRUCmOKz': "User's Job Title", 
  'rejected_sign_in': False, 
  
  #Custom fields added for convenience. Any suggestions, please get in contact.
  
  #In and Out times converted to your local timezone. You can specify this timezone if needed.
  'in_datetime_local': datetime.datetime(2021, 4, 29, 9, 39, 57, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000), 'Eastern Daylight Time')), 
  'out_datetime_local': None,  
  }
  
  ```
   
   
## The library can give you today's data, or search historical data. Examples below.
   
   
 ### get_today

 ```python
visitors=api.get_today()
for visitor in visitors:
	print(visitor.__dict__)
  ```


 ### get_history
 #### Accurate to the day.

 ```python
from datetime import datetime, timedelta
start_date=datetime.now()-timedelta(days=7)
end_date=datetime.now()
app_obj.get_history(start_date, end_date)
  ```
