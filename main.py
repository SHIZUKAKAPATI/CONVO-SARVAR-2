import random
import string
import json
import time
import requests
import uuid
import base64
import io
import struct
import sys
import os  # <-- IMPORTANT: Add os import
from flask import Flask, render_template_string, request, jsonify, session
import threading

# Crypto libraries check
try:
    from Crypto.Cipher import AES, PKCS1_v1_5
    from Crypto.PublicKey import RSA
    from Crypto.Random import get_random_bytes
except ImportError:
    print("Error: 'pycryptodome' module not found.")
    print("Run: pip install pycryptodome")
    sys.exit()

# ===========================================
# ORIGINAL CLASSES (UNCHANGED)
# ===========================================

class FacebookPasswordEncryptor:
    @staticmethod
    def get_public_key():
        try:
            url = 'https://b-graph.facebook.com/pwd_key_fetch'
            params = {
                'version': '2',
                'flow': 'CONTROLLER_INITIALIZATION',
                'method': 'GET',
                'fb_api_req_friendly_name': 'pwdKeyFetch',
                'fb_api_caller_class': 'com.facebook.auth.login.AuthOperations',
                'access_token': '438142079694454|fc0a7caa49b192f64f6f5a6d9643bb28'
            }
            response = requests.post(url, params=params).json()
            return response.get('public_key'), str(response.get('key_id', '25'))
        except Exception as e:
            raise Exception(f"Public key fetch error: {e}")

    @staticmethod
    def encrypt(password, public_key=None, key_id="25"):
        if public_key is None:
            public_key, key_id = FacebookPasswordEncryptor.get_public_key()

        try:
            rand_key = get_random_bytes(32)
            iv = get_random_bytes(12)
            
            pubkey = RSA.import_key(public_key)
            cipher_rsa = PKCS1_v1_5.new(pubkey)
            encrypted_rand_key = cipher_rsa.encrypt(rand_key)
            
            cipher_aes = AES.new(rand_key, AES.MODE_GCM, nonce=iv)
            current_time = int(time.time())
            cipher_aes.update(str(current_time).encode("utf-8"))
            encrypted_passwd, auth_tag = cipher_aes.encrypt_and_digest(password.encode("utf-8"))
            
            buf = io.BytesIO()
            buf.write(bytes([1, int(key_id)]))
            buf.write(iv)
            buf.write(struct.pack("<h", len(encrypted_rand_key)))
            buf.write(encrypted_rand_key)
            buf.write(auth_tag)
            buf.write(encrypted_passwd)
            
            encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
            return f"#PWD_FB4A:2:{current_time}:{encoded}"
        except Exception as e:
            raise Exception(f"Encryption error: {e}")


class FacebookAppTokens:
    APPS = {
        'FB_ANDROID': {'name': 'Facebook For Android', 'app_id': '350685531728'},
        'MESSENGER_ANDROID': {'name': 'Facebook Messenger For Android', 'app_id': '256002347743983'},
        'FB_LITE': {'name': 'Facebook For Lite', 'app_id': '275254692598279'},
        'MESSENGER_LITE': {'name': 'Facebook Messenger For Lite', 'app_id': '200424423651082'},
        'ADS_MANAGER_ANDROID': {'name': 'Ads Manager App For Android', 'app_id': '438142079694454'},
        'PAGES_MANAGER_ANDROID': {'name': 'Pages Manager For Android', 'app_id': '121876164619130'}
    }
    
    @staticmethod
    def get_app_id(app_key):
        app = FacebookAppTokens.APPS.get(app_key)
        return app['app_id'] if app else None
    
    @staticmethod
    def get_all_app_keys():
        return list(FacebookAppTokens.APPS.keys())
    
    @staticmethod
    def extract_token_prefix(token):
        for i, char in enumerate(token):
            if char.islower():
                return token[:i]
        return token


