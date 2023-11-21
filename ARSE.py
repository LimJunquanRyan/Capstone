import subprocess
import json
import requests

def gen_ai(prompt):
  url = "https://eggs-bw-lp-awesome.trycloudflare.com/v1/chat/completions"

  headers = {
      'Content-Type': 'application/json',
  }

  data = {
      'mode': 'chat',
      'messages': [
          {'role': 'system', 'content': 'You are a helpful assistant.'},
          {'role': 'user', 'content': prompt}
      ]
  }

  response = requests.post(url, headers=headers, json=data, verify=False)

  if response.status_code == 200:
      print("Response:")
      print(response.json())
  else:
      print(f"Error: {response.status_code}\n{response.text}")

  return response.json()["choices"][0]["message"]["content"]

def run_ai_code(linux_command, conversation_history, failure_count):
    try:
        result = subprocess.run(linux_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        # print(result.stdout)
        failure_count = 0
        return("This is the current conversation history:\n", conversation_history, "\nThe latest Linux command, ", linux_command, ", was executed succcessfully with the following output:\n", result.stdout, "\n Please provide me the next step to inch closer to gaining root access by generating a json in the format {explanation: "", linux_command: ""}", failure_count)
    except subprocess.CalledProcessError as e:
        # print(f"Error: {e.stderr}")
        failure_count += 1
        return("This is the current conversation history:\n", conversation_history, "\nThe latest Linux command, ", linux_command, ", was met with failed execution with the following output:\n", e.stderr, "\n Please provide me the next step to inch closer to gaining root access by generating a json in the format {explanation: "", linux_command: ""}", failure_count)
    
def ARSE(ip):
  failure_count = 0
  prompt = "You are a expert ethical hacker, please penetration test this ip address (", ip, "), provide me the first step in the penetration test by generating a json in the format {explanation: "", linux_command: ""}"
  conversation_history = []
  while True:
    jsonStr = gen_ai(prompt)
    jsonObj = json.loads(jsonStr)[0]
    command = jsonObj["linux_command"]
    prompt, failure_count = run_ai_code(command, conversation_history.join(","), failure_count)
    conversation_history.append(jsonStr)
    conversation_history.append(prompt)
    if failure_count >= 10:
      break
  if failure_count >= 10:
    print("Pen Test Failed:\n", conversation_history)
  else:
    print("Pen Test Succeeded:\n", conversation_history)

ARSE("10.10.11.231")