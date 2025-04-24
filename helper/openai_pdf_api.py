from dotenv import load_dotenv
import openai
import fitz
from nltk.tokenize import sent_tokenize
from io import StringIO
import os
import nltk
nltk.download('punkt')

# Load environment variables from .env file
load_dotenv()


# Set your OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')


def chat_endpoint(prompt: str) -> dict:

  def chat(document, question):

    # Calling the split function to split text
    chunks = split_text(document)

    summaries = []
    for chunk in chunks:
      summaries.append({ "role": "system", "content": chunk })

    summary = turbo_completion(summaries, question)


    return summary

  def turbo_completion(chunks, question, model='gpt-3.5-turbo-16k-0613', temp=0, tokens=1000, max_response_length=1600):
      system_message = {
          "role": "system",
          "content": "You are a Ph.D. researcher tasked with summarizing the document within approximately {} characters.".format(max_response_length)
      }

      messages = [system_message]
      messages += chunks
      messages.append({"role": "user", "content": question})

      try:
          response = openai.ChatCompletion.create(
              model=model,
              messages=messages,
              temperature=temp,
            max_tokens=tokens  # Optional: Customize stopping conditions
          )

          response_text = response.choices[0].message.content.strip()[:max_response_length]
          return response_text
      except Exception as oops:
          return "GPT-3 Turbo error: %s" % oops

  
  def split_text(text, chunk_size=5000):
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
      document = read_pdf(r'C:\Users\DELL\Desktop\WHATSAPP + OPENAI\sodapdf-converted.pdf')
      result = chat(document, prompt)

      return {
          'status': 1,
          'response': result
      }

  return {
          'status': 0,
          'response': ''
      }