class FacebookLogin:
    API_URL = "https://b-graph.facebook.com/auth/login"
    ACCESS_TOKEN = "350685531728|62f8ce9f74b12f84c123cc23437a4a32"
    API_KEY = "882a8490361da98702bf97a021ddc14d"
    SIG = "214049b9f17c38bd767de53752b53946"
    
    BASE_HEADERS = {
        "content-type": "application/x-www-form-urlencoded",
        "x-fb-net-hni": "45201",
        "zero-rated": "0",
        "x-fb-sim-hni": "45201",
        "x-fb-connection-quality": "EXCELLENT",
        "x-fb-friendly-name": "authenticate",
        "x-fb-connection-bandwidth": "78032897",
        "x-tigon-is-retry": "False",
        "authorization": "OAuth null",
        "x-fb-connection-type": "WIFI",
        "x-fb-device-group": "3342",
        "priority": "u=3,i",
        "x-fb-http-engine": "Liger",
        "x-fb-client-ip": "True",
        "x-fb-server-cluster": "True"
    }
    
    def __init__(self, uid_phone_mail, password, machine_id=None, convert_token_to=None, convert_all_tokens=False):
        self.uid_phone_mail = uid_phone_mail
        
        if password.startswith("#PWD_FB4A"):
            self.password = password
        else:
            self.password = FacebookPasswordEncryptor.encrypt(password)
        
        if convert_all_tokens:
            self.convert_token_to = FacebookAppTokens.get_all_app_keys()
        elif convert_token_to:
            self.convert_token_to = convert_token_to if isinstance(convert_token_to, list) else [convert_token_to]
        else:
            self.convert_token_to = []
        
        self.session = requests.Session()
        
        self.device_id = str(uuid.uuid4())
        self.adid = str(uuid.uuid4())
        self.secure_family_device_id = str(uuid.uuid4())
        self.machine_id = machine_id if machine_id else self._generate_machine_id()
        self.jazoest = ''.join(random.choices(string.digits, k=5))
        self.sim_serial = ''.join(random.choices(string.digits, k=20))
        
        self.headers = self._build_headers()
        self.data = self._build_data()
    
    @staticmethod
    def _generate_machine_id():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    
    def _build_headers(self):
        headers = self.BASE_HEADERS.copy()
        headers.update({
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"350685531728","retry_attempt":"0"},"application_tags":"unknown"}',
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23113RKC6C Build/PQ3A.190705.08211809) [FBAN/FB4A;FBAV/417.0.0.33.65;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/480086274;FBCR/MobiFone;FBMF/Redmi;FBBD/Redmi;FBDV/23113RKC6C;FBSV/9;FBCA/x86:armeabi-v7a;FBDM/{density=1.5,width=1280,height=720};FB_FW/1;FBRV/0;]"
        })
        return headers
    
    def _build_data(self):
        base_data = {
            "format": "json",
            "email": self.uid_phone_mail,
            "password": self.password,
            "credentials_type": "password",
            "generate_session_cookies": "1",
            "locale": "vi_VN",
            "client_country_code": "VN",
            "api_key": self.API_KEY,
            "access_token": self.ACCESS_TOKEN
        }
        
        base_data.update({
            "adid": self.adid,
            "device_id": self.device_id,
            "generate_analytics_claim": "1",
            "community_id": "",
            "linked_guest_account_userid": "",
            "cpl": "true",
            "try_num": "1",
            "family_device_id": self.device_id,
            "secure_family_device_id": self.secure_family_device_id,
            "sim_serials": f'["{self.sim_serial}"]',
            "openid_flow": "android_login",
            "openid_provider": "google",
            "openid_tokens": "[]",
            "account_switcher_uids": f'["{self.uid_phone_mail}"]',
            "fb4a_shared_phone_cpl_experiment": "fb4a_shared_phone_nonce_cpl_at_risk_v3",
            "fb4a_shared_phone_cpl_group": "enable_v3_at_risk",
            "enroll_misauth": "false",
            "error_detail_type": "button_with_disabled",
            "source": "login",
            "machine_id": self.machine_id,
            "jazoest": self.jazoest,
            "meta_inf_fbmeta": "V2_UNTAGGED",
            "advertiser_id": self.adid,
            "encrypted_msisdn": "",
            "currently_logged_in_userid": "0",
            "fb_api_req_friendly_name": "authenticate",
            "fb_api_caller_class": "Fb4aAuthHandler",
            "sig": self.SIG
        })
        
        return base_data
    
    def _convert_token(self, access_token, target_app):
        try:
            app_id = FacebookAppTokens.get_app_id(target_app)
            if not app_id:
                return None
            
            response = requests.post(
                'https://api.facebook.com/method/auth.getSessionforApp',
                data={
                    'access_token': access_token,
                    'format': 'json',
                    'new_app_id': app_id,
                    'generate_session_cookies': '1'
                }
            )
            
            result = response.json()
            
            if 'access_token' in result:
                token = result['access_token']
                prefix = FacebookAppTokens.extract_token_prefix(token)
                
                cookies_dict = {}
                cookies_string = ""
                
                if 'session_cookies' in result:
                    for cookie in result['session_cookies']:
                        cookies_dict[cookie['name']] = cookie['value']
                        cookies_string += f"{cookie['name']}={cookie['value']}; "
                
                return {
                    'token_prefix': prefix,
                    'access_token': token,
                    'cookies': {
                        'dict': cookies_dict,
                        'string': cookies_string.rstrip('; ')
                    }
                }
            return None     
        except:
            return None
    
    def _parse_success_response(self, response_json):
        original_token = response_json.get('access_token')
        original_prefix = FacebookAppTokens.extract_token_prefix(original_token)
        
        result = {
            'success': True,
            'original_token': {
                'token_prefix': original_prefix,
                'access_token': original_token
            },
            'cookies': {}
        }
        
        if 'session_cookies' in response_json:
            cookies_dict = {}
            cookies_string = ""
            for cookie in response_json['session_cookies']:
                cookies_dict[cookie['name']] = cookie['value']
                cookies_string += f"{cookie['name']}={cookie['value']}; "
            result['cookies'] = {
                'dict': cookies_dict,
                'string': cookies_string.rstrip('; ')
            }
        
        if self.convert_token_to:
            result['converted_tokens'] = {}
            for target_app in self.convert_token_to:
                converted = self._convert_token(original_token, target_app)
                if converted:
                    result['converted_tokens'][target_app] = converted
        
        return result
    
    def _handle_2fa_manual(self, error_data):
        return {
            'requires_2fa': True,
            'login_first_factor': error_data['login_first_factor'],
            'uid': error_data['uid']
        }
    
    def login(self):
        try:
            response = self.session.post(self.API_URL, headers=self.headers, data=self.data)
            response_json = response.json()
            
            if 'access_token' in response_json:
                return self._parse_success_response(response_json)
            
            if 'error' in response_json:
                error_data = response_json.get('error', {}).get('error_data', {})
                
                # Check for 2FA requirement
                if 'login_first_factor' in error_data and 'uid' in error_data:
                    return self._handle_2fa_manual(error_data)
                
                return {
                    'success': False,
                    'error': response_json['error'].get('message', 'Unknown error'),
                    'error_user_msg': response_json['error'].get('error_user_msg')
                }
            
            return {'success': False, 'error': 'Unknown response format'}
            
        except json.JSONDecodeError:
            return {'success': False, 'error': 'Invalid JSON response'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

# ===========================================
# FLASK APPLICATION
# ===========================================

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'facebook_login_tool_secret_key_2024')
login_sessions = {}

