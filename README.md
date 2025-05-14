 Open Command Prompt (CMD)
Press Win + R, type cmd, and hit Enter
Use the cd (Change Directory) command to go to your project folder.
Else
Open the File fraud_detection_app.py in IDLE 
Then Click F5 To run the Code in IDLE
U get The O/P in Following Way:

🚀 Starting Fraud Detection API...
 * Serving Flask app 'fraud_detection_app'
 * Debug mode: off
[31m[1mWARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.[0m
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.0.106:5000
[33mPress CTRL+C to quit[0m

Now open Command Prompt and Run the Curl command in the Command Prompt

The Curl Command is given Below:

curl --header "Content-Type: application/json" --request POST --data "{\"CardNumber\": \"cardno\", \"Amount\": amt}" http://127.0.0.1:5000/detect

1.Replace the cardno with the CardNumber thaat have to be tested
2.Replace the amt with the Amount needed to be entered
Follow the above 2 points before Entering the Curl command in the Cmd prmpt

Hence You Get the Output.
