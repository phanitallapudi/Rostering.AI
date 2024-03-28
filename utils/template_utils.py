

llm_assistance_prompt = """You are an analyst for a company which provides various services like mentioned below,
here is a list of services available : {services}

Now your task is to analyze the query of the customer and return the appropriate service which will fullfill the customer neeed
here is the query of the customer : {query}

You just need to return the service name and nothing else needed, for example if the appropriate services for the query is customer services then you need to return the answer like mentioned below

customer services
"""

ticket_query_prompt = """You need to analye the ticket information which is given below and return the response for the query
Here is the nessesary details which you want to process : {query}

Now take a deep breathe and generate the appropriate response for the query.
"""