from langchain import LLMChain
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.agents import load_tools,initialize_agent,AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import SimpleSequentialChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

local_path = (
    "C:\\Users\\frenchstudent\\FrenchMeiChan\\src\\noyau_fonctionnel\\iaChat\\models\\ggml-gpt4all-j-v1.3-groovy.bin"  # replace with your desired local file path
)
# Callbacks support token-wise streaming
callbacks = [StreamingStdOutCallbackHandler()]
llm = GPT4All(model=local_path, backend="gptj", callbacks=callbacks, verbose=False)

template = """Assistant is a large language model with GPT4ALL.

Assistant is designed to be able to assist with a wide range of tasks, 
from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. 
As a language model, Assistant is able to generate human-like text based on the input it receives, 
allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving.
It is able to process and understand large amounts of text, and can use this knowledge to provide 
accurate and informative responses to a wide range of questions. 
Additionally, Assistant is able to generate its own text based on the input it receives, 
allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

{history}
Human: {human_input}
Assistant:"""

tools = load_tools(
    ["arxiv"],
)

prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)
llm_chain = LLMChain(llm=llm, prompt=prompt,verbose=False,memory=ConversationBufferWindowMemory())

#Agent use, with GPT4ALL, USE CASE 1
agent = initialize_agent(tools, llm, verbose=False)

while(True):
    text=input("Human : ")
    print("Mic : ")
    #agent.run(input=text)
    print(llm_chain.memory)
    llm_chain.predict(human_input=text)
    print("\n")

