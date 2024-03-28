from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from utils.template_utils import llm_assistance_prompt, ticket_query_prompt
from app.classes.base_llm_class import BaseLLMRequirements
from app.classes.technicians_info import TechniciansInfo
from app.classes.ticket_management import TicketManagement
from utils.database_utils import technicial_skill_set
from utils.map_utils import calculate_route

import json

class LLMAssistance(BaseLLMRequirements, TicketManagement):
    def __init__(self) -> None:
        self.memory = ConversationBufferMemory(memory_key="chat_history")

    def get_prompt(self):
        return PromptTemplate(
            input_variables=["services", "query"], template=llm_assistance_prompt
        )
    
    def get_prompt_ticket_query(self):
        return PromptTemplate(
            input_variables=["query"], template=ticket_query_prompt
        )

    def get_technician_using_llm(self, question, user_lat, user_lon):
        llm_chain = LLMChain(
            llm = self.get_llm(),
            prompt = self.get_prompt()
        )
        llm_response = llm_chain({"services": technicial_skill_set,"query": question})
        retrived_technicial_skillset = llm_response["text"]

        technicians_list = self.get_nearest_technician(skill_set=retrived_technicial_skillset, user_lat=user_lat, user_lon=user_lon)
        nearest_persons = self.find_nearest_persons(latitude=user_lat, longitude=user_lon, technicians_list=technicians_list, num_persons=5)

        return nearest_persons
    
    def get_information_using_details(self, query, ticket_id):
        ticket_details = self.get_single_ticket(ticket_id)
        ticket_location = ticket_details["location"]
        
        # Check if technician is assigned to the ticket
        if "assigned_to" in ticket_details and ticket_details["assigned_to"]:
            technician_location = ticket_details["assigned_to"]["current_location"]
            origin = f"{technician_location[0]}, {technician_location[1]}"
        else:
            # Handle case when no technician is assigned
            origin = None

        destination = f"{ticket_location[0]}, {ticket_location[1]}"
        
        # Calculate route only if technician is assigned
        if origin:
            route = calculate_route(origin, destination)
            summary = route['routes'][0]['summary']
        else:
            summary = None
        
        technicians_list = self.get_nearest_technician(skill_set=ticket_details["title"], user_lat=ticket_location[0], user_lon=ticket_location[1])
        
        llm_chain = LLMChain(
            llm=self.get_llm(),
            prompt=self.get_prompt_ticket_query(),
            verbose=True,
            memory=self.memory 
        )
    
        # Ensure inputs are correctly formatted for the LLMChain
        data_to_be_sent = f"ticket_details : {ticket_details}\npath : {summary}\nother_technicians : {technicians_list}\nquery : {query}"
        inputs = {
            "query": data_to_be_sent
        }
        
        # Pass inputs to the LLMChain
        llm_response = llm_chain(inputs)
        return llm_response


