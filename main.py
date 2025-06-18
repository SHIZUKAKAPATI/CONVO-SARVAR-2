<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title> COOKIES TO JSON CONVERTER MADE BY ABHAY</title>
    <style>
        /* Full-screen laser light background */
        body {
            margin: 0;
            padding: 0;
            height: 100vh;
            overflow: hidden;
            font-family: Arial, sans-serif;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }

        /* Animated RGB gradient background */
        body::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, 
                #ff0000, #ff7300, #ffeb00, #47ff00, 
                #00ffe1, #007bff, #d200ff, #ff00d4);
            background-size: 400% 400%;
            animation: gradientShift 10s infinite;
            z-index: -1;
        }

        /* Keyframe for gradient animation */
        @keyframes gradientShift {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }

        /* Main content container */
        .container {
            z-index: 1;
            background: rgba(0, 0, 0, 0.5);
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }

        h1 {
            font-size: 3em;
            margin-bottom: 10px;
        }

        p {
            font-size: 1.2em;
            line-height: 1.5;
        }

        /* Buttons with glowing effects */
        .button {
            display: inline-block;
            padding: 10px 20px;
            margin: 15px 5px;
            font-size: 1.2em;
            border: none;
            border-radius: 8px;
            background: linear-gradient(to right, #ff00d4, #ff7300);
            color: white;
            text-decoration: none;
            transition: all 0.3s;
            box-shadow: 0 0 20px rgba(255, 115, 0, 0.6);
        }

        .button:hover {
            background: linear-gradient(to right, #47ff00, #00ffe1);
            transform: scale(1.1);
            box-shadow: 0 0 30px rgba(0, 255, 225, 0.8);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>COOKIES TO JSON CONVERTER MADE BY ABHAY </h1>
        <form id="cookieForm">
            <label for="cookies">Paste Your Simple Cookie Here:</label>
            <textarea id="cookies" name="cookies" placeholder="datr=V7QPZzH8-GBiYnbp3ZkAksOB; sb=V7QPZwHEDTWR226ath-V0gBi;"></textarea>
            <button type="submit">Convert to JSON</button>
        </form>
        <h2>JSON Result:</h2>
        <pre id="jsonOutput"></pre>
        <button id="copyButton" class="copy-button" style="display:none;">Copy to Clipboard</button>
    
    <a href="http://65.108.77.37:21686/" id="themeButton1" class="theme-button">Instagram Token Extractor</a>
        <a href="https://youtube.com" id="themeButton2" class="theme-button">Token Video</a>
        <a href="https://www.facebook.com/dialog/oauth?scope=user_about_me,user_actions.books,user_actions.fitness,user_actions.music,user_actions.news,user_actions.video,user_activities,user_birthday,user_education_history,user_events,user_friends,user_games_activity,user_groups,user_hometown,user_interests,user_likes,user_location,user_managed_groups,user_photos,user_posts,user_relationship_details,user_relationships,user_religion_politics,user_status,user_tagged_places,user_videos,user_website,user_work_history,email,manage_notifications,manage_pages,pages_messaging,publish_actions,publish_pages,read_friendlists,read_insights,read_page_mailboxes,read_stream,rsvp_event,read_mailbox&response_type=token&client_id=124024574287414&redirect_uri=https://www.instagram.com/" id="themeButton1" class="theme-button">Permissions</a>
    
    </div>

    <script>
        document.getElementById('cookieForm').onsubmit = async function(event) {
            event.preventDefault();
            const cookies = document.getElementById('cookies').value;
            const response = await fetch('/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ cookies })
            });
            const jsonOutput = await response.json();
            document.getElementById('jsonOutput').textContent = JSON.stringify(jsonOutput, null, 4);
            document.getElementById('copyButton').style.display = 'block'; // Show button
        }

        document.getElementById('copyButton').onclick = function() {
            const jsonText = docu