# HTML Template with CSS and JavaScript
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>𝕱𝖆𝖈𝖊𝖇𝖔𝖔𝖐 𝕷𝖔𝖌𝖎𝖓 𝕿𝖔𝖔𝖑</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }

        :root {
            --primary-gradient: linear-gradient(135deg, #1877f2 0%, #00a8ff 100%);
            --secondary-gradient: linear-gradient(135deg, #4267B2 0%, #5890ff 100%);
            --dark-bg: #0f1419;
            --card-bg: rgba(255, 255, 255, 0.05);
            --glass-bg: rgba(255, 255, 255, 0.08);
            --text-primary: #ffffff;
            --text-secondary: #b0b3b8;
            --accent: #00a8ff;
            --success: #00d68f;
            --danger: #ff4757;
            --warning: #ffaa00;
        }

        body {
            background-color: var(--green-bg);
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(24, 119, 242, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 70%, rgba(0, 168, 255, 0.15) 0%, transparent 50%);
            min-height: 100vh;
            color: var(--text-primary);
            overflow-x: hidden;
            position: relative;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                linear-gradient(90deg, transparent 49%, rgba(255,255,255,0.03) 50%, transparent 51%),
                linear-gradient(transparent 49%, rgba(255,255,255,0.03) 50%, transparent 51%);
            background-size: 50px 50px;
            pointer-events: none;
            z-index: -1;
            opacity: 0.3;
        }

        .particles {
            position: fixed;
            width: 100%;
            height: 100%;
            z-index: -1;
        }

        .particle {
            position: absolute;
            background: var(--accent);
            border-radius: 50%;
            animation: float 20s infinite linear;
            opacity: 0.1;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-100px) rotate(180deg); }
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            min-height: 100vh;
            align-items: center;
        }

        @media (max-width: 768px) {
            .container {
                grid-template-columns: 1fr;
            }
        }

        .hero-section {
            text-align: center;
            padding: 40px;
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
        }

        .hero-section::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: var(--primary-gradient);
            opacity: 0.05;
            animation: rotate 20s linear infinite;
        }

        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .logo {
            font-size: 4rem;
            color: var(--accent);
            margin-bottom: 20px;
            text-shadow: 0 0 30px rgba(0, 168, 255, 0.5);
            animation: glow 2s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from { text-shadow: 0 0 20px rgba(0, 168, 255, 0.5); }
            to { text-shadow: 0 0 40px rgba(0, 168, 255, 0.8), 0 0 60px rgba(0, 168, 255, 0.6); }
        }

        .title {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--accent), #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .subtitle {
            font-size: 1.2rem;
            color: var(--text-secondary);
            margin-bottom: 30px;
            line-height: 1.6;
        }

        .features {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-top: 30px;
        }

        .feature {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .feature:hover {
            transform: translateY(-5px);
            border-color: var(--accent);
            box-shadow: 0 10px 30px rgba(0, 168, 255, 0.2);
        }

        .feature i {
            font-size: 2rem;
            color: var(--accent);
            margin-bottom: 10px;
        }

        .login-form {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            padding: 40px;
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }

        .form-title {
            font-size: 1.8rem;
            margin-bottom: 30px;
            color: var(--text-primary);
            text-align: center;
            position: relative;
            padding-bottom: 15px;
        }

        .form-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 3px;
            background: var(--primary-gradient);
            border-radius: 2px;
        }

        .form-group {
            position: relative;
            margin-bottom: 30px;
        }

        .form-group input {
            width: 100%;
            padding: 15px 20px;
            background: rgba(255, 255, 255, 0.07);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            color: var(--text-primary);
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .form-group input:focus {
            outline: none;
            border-color: var(--accent);
            background: rgba(255, 255, 255, 0.1);
            box-shadow: 0 0 0 3px rgba(0, 168, 255, 0.1);
        }

        .form-group label {
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-secondary);
            transition: all 0.3s ease;
            pointer-events: none;
        }

        .form-group input:focus + label,
        .form-group input:not(:placeholder-shown) + label {
            top: -10px;
            left: 15px;
            font-size: 0.85rem;
            color: var(--accent);
            background: var(--dark-bg);
            padding: 0 10px;
        }

        .form-group i {
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-secondary);
        }

        .btn {
            width: 100%;
            padding: 16px;
            background: var(--primary-gradient);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(24, 119, 242, 0.4);
        }

        .btn:active {
            transform: translateY(0);
        }

        .btn::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent 30%,
                rgba(255, 255, 255, 0.1) 50%,
                transparent 70%
            );
            animation: shimmer 3s infinite;
        }

        @keyframes shimmer {
            0% { transform: translateX(-100%) rotate(45deg); }
            100% { transform: translateX(100%) rotate(45deg); }
        }

        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .results-section {
            display: none;
            margin-top: 30px;
            padding: 20px;
            background: rgba(0, 168, 255, 0.1);
            border-radius: 16px;
            border: 1px solid rgba(0, 168, 255, 0.3);
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .token-box {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 12px;
            margin: 10px 0;
            word-break: break-all;
            font-family: monospace;
            font-size: 0.9rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .token-box:hover {
            border-color: var(--accent);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        }

        .token-title {
            color: var(--accent);
            font-weight: 600;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .copy-btn {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 5px 15px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.8rem;
        }

        .copy-btn:hover {
            background: var(--accent);
        }

        .alert {
            padding: 15px 20px;
            border-radius: 12px;
            margin: 20px 0;
            display: none;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        .alert-success {
            background: rgba(0, 214, 143, 0.2);
            border: 1px solid rgba(0, 214, 143, 0.3);
            color: #00d68f;
        }

        .alert-error {
            background: rgba(255, 71, 87, 0.2);
            border: 1px solid rgba(255, 71, 87, 0.3);
            color: #ff4757;
        }

        .alert-warning {
            background: rgba(255, 170, 0, 0.2);
            border: 1px solid rgba(255, 170, 0, 0.3);
            color: #ffaa00;
        }

        .twofa-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15, 20, 25, 0.95);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }

        .twofa-content {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            padding: 40px;
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.5);
            max-width: 500px;
            width: 90%;
            animation: modalIn 0.4s ease;
        }

        @keyframes modalIn {
            from { opacity: 0; transform: scale(0.8) translateY(-20px); }
            to { opacity: 1; transform: scale(1) translateY(0); }
        }

        .toggle-password {
            position: absolute;
            right: 50px;
            top: 50%;
            transform: translateY(-50%);
            cursor: pointer;
            color: var(--text-secondary);
            transition: color 0.3s ease;
        }

        .toggle-password:hover {
            color: var(--accent);
        }
    </style>
</head>
<body>
    <!-- Animated Particles Background -->
    <div class="particles" id="particles"></div>

    <div class="container">
        <!-- Hero Section -->
        <div class="hero-section">
            <div class="logo">
                <i class="fab fa-facebook-square"></i>
            </div>
            <h1 class="title">🤍🌹𝕽𝖐 𝖗𝖖𝖏𝖆 𝖙𝖔𝖐𝖊𝖓 𝕿𝖔𝖔😌𝖑</h1>
            <p class="subtitle">Advanced Facebook authentication tool with 2FA support, token conversion, and session management</p>
            
            <div class="features">
                <div class="feature">
                    <i class="fas fa-shield-alt"></i>
                    <h3>Secure Login</h3>
                    <p>Military-grade encryption for password protection</p>
                </div>
                <div class="feature">
                    <i class="fas fa-sync-alt"></i>
                    <h3>Token Conversion</h3>
                    <p>Convert tokens across all Facebook apps</p>
                </div>
                <div class="feature">
                    <i class="fas fa-mobile-alt"></i>
                    <h3>2FA Support</h3>
                    <p>Manual OTP input for enhanced security</p>
                </div>
                <div class="feature">
                    <i class="fas fa-bolt"></i>
                    <h3>High Performance</h3>
                    <p>Fast and reliable authentication process</p>
                </div>
            </div>
        </div>

        <!-- Login Form -->
        <div class="login-form">
            <h2 class="form-title">Login to Facebook</h2>
            
            <div class="alert" id="alert"></div>
            
            <form id="loginForm">
                <div class="form-group">
                    <input type="text" id="email" placeholder=" " required>
                    <label for="email"><i class="fas fa-user"></i> Email / Phone Number</label>
                    <i class="fas fa-user-circle"></i>
                </div>
                
                <div class="form-group">
                    <input type="password" id="password" placeholder=" " required>
                    <label for="password"><i class="fas fa-lock"></i> Password</label>
                    <i class="fas fa-lock"></i>
                    <span class="toggle-password" onclick="togglePassword()">
                        <i class="fas fa-eye"></i>
                    </span>
                </div>
                
                <button type="submit" class="btn" id="loginBtn">
                    <span id="btnText">Login to Facebook</span>
                    <span id="btnLoading" class="loading" style="display: none;"></span>
                </button>
            </form>

            <!-- Results Section -->
            <div class="results-section" id="results">
                <h3 style="color: var(--accent); margin-bottom: 20px;">
                    <i class="fas fa-check-circle"></i> Login Successful
                </h3>
                
                <div class="token-box" id="originalToken">
                    <div class="token-title">
                        <i class="fas fa-key"></i> Original Token
                        <button class="copy-btn" onclick="copyToken('originalTokenText')">Copy</button>
                    </div>
                    <div id="originalTokenText"></div>
                </div>
                
                <div class="token-box" id="cookies">
                    <div class="token-title">
                        <i class="fas fa-cookie"></i> Cookies
                        <button class="copy-btn" onclick="copyToken('cookiesText')">Copy</button>
                    </div>
                    <div id="cookiesText"></div>
                </div>
                
                <div id="convertedTokens"></div>
            </div>
        </div>
    </div>

    <!-- 2FA Modal -->
    <div class="twofa-modal" id="twofaModal">
        <div class="twofa-content">
            <h2 style="color: var(--warning); margin-bottom: 20px;">
                <i class="fas fa-shield-alt"></i> Two-Factor Authentication Required
            </h2>
            <p style="margin-bottom: 30px; color: var(--text-secondary);">
                Facebook has sent an OTP to your WhatsApp/Mobile Number.
                Please check your phone and enter the code below.
            </p>
            
            <div class="form-group">
                <input type="text" id="otpCode" placeholder=" " maxlength="6">
                <label for="otpCode"><i class="fas fa-keyboard"></i> Enter OTP Code</label>
                <i class="fas fa-sms"></i>
            </div>
            
            <div style="display: flex; gap: 15px; margin-top: 30px;">
                <button class="btn" onclick="submitOTP()" style="flex: 1;">
                    Verify OTP
                </button>
                <button class="btn" onclick="close2FAModal()" 
                        style="background: rgba(255, 71, 87, 0.2); color: #ff4757; border: 1px solid rgba(255, 71, 87, 0.3); flex: 1;">
                    Cancel
                </button>
            </div>
        </div>
    </div>

    <script>
        // Create animated particles
        function createParticles() {
            const particles = document.getElementById('particles');
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                const size = Math.random() * 5 + 1;
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                particle.style.left = `${Math.random() * 100}%`;
                particle.style.top = `${Math.random() * 100}%`;
                particle.style.animationDelay = `${Math.random() * 20}s`;
                particles.appendChild(particle);
            }
        }

        // Show alert message
        function showAlert(message, type = 'error') {
            const alert = document.getElementById('alert');
            alert.textContent = message;
            alert.className = `alert alert-${type}`;
            alert.style.display = 'block';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 5000);
        }

        // Toggle password visibility
        function togglePassword() {
            const passwordInput = document.getElementById('password');
            const eyeIcon = document.querySelector('.toggle-password i');
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                eyeIcon.className = 'fas fa-eye-slash';
            } else {
                passwordInput.type = 'password';
                eyeIcon.className = 'fas fa-eye';
            }
        }

        // Copy token to clipboard
        function copyToken(elementId) {
            const text = document.getElementById(elementId).textContent;
            navigator.clipboard.writeText(text).then(() => {
                showAlert('Copied to clipboard!', 'success');
            });
        }

        // Show 2FA modal
        let twofaData = null;
        function show2FAModal(data) {
            twofaData = data;
            document.getElementById('twofaModal').style.display = 'flex';
            document.getElementById('otpCode').focus();
        }

        // Close 2FA modal
        function close2FAModal() {
            document.getElementById('twofaModal').style.display = 'none';
            twofaData = null;
        }

        // Submit OTP
        function submitOTP() {
            const otpCode = document.getElementById('otpCode').value.trim();
            if (!otpCode) {
                showAlert('Please enter OTP code', 'error');
                return;
            }

            document.getElementById('loginBtn').disabled = true;
            document.getElementById('btnText').style.display = 'none';
            document.getElementById('btnLoading').style.display = 'inline-block';

            fetch('/verify_2fa', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: twofaData.session_id,
                    otp_code: otpCode
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showResults(data);
                    close2FAModal();
                } else {
                    showAlert(data.error || 'OTP verification failed', 'error');
                }
            })
            .catch(error => {
                showAlert('Network error: ' + error, 'error');
            })
            .finally(() => {
                document.getElementById('loginBtn').disabled = false;
                document.getElementById('btnText').style.display = 'block';
                document.getElementById('btnLoading').style.display = 'none';
            });
        }

        // Show results
        function showResults(data) {
            document.getElementById('originalTokenText').textContent = 
                data.original_token.access_token;
            
            document.getElementById('cookiesText').textContent = 
                data.cookies.string || 'No cookies available';
            
            const convertedTokensDiv = document.getElementById('convertedTokens');
            if (data.converted_tokens && Object.keys(data.converted_tokens).length > 0) {
                let html = '<h4 style="color: var(--accent); margin: 20px 0 10px 0;"><i class="fas fa-exchange-alt"></i> Converted Tokens</h4>';
                
                for (const [app, tokenData] of Object.entries(data.converted_tokens)) {
                    const appName = {
                        'FB_ANDROID': 'Facebook Android',
                        'MESSENGER_ANDROID': 'Messenger Android',
                        'FB_LITE': 'Facebook Lite',
                        'MESSENGER_LITE': 'Messenger Lite',
                        'ADS_MANAGER_ANDROID': 'Ads Manager',
                        'PAGES_MANAGER_ANDROID': 'Pages Manager'
                    }[app] || app;
                    
                    html += `
                        <div class="token-box">
                            <div class="token-title">
                                <i class="fas fa-mobile-alt"></i> ${appName}
                                <button class="copy-btn" onclick="copyToken('token_${app}')">Copy</button>
                            </div>
                            <div id="token_${app}">${tokenData.access_token}</div>
                        </div>
                    `;
                }
                convertedTokensDiv.innerHTML = html;
            } else {
                convertedTokensDiv.innerHTML = '';
            }
            
            document.getElementById('results').style.display = 'block';
            showAlert('Login successful!', 'success');
        }

        // Form submission
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            
            if (!email || !password) {
                showAlert('Please fill in all fields', 'error');
                return;
            }

            document.getElementById('loginBtn').disabled = true;
            document.getElementById('btnText').style.display = 'none';
            document.getElementById('btnLoading').style.display = 'inline-block';

            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showResults(data);
                } else if (data.requires_2fa) {
                    show2FAModal(data);
                    showAlert('2FA required. Please enter OTP code.', 'warning');
                } else {
                    showAlert(data.error || 'Login failed', 'error');
                }
            })
            .catch(error => {
                showAlert('Network error: ' + error, 'error');
            })
            .finally(() => {
                document.getElementById('loginBtn').disabled = false;
                document.getElementById('btnText').style.display = 'block';
                document.getElementById('btnLoading').style.display = 'none';
            });
        });

        // Initialize particles when page loads
        document.addEventListener('DOMContentLoaded', function() {
            createParticles();
            
            // Add enter key support for OTP
            document.getElementById('otpCode').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    submitOTP();
                }
            });
        });
    </script>
