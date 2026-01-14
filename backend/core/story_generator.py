from sqlalchemy.orm import Session
# from core.config import settings   # commented as we are using load_dotenv for fetching api_key

# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.models import StoryLLMResponse, StoryNodeLLM
# WE will get response as string from LLM, and then we will pipe it
# into class PydanticOutputParser (for parsing all the data LLm is giving us )

from core.prompts import  STORY_PROMPT
from models.story import Story, StoryNode  # for saving the story - used in generate_story method
# importing StoryNode - for conversion of received JSON LLm response into Python data type for db storage

# for importing api_key value into the core logic
from dotenv import load_dotenv

load_dotenv()


# **------here we will call AI model which will generate the story
class StoryGenerator:    ## we are writing class here to organize the function mainly

    @classmethod
    def _get_llm(cls):      #_ means private method
        # return ChatOpenAI(model="gpt-4-turbo")
        # return ChatOpenAI(model="gpt-4o-mini")
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    # for generating the story
    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy")-> Story:
        llm = cls._get_llm()

        # below we are passing pydantic model defined into pydanticOutputParser
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                STORY_PROMPT
            ),  # system message
            (       #user message
                "human",
                f"Create the story with this theme: {theme}"
            )
        ]).partial(format_instructions=story_parser.get_format_instructions())

        # get_format_instructions() - it make sure we are getting the response in string and follows the format instructions
        # mention in prompts.py
        raw_response = llm.invoke(prompt.invoke({}))  # invoking the llm with defined prompt variable


        response_text = raw_response
        if hasattr(raw_response, "content"):   # checking if received the response has "content" attribute - MINOR VALIDATION
            response_text = raw_response.content

        # making sure story_structure is aligned with "class StoryLLMResponse(BaseModel)' structure
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

        #calling _process_story_node for processing the received LLM data into database acceptable format
        cls._process_story_node(db, story_db.id, root_node_data,is_root=True)

        db.commit()
        return story_db

    #class method which will go through all the data that we received from LLM and
    #convert it to into a correct python data type because -->
    # data got from LLM - json format
    # data storage allowed in db - python data type format
    # conversion of json format to python data type format takes place in below function
    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool=False ) -> StoryNode:
        #calling this function RECURSIVELY using is_root as base condition
        # below we are going take infor from StoryNodeLLM type node to StoryNode type node
        #     ROOT NODE ----
        node = StoryNode(
            # story_id=story_id,
            # content=node_data.content if hasattr(node_data, "content") else node_data["content"],
            # is_root=is_root,
            # is_ending=node_data.is_Ending if hasattr(node_data, "is_Ending") else node_data["is_Ending"],
            # is_winning_ending=node_data.isWinningEnding if hasattr(node_data, "isWinningEnding") else node_data["isWinningEnding"],
            # options=[]
            story_id=story_id,
            content=node_data.content,
            is_root=is_root,
            is_ending=node_data.isEnding,
            is_winning=node_data.isWinningEnding,
            options=[]
        )
        # replacing node_data["attribute"] with node_data.attribute - for resolving error - 'StoryNodeLLM' object is not subscriptable

        db.add(node)
        db.flush()

        # logic for recursive iteration for checking all the nodes of the story one by one till we reach to the ending node
        # processing below logic if node is non-ending and has non-empty "options" attribute
        if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
            # we are going to access each child node in the options and process it in _process_story_node function
            options_list = []
            for option_data in node_data.options:   #here we are checking options from node_data(parameter of the method) not node( the object which is being added to db)
                next_node = option_data.nextNode

                #validatin if node in this current loop iteration is of StoryNodeLLM formatted or no
                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)

                child_node = cls._process_story_node(db, story_id, next_node, is_root=False)

                options_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id
                })
            # Populating the options of the root node
            node.options = options_list  #passing the options list to the node - options

        db.flush()
        return node

















