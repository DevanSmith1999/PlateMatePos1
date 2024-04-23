
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS 
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate

import os
import pandas as pd


#api-key
os.environ["OPENAI_API_KEY"] = "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"
api_key = "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"


#Path to csv file  #needs to be changed later
file_path = "PlateMate/Final_Menu_Items_with_Ingredients_v2.csv"
df = pd.read_csv(file_path)

#List of comma-separated strings representing each row of the CSV.
texts = [', '.join(map(str, row)) for row in df.values]



#Creates embeddings using OpenAI's Text Embedding API.
embeddings = OpenAIEmbeddings(deployment= "text-embedding-ada-002", chunk_size=1, api_key= "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")
docsearch = FAISS.from_texts(texts, embeddings)

# Later change to take input from front-end
#query = input("Input text here: ")

# main function interacting with the Chatbot
def chat(query):    
    retriever = docsearch.as_retriever(search_type ="similarity", search_kwargs={"k":15})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")
    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature = 0.2)


    #Chatbot template used to manipulate its parameters
    system_template = """
    You are a simple chatbot aimed at answering questions about the menu for customers.
    The menu is given to you through your vector database reference.
    For anything food or menu-related, your answer should be short and polite.
    You have freedom to answer general questions about food
    If a customer asks a question not related to the topic of food or menu items, 
    try to steer the cover conversation back on topic.
    # For the additional context of this restaurant the following information can be used:
  # • FISH IS FRIED IN A MIXTURE OF CORN FLOUR AND CORN MEAL
  # • SHRIMP (Large, Tail On) ARE FRIED IN CORN FLOUR
  # • OYSTERS ARE FRIED IN CORN MEAL
  # • SOFT SHELLS, FROG LEGS, CHICKEN AND POPCORN SHRIMP ARE FRIED IN WHITE
  # FLOUR (these items are not Gluten Free)
  # • THE SEAFOOD CAN BE BATTERED DIFFERENTLY FOR SPECIAL REQUESTS
  # • ALL SEAFOOD IS COOKED WITH SALT (CAN BE COOKED WITH NO SALT BY RE-
  # QUEST)
  # • WE FRY OUR FOOD IN VEGETABLE OIL - NEVER PEANUT OIL
  # • OUR BROILED AND BOILED SEAFOOD IS GLUTEN-FREE
  # • WE DO NOT HAVE A HOUSE DRESSING...REMOULADE, COCKTAIL, AND TARTAR
  # ARE ALL HOMEMADE
  # • IF SOMEONE ADDS A SIDE OF TOAST OR FRENCH BREAD TO THEIR ORDER IT IS
  # AN ADDITIONAL CHARGE (2 SLICES TOAST=1.00, FRENCH BREAD=1.50)
  # • WE DO NOT OFFER A SENIOR CITIZEN DISCOUNT
  # • WE SUPPORT OUR MILITARY AND FIRST RESPONDERS BY DONATING TO VARI-
  # OUS LOCAL CHARITIES. WE DO NOT OFFER A DISCOUNT TO MILITARY OR FIRST RESPONDERS.
    ----------------
    CONTEXT:
    {context}

    CHAT HISTORY:
    {chat_history}

    USER QUESTION:
    {question}

    """
    prompt_doc = PromptTemplate(template = system_template, input_variables=["CONTEXT", "CHAT HISTORY", "USER QUESTION"])

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        memory = memory,
        retriever = retriever,
        combine_docs_chain_kwargs={'prompt': prompt_doc},
    )
    #accepts user and returns the Chatbot's response
    
    result = qa_chain({"question": query})
    print(result["answer"])
    return(result["answer"])



