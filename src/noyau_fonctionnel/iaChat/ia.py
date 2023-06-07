from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler



template = """Question: {question}

Answer: Let's work this out in a step by step way to be sure we have the right answer."""

prompt = PromptTemplate(template=template, input_variables=["question"])

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = LlamaCpp(
    model_path="./llama.cpp/models/7B/ggml-model-q4_0.bin", 
    callback_manager=callback_manager, 
    verbose=True
)

llm_chain = LLMChain(prompt=prompt, llm=llm)
text = "What would be a good company name for a company that makes colorful socks?"
llm_chain.run(text)