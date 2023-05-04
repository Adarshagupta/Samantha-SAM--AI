import http.client
import base64
import json
import openai
import os

# Set up OpenAI API credentials
openai.api_key = os.environ["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"]

# Define a function to generate a respose using OpenAI's GPT-3
def generate_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

# Define the D-ID API endpoint and API key
api_key = 'Ymx1ZWFkYXJzaDFAZ21haWwuY29t:dbEqADkv2esLTD3vE2Hrc'
headers = {
    'Content-Type': 'multipart/form-data',
    'Authorization': 'Basic ' + base64.b64encode(('apikey:' + api_key).encode('ascii')).decode('ascii')
}

conn = http.client.HTTPSConnection("api.d-id.com")

# Define the prompt for OpenAI's GPT-3
prompt = "Convert this image into an AI assistant."

# Generate a response using OpenAI's GPT-3
response_text = generate_response(prompt)

# Print the generated response
print(f'GPT-3 response: {response_text}')

# Define the payload for the D-ID API request
payload = '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="image"; filename="image.jpg"\r\nContent-Type: image/jpeg\r\n\r\n'
with open('Samantha(SAM).jpeg', 'rb') as f:
    payload += f.read().decode('ISO-8859-1')
payload += '\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'

# Make the D-ID API request
conn.request("POST", "/v2.3/face-swapping/image", payload, headers=headers)

res = conn.getresponse()
data = res.read().decode("utf-8")

if res.status == 200:
    response_dict = json.loads(data)
    if response_dict.get('success', False):
        output_image_data = response_dict.get('output', '')
        if output_image_data:
            with open('output_image.jpg', 'wb') as f:
                f.write(output_image_data)
            print('Output image saved as output_image.jpg')
        else:
            print('Error: Output image not found in API response')
    else:
        error_message = response_dict.get('error_message', 'Unknown error')
        print(f'Error: {error_message}')
else:
    print(f'Error: API request failed with status code {res.status}\n{data}')
