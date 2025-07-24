import os
import requests
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Muat environment variable (untuk development lokal)
load_dotenv()

# Konfigurasi Flask App
app = Flask(__name__)
CORS(app)

# URL API untuk model AI di Hugging Face.
# Kita akan menggunakan model chat yang populer dan gratis.
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

# Ambil token rahasia dari environment variable
# Di PythonAnywhere, ini akan diambil dari file WSGI
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Fungsi untuk memanggil Hugging Face API
def query_huggingface_api(payload):
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Route untuk halaman utama (hanya untuk penanda)
@app.route('/')
def index():
    return "<h1>Backend AI LP3I (Hugging Face) Aktif</h1>"

# Route utama untuk API
@app.route('/api/generate', methods=['POST'])
def api_generate():
    if not HF_API_TOKEN:
        return jsonify({"error": "Kunci API Hugging Face tidak terkonfigurasi di server."}), 500
        
    try:
        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({"error": "Request tidak valid. 'prompt' tidak ditemukan."}), 400

        prompt = data.get('prompt')
        
        # Kirim prompt ke Hugging Face
        api_response = query_huggingface_api({
            "inputs": prompt,
        })

        # Cek jika ada error dari API
        if "error" in api_response:
             # Jika model sedang loading, beri pesan yang lebih ramah
            if "is currently loading" in api_response["error"]:
                return jsonify({"text": "Model AI sedang disiapkan, coba lagi dalam 20 detik..."})
            return jsonify({"error": api_response["error"]}), 500

        # Ambil teks dari respons API
        generated_text = api_response[0].get("generated_text", "")
        # Seringkali model mengulang prompt, kita bersihkan
        cleaned_text = generated_text.replace(prompt, "").strip()

        return jsonify({"text": cleaned_text or "Maaf, saya tidak bisa menghasilkan jawaban saat ini."})

    except Exception as e:
        print(f"Error internal: {e}")
        return jsonify({"error": str(e)}), 500

# Untuk testing lokal
if __name__ == '__main__':
    app.run(debug=True)
