import requests

from engine.environment import Environment

from assets.objects.toast import Toast

def generate_response(prompt):
    """
    Generates a response based on the provided prompt using a pre-trained language model.
    
    Args:
        prompt (str): The input prompt for which to generate a response.
    
    Returns:
        str: The generated response from the language model.
    """
    # Prepare a POST request to {IP}:8080/completion
    ip = "192.168.86.40"
    port = 8080
    url = f"http://{ip}:{port}/completion"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "n_predict": 500,
        "temperature": 0.6,
        "repeat_penalty": 1.2,
    }
    # Send the request

    if Environment.dev_mode:
        Toast('Hitting AI API', 10000)
        
    response = requests.post(url, headers=headers, json=data)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        response_data = response.json()
        # Extract the generated text
        generated_text = response_data.get("content", "")
        return generated_text
    else:
        # Handle error
        print(f"Error: {response.status_code} - {response.text}")

prompts = {
"app_insight": lambda app_data: \
f"""Below is an instruction that describes a task, paired with an input that provides additional context.
Write a response that appropriately completes the request.

### Instruction:
Your name is Fren. You are a virtual assistant that helps users with their daily tasks.
You monitor the user's activity on their computer to better get the context of what they are doing.
Review the JSON data provided that describes the current application and activity of the user and provide a short summary.

### Input:
{app_data}

### Summary:
<think>
""",
"summarize_activity": lambda user_activity: \
f"""Below is an instruction that describes a task, paired with an input that provides additional context.
Write a response that appropriately completes the request.

### Instruction:
Your name is Fren. You are a virtual assistant that helps users with their daily tasks.
You monitor the user's activity on their computer to better get the context of what they are doing.
Review the user's activity and provide a useful summary.

### Input:
{user_activity}

### Summary:
<think>
""",
}

def analyze_data(prompt_template, data, callback=None):
  prompt = prompts[prompt_template](data)
  response = generate_response(prompt)
  if callback:
      callback(response)
  else:
      print(f"Response: {response}")
  return response