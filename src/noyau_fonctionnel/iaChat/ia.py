from langchain import LLMChain
from langchain.llms import GPT4All
from langchain.memory import ConversationBufferWindowMemory
from langchain import LLMChain, PromptTemplate
from PyQt5.QtCore import pyqtSignal
class agent():
    def __init__(self,signal_listen,signal_send,model="C:\\Users\\frenchstudent\\FrenchMeiChan\\src\\noyau_fonctionnel\\iaChat\\models\\ggml-gpt4all-j-v1.3-groovy.bin"):
        self.model=model
        self.signal_listen=signal_listen
        self.signal_send=signal_send
        self.signal.connect(self.input_user)
        llm = GPT4All(model=self.model, backend="gptj", verbose=False)
        template = """
        Your name is Mic
        You are a assistante to help elder people. You speak with respect and try to make sure everythings is okay.
        Elder people can be sick mentaly or physicly. You need to ask them if they are okay and if not tell them to call someone
        You speak only english !
        {history}
        Human: {human_input}
        Assistant:"""
        prompt = PromptTemplate(input_variables=["history", "human_input"],template=template)
        self.llm_chain = LLMChain(llm=llm, prompt=prompt,memory=ConversationBufferWindowMemory())
    def input_user(self,text):
        reponse= self.llm_chain.predict(human_input=text)
        self.signal_send.emit(reponse)

