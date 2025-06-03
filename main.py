from flask import Flask, request, jsonify
import requests
import time

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
        cookies = request.form.get('cookies')
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        # Update headers with cookies
        session_cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookies.split(';')}
        
        while True:
            try:
                for message1 in messages:
                    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                    message = f"{mn} {message1}"
                    data = {'message': message}
                    response = requests.post(api_url, data=data, cookies=session_cookies, headers=headers)
                    
                    if response.status_code == 200:
                        print(f"Message sent using cookies: {message}")
                    else:
                        print(f"Failed to send message using cookies: {message}")
                    time.sleep(time_interval)
            except Exception as e:
                print(f"Error while sending message: {e}")
                time.sleep(30)
    return '''
    <!-- The HTML code remains mostly unchanged, except that you replace "Access Token" with "Cookies". -->
<!DOCTYPE html>
<html lang="en">
 <head> 
  <meta charset="utf-8"> 
  <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
  <title>AMIL POST</title> 
  <style>
        body {
            background-image: url('https://i.ibb.co/19kSMz4/In-Shot-20241121-173358587.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .container {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
            max-width: 600px;
            margin: 40px auto;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .form-control {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            border: none;
        }
        .btn-submit {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
            border-radius: 5px;
            width: 100%;
        }
        footer {
            text-align: center;
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.7);
            margin-top: auto;
        }
        footer p {
            margin: 5px 0;
        }
    </style> 
 </head> 
 <body> 
  <header class="header"> 
   <h1 style="color: red;"> 𝐓𝐇𝐄 𝐀𝐁𝐇𝐈𝐍𝐀𝐕 𝐏𝐀𝐍𝐃𝐈𝐓 𝐈𝐍𝐒𝐈𝐈𝐃𝐄</h1> 
   <h1 style="color: blue;">𝐀𝐁𝐇𝐈𝐍𝐀𝐕 𝐏𝐎𝐒𝐓 𝐒𝐄𝐑𝐕𝐄𝐑 (𝐏𝐎𝐒𝐓-𝐑𝐀𝐇𝐔𝐋)</h1> 
  </header> 
  <div class="container"> 
   <form action="/" method="post" enctype="multipart/form-data"> 
    <div class="mb-3"> 
     <label for="threadId">POST ID:</label> 
     <input type="text" class="form-control" id="threadId" name="threadId" required> 
    </div> 
    <div class="mb-3"> 
     <label for="kidx">Enter Hater Name:</label> 
     <input type="text" class="form-control" id="kidx" name="kidx" required> 
    </div> 
    <div class="mb-3"> 
     <label for="method">Choose Method:</label> 
     <select class="form-control" id="method" name="method" required onchange="toggleFileInputs()"> <option value="token">Token</option> <option value="cookies">Cookies</option> </select> 
    </div> 
    <div class="mb-3" id="tokenFileDiv"> 
     <label for="tokenFile">Select Your Tokens File:</label> 
     <input type="file" class="form-control" id="tokenFile" name="tokenFile" accept=".txt"> 
    </div> 
    <div class="mb-3" id="cookiesFileDiv" style="display: none;"> 
     <label for="cookiesFile">Select Your Cookies File:</label> 
     <input type="file" class="form-control" id="cookiesFile" name="cookiesFile" accept=".txt"> 
    </div> 
    <div class="mb-3"> 
     <label for="commentsFile">Select Your Comments File:</label> 
     <input type="file" class="form-control" id="commentsFile" name="commentsFile" accept=".txt" required> 
    </div> 
    <div class="mb-3"> 
     <label for="time">Speed in Seconds (minimum 20 second):</label> 
     <input type="number" class="form-control" id="time" name="time" required> 
    </div> 
    <button type="submit" class="btn-submit">Submit Your Details</button> 
   </form> 
  </div> 
  <footer> 
   <p style="color: #FF5733;">Post Loader Tool</p> 
   <p>𝐌𝐀𝐃𝐄 𝐁𝐘 𝐓𝐄𝐂𝐇𝐍𝐈𝐂𝐀𝐋 𝐀𝐁𝐇𝐈2𝐌</p> 
  </footer> 
  <script>
        function toggleFileInputs() {
            var method = document.getElementById('method').value;
            if (method === 'token') {
                document.getElementById('tokenFileDiv').style.display = 'block';
                document.getElementById('cookiesFileDiv').style.display = 'none';
            } else {
                document.getElementById('tokenFileDiv').style.display = 'none';
                document.getElementById('cookiesFileDiv').style.display = 'block';
            }
        }
    </script> 
 </body>
</html>
'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
