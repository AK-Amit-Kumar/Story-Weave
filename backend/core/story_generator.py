from sqlalchemy.orm import Session
from core.config import settings

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.models import StoryLLMResponse, StoryNodeLLM
# WE will get response as string from LLM and then we will pipe it
# into class PydanticOutputParser (for parsing all the data LLm is giving us )

from core.prompts import  STORY_PROMPT
from models.story import Story  # for saving the story


# **------here we will call AI model which will generate the story
class StoryGenerator:

    @classmethod
    def _get_llm(cls):
        return ChatOpenAI(model="gpt-4-turbo")

    # for generating the story
    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy")-> Story:
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

        prompt = ChatPromptTemplate([
            (
                "system",
                STORY_PROMPT
            ),  # system message
            (
                "human",
                f"Create the story with this theme: {theme}"
            )
        ]).partial(format_instructions=story_parser.get_format_instructions())

        raw_response = llm.invoke(prompt.invoke({}))

        response_text = raw_response
        if hasattr(raw_response, "content"):
            response_text = raw_response.content

        story_structure = story_parser.parse(response_text)

        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()    # it will update the story db object with all the automatically populated field like id of the story


        # this is to validate if our root node is in dict format, then is it in correct format of our root node
        # Basically we are getting llm response in JSON - so we are making sure if it is correct dictionary format mentioned in StoryNodeLLM
        # then making sure that this data is moved to python object through pydantic object
        root_node_data = story_structure.rootNode
        if isinstance(root_node_data, dict):
           root_node_data = StoryNodeLLM.model_validate(root_node_data)


        # todo: process data
        db.commit()
        return story_db

    @classmethod


















