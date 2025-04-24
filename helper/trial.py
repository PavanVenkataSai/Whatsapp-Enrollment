import openai
import fitz
from nltk.tokenize import sent_tokenize
from io import StringIO
import os
import nltk
nltk.download('punkt')

from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


os.environ['OPENAI_API_KEY']='s7NxsGbv'

def chat_endpoint(prompt):

  def create_rqa(chunks, question):
      prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Format your responses as a friendly assistant.
    Your goal is to have a conversational interaction, answer user questions, and inquire about their preferences. 
    Respond to user specific question. If any greetings message response with greetings.
    
      {context}

      

      Question: {question}
      Answer in English:"""
      PROMPT = PromptTemplate(
          template=prompt_template, input_variables=["context", "question"]
      )

      embeddings = OpenAIEmbeddings()
      docsearch = FAISS.from_texts(chunks, embeddings)
      retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 4})
      chain_type_kwargs = {"prompt": PROMPT}
      rqa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True, chain_type_kwargs=chain_type_kwargs)
      answer = rqa(question)
      
      return answer

  def split_text(text, chunk_size=2000):
    """
    Splits the given text into chunks of approximately the specified chunk size.

    Args:
    text (str): The text to split.

    chunk_size (int): The desired size of each chunk (in characters).

    Returns:
    List[str]: A list of chunks, each of approximately the specified chunk size.
    """

    chunks = []
    current_chunk = StringIO()
    current_size = 0
    sentences = sent_tokenize(text)
    for sentence in sentences:
      sentence_size = len(sentence)
      if sentence_size > chunk_size:
        while sentence_size > chunk_size:
          chunk = sentence[:chunk_size]
          chunks.append(chunk)
          sentence = sentence[chunk_size:]
          sentence_size -= chunk_size
          current_chunk = StringIO()
          current_size = 0
      if current_size + sentence_size < chunk_size:
        current_chunk.write(sentence)
        current_size += sentence_size
      else:
        chunks.append(current_chunk.getvalue())
        current_chunk = StringIO()
        current_chunk.write(sentence)
        current_size = sentence_size
    if current_chunk:
      chunks.append(current_chunk.getvalue())
    return chunks


  def read_pdf(filename):
    context = ''

    with fitz.open(filename) as pdf_file:
        num_pages = pdf_file.page_count

        for page_num in range(num_pages):
            page = pdf_file[page_num]
            page_text = page.get_text()
            context += page_text

    return context
    
  if prompt:
    document = read_pdf(r'C:\Users\Dell\Desktop\Whatsapp+OpenAI\ValueHealthSol.pdf')
    result = create_rqa(split_text(document), prompt)
    return {
        'status': 1,
        'response': result['result']
    }

  else:
    return {
        'status': 0,
        'response':''
    }

# print((chat_endpoint("what are the features of the company linked cabs?")))