import json
import openai

client = openai.OpenAI(api_key="API-KEY")

PROMPT = """
You will be given descriptions of books provided by users. 
Your task is to extract specific pieces of information from each description and organize them into a dictionary. 
The fields to be extracted are: category, title, author, publisher, year, page, language, extension. 

If any information is missing from the user's description, you should return null for that field. 
The output should be structured as a json, with each field represented as a key and the extracted or missing information as the value.

Example:
User Description: "I'm looking for a fantasy book titled 'The Enchanted Forest' by John Smith, published in 2015 by Magic Press, 300 pages, in English."

Output:
{
  "category": "fantasy",
  "title": "The Enchanted Forest",
  "author": "John Smith",
  "publisher": "Magic Press",
  "year": 2015,
  "page": 300,
  "language": "English",
}

Your goal is to accurately fill out this dictionary based on the information provided in the user's description. 
If a user doesn’t mention the book's language, for example, you should return null the 'language' field.

The following is the user's description:
```
[USER_DESCRIPTION]
```
"""


def extract_fields(user_input):
    prompt = PROMPT.replace("[USER_DESCRIPTION]", user_input)
    retry = 0
    while retry < 3:
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
            )
            text = completion.choices[0].message.content
            return json.loads(text)
        except Exception as e:
            print(e)
            retry += 1
    return {}


if __name__ == "__main__":
    user_input = "I'm looking for a Comic book, 300 pages, in English and publish on 2024 and does'nt need anything more."
    fields = extract_fields(user_input)
    print(fields)