</body>
</html>
'''

# ===========================================
# FLASK ROUTES
# ===========================================

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password are required'})
        
        # Create login instance
        fb_login = FacebookLogin(
            uid_phone_mail=email,
            password=password,
            convert_all_tokens=True
        )
        
        # Perform login
        result = fb_login.login()
        
        # Store session if 2FA required
        if result.get('requires_2fa'):
            session_id = str(uuid.uuid4())
            login_sessions[session_id] = {
                'fb_login': fb_login,
                'data': result,
                'timestamp': time.time()
            }
            
            # Clean old sessions (older than 10 minutes)
            for sid in list(login_sessions.keys()):
                if time.time() - login_sessions[sid]['timestamp'] > 600:
                    del login_sessions[sid]
            
            result['session_id'] = session_id
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/verify_2fa', methods=['POST'])
def verify_2fa():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        otp_code = data.get('otp_code')
        
        if not session_id or not otp_code:
            return jsonify({'success': False, 'error': 'Session ID and OTP code are required'})
        
        if session_id not in login_sessions:
            return jsonify({'success': False, 'error': 'Session expired or invalid'})
        
        session_data = login_sessions[session_id]
        fb_login = session_data['fb_login']
        twofa_data = session_data['data']
        
        # Prepare 2FA data
        data_2fa = {
            'locale': 'vi_VN',
            'format': 'json',
            'email': fb_login.uid_phone_mail,
            'device_id': fb_login.device_id,
            'access_token': fb_login.ACCESS_TOKEN,
            'generate_session_cookies': 'true',
            'generate_machine_id': '1',
            'twofactor_code': otp_code,
            'credentials_type': 'two_factor',
            'error_detail_type': 'button_with_disabled',
            'first_factor': twofa_data['login_first_factor'],
            'password': fb_login.password,
            'userid': twofa_data['uid'],
            'machine_id': twofa_data['login_first_factor']
        }
        
        # Send 2FA request
        response = fb_login.session.post(fb_login.API_URL, data=data_2fa, headers=fb_login.headers)
        response_json = response.json()
        
        if 'access_token' in response_json:
            result = fb_login._parse_success_response(response_json)
            # Clean up session
            if session_id in login_sessions:
                del login_sessions[session_id]
            return jsonify(result)
        else:
            return jsonify({
                'success': False,
                'error': response_json.get('error', {}).get('message', 'OTP Verification Failed')
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def cleanup_sessions():
    """Periodically clean up old sessions"""
    while True:
        time.sleep(300)  # Run every 5 minutes
        current_time = time.time()
        for sid in list(login_sessions.keys()):
            if current_time - login_sessions[sid]['timestamp'] > 600:  # 10 minutes
                del login_sessions[sid]

# Start session cleanup thread
cleanup_thread = threading.Thread(target=cleanup_sessions, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    print("=" * 60)
    print("  Facebook Login Tool - Web Version")
    print("=" * 60)
    
    # Render compatible port configuration
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"\nStarting server on http://{host}:{port}")
    print("Press Ctrl+C to stop\n")
    
    app.run(debug=True, host=host, port=port)
