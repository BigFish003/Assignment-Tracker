import json
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI


# File paths
file_path = r"C:\Users\samth\chome\data\data.json"
refined_path = r"C:\Users\samth\chome\data\refined.json"


# Flask app setup
app = Flask(__name__)
CORS(app)


# Time
today = date.today()
def days_until_future_date(input_date):
   input_date = datetime.strptime(input_date, "%b %d").replace(year=datetime.now().year)
   current_date = datetime.now()
   date_difference = input_date - current_date
   if date_difference.days < 0:
       input_date = input_date.replace(year=input_date.year + 1)
       date_difference = input_date - current_date
   days_difference = date_difference.days


   return days_difference


# OpenAI setup
client = OpenAI(
   api_key="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",
)


# Functions
def evaluate(dd, at, c):
   chat_completion = client.chat.completions.create(
       messages=[
           {
               "role": "user",
               "content": f"only respond to this prompt with a digit, ex: '38', no more:  today is {today}, I have an assignment due on {dd} here is the name and content of the assignment, Name: {at}, Content: {c}, based on what ive told you, how long do you think it will take me to do this assignment, the only thing that your answer will contain is the number of minutes you think it will take me based on the title and content",
           }
       ],
       model="gpt-3.5-turbo",
   )
   return chat_completion.choices[0].message.content


def jsinclr():
   with open(file_path, 'w') as file:
       json.dump([], file)


def rtrnlst(lst):
   try:
       with open(lst, 'r') as file:
           loaded_list = json.load(file)
           return loaded_list
   except FileNotFoundError:
       print(f"The file {lst} does not exist.")
   except json.JSONDecodeError as e:
       print(f"Error decoding JSON: {e}")
   except Exception as e:
       print(f"An error occurred: {e}")


def addjsontolist(file_path, new_item):
   try:
       with open(file_path, 'r') as file:
           existing_data = json.load(file)


       existing_data.append(new_item)


       with open(file_path, 'w') as file:
           json.dump(existing_data, file)


       print(f"Item '{new_item}' added to the JSON list in {file_path}.")


   except FileNotFoundError:
       print(f"The file {file_path} does not exist.")
   except json.JSONDecodeError as e:
       print(f"Error decoding JSON: {e}")
   except Exception as e:
       print(f"An error occurred: {e}")


def refine(thing):
   if int(days_until_future_date(thing["message"]["dd"])) < 150:
       if int(days_until_future_date(thing["message"]["dd"])) <2:
           y = "t"
       elif int(days_until_future_date(thing["message"]["dd"])) <8:
           y = "w"
       else:
           y = "m"
       newdata = [y, thing["message"]["at"], int(evaluate(thing["message"]["dd"], thing["message"]["at"], thing["message"]["c"]))]
       addjsontolist(refined_path, newdata)
   else:pass


# Flask route
@app.route('/api', methods=['POST'])
def process_extension_data():
   data = request.get_json()
   print("Received data:", data)
   addjsontolist(file_path, data)
   refine(data)
   return jsonify({"response": "Message received and processed successfully"})


def calculate_total_time():
   assignment_list = []
   wassignment_list = []
   massignment_list = []
   lis = rtrnlst(refined_path)
   for i in range(len(lis)):
       if lis[i][0] == "t":
           assignment_list.append([lis[i][1], lis[i][2]])
   for i in range(len(lis)):
       if lis[i][0] == "w":
           wassignment_list.append([lis[i][1], lis[i][2]])
   for i in range(len(lis)):
       if lis[i][0] == "m":
           massignment_list.append([lis[i][1], lis[i][2]])
   total_time = sum(int(item[1]) if isinstance(item[1], int) else int(item[1]) for item in assignment_list if str(item[1]).isdigit())
   return [total_time, assignment_list, wassignment_list, massignment_list]


@app.route('/remove_assignment', methods=['POST'])
def remove_assignment():
    data = request.get_json()
    assignment = data.get('assignment')
    time = data.get('time')
    rem = [assignment, time]



@app.route('/assignment_tracker')
def assignment_tracker():
   total_time = calculate_total_time()
   print(total_time)
   return render_template('assignment_tracker.html', assignment_list=total_time[1], wassignment_list = total_time[2] , massignment_list = total_time[3], total_time=total_time[0])


if __name__ == '__main__':
   app.run(debug=True)

