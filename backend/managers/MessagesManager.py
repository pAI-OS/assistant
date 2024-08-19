from uuid import uuid4
from threading import Lock
from sqlalchemy import select, insert, update, delete, func
from backend.models import Message, Conversation
from backend.db import db_session_context
from backend.schemas import MessageSchema, MessageCreateSchema
from typing import List, Tuple, Optional, Dict, Any
from backend.utils import get_current_timestamp
from backend.managers.RagManager import RagManager

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

class MessagesManager:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(MessagesManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            with self._lock:
                if not hasattr(self, '_initialized'):
                    self._initialized = True

    async def create_message(self, message_data: MessageCreateSchema) -> str:
        async with db_session_context() as session:
            timestamp = get_current_timestamp()
            
            # update conversation last_updated_timestamp
            conversation_id = message_data['conversation_id']
            result = await session.execute(select(Conversation).filter(Conversation.id == conversation_id))
            conversation = result.scalar_one_or_none()
            conversation.last_updated_timestamp = timestamp
            
            #ToDo: Get correct llm model
            llm = Ollama(model="llama3.1")
            assistant_id = message_data['assistant_id']
            query = message_data['prompt']
            rm = RagManager()
            response = await rm.retrive_and_generate(assistant_id, query, llm)
            message_data["chat_response"] = response["answer"]
            message_data['timestamp'] = timestamp
            print(f"message_data = {message_data}")
            
            new_message = Message(id=str(uuid4()), **message_data)
            session.add(new_message)
            await session.commit() 
            await session.refresh(new_message)
            return new_message.id    

    async def retrieve_message(self, id:str) -> Optional[MessageSchema]:
        async with db_session_context() as session:            
            result = await session.execute(select(Message).filter(Message.id == id))
            message = result.scalar_one_or_none()
            if message:
                return MessageSchema(
                    id=message.id,
                    assistant_id=message.assistant_id,
                    conversation_id=message.conversation_id,
                    timestamp=message.timestamp,
                    prompt=message.prompt,
                    chat_response=message.chat_response,             
                )
            return None