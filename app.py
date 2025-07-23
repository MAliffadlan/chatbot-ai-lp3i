import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import library CORS
from dotenv import load_dotenv

# Muat environment variable dari file .env
load_dotenv()

# Konfigurasi Flask App
app = Flask(__name__)

CORS(app)

# Konfigurasi Gemini API dengan kunci dari .env
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY tidak ditemukan di file .env Anda.")
        model = None
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Error saat mengkonfigurasi Gemini API: {e}")
    model = None

# Route untuk menyajikan halaman utama chatbot (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk "jembatan" ke Gemini API
@app.route('/api/generate', methods=['POST'])
def api_generate():
    if model is None:
        return jsonify({"error": "Model AI tidak terkonfigurasi. Periksa kunci API di terminal server Anda."}), 500
        
    try:
        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({"error": "Request tidak valid. 'prompt' tidak ditemukan."}), 400

        prompt = data.get('prompt')
        response = model.generate_content(prompt)
        
        return jsonify({"text": response.text})

    except Exception as e:
        print(f"Error saat memanggil API: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
