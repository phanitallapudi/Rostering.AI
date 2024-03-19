from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from utils.template_utils import llm_assistance_prompt
from app.classes.base_llm_class import BaseLLMRequirements
from app.classes.technicians_info import TechniciansInfo
from utils.database_utils import technicial_skill_set


class LLMAssistance(BaseLLMRequirements, TechniciansInfo):
    def __init__(self) -> None:
        pass

    def get_prompt(self):
        return PromptTemplate(
            input_variables=["services", "query"], template=llm_assistance_prompt
        )

    def get_technician_using_llm(self, question, user_lat, user_lon):
        llm_chain = LLMChain(
            llm = self.get_llm(),
            prompt = self.get_prompt()
        )
        llm_response = llm_chain({"services": technicial_skill_set,"query": question})
        retrived_technicial_skillset = llm_response["text"]

        technicians_list = self.get_nearest_technician_skillset(skill_set=retrived_technicial_skillset, user_lat=user_lat, user_lon=user_lon)
        nearest_persons = self.find_nearest_persons(latitude=user_lat, longitude=user_lon, technicians_list=technicians_list, num_persons=5)

        return nearest_persons

