# 🎬 CineBot: Chatbot Rekomendasi Film & TV

---

## 🚀 **COBA DEMO LANGSUNG!**

### 👆 **[🎬 KLIK DISINI UNTUK MENCOBA CINEBOT →](https://chatbot-moviedb.streamlit.app)**

> **💡 Demo gratis tersedia!** Cukup masukkan Google AI API Key Anda (gratis dari [Google AI Studio](https://aistudio.google.com)) dan mulai chatting tentang film favorit Anda!

---

Selamat datang di **CineBot**, sebuah chatbot cerdas yang dirancang untuk menjadi asisten pribadi Anda dalam menjelajahi dunia sinema. Ditenagai oleh model AI canggih Google Gemini, CineBot dapat memberikan rekomendasi film, menjawab pertanyaan seputar aktor, sutradara, dan memberikan informasi detail dari The Movie Database (TMDB).

## ✨ Keunggulan Utama

CineBot tidak hanya sekadar chatbot biasa. Aplikasi ini dirancang dengan beberapa fitur unggulan untuk memberikan pengalaman yang optimal dan efisien.

### 1\. 🪙 Efisiensi Penggunaan Token

Untuk menjaga kecepatan respons dan menghemat biaya API, CineBot secara cerdas **membatasi riwayat percakapan** yang dikirim ke model. Dengan hanya mengingat 3 interaksi terakhir, chatbot tetap kontekstual tanpa membebani penggunaan token.

### 2\. 🧠 Memahami Konteks Percakapan

CineBot mampu **mengikuti alur percakapan**. Anda bisa mengajukan pertanyaan lanjutan dan chatbot akan memahaminya berdasarkan respons sebelumnya, membuat interaksi terasa lebih natural dan tidak kaku.

### 3\. 🎯 Validasi Domain Berlapis

Agar jawaban selalu relevan, CineBot menerapkan **dua lapis validasi domain**:

- **Validasi Awal (Aplikasi):** Sebuah fungsi Python di sisi aplikasi melakukan pengecekan cepat berbasis kata kunci untuk menyaring pertanyaan yang jelas-jelas di luar topik film.
- **Validasi Kontekstual (LLM):** Model AI diberikan instruksi tegas untuk menolak pertanyaan di luar domain sinema, memungkinkannya menangani kasus-kasus ambigu secara cerdas.

### 4\. 🎭 Persona Ahli Film

Melalui _prompt engineering_ yang cermat, LLM diberikan **persona sebagai "CineBot"**, seorang ahli film yang ramah dan antusias. Ini memastikan setiap jawaban yang diberikan tidak hanya akurat tetapi juga konsisten dalam gaya, nada, dan format, seolah Anda sedang berbicara dengan seorang pakar sungguhan.

### 5\. 🎛️ Kontrol Parameter Generasi AI

CineBot memberikan **kontrol penuh kepada pengguna** untuk menyesuaikan cara AI merespons. Fitur-fitur yang dapat diatur meliputi:

#### **🌡️ Temperature (Kreativitas)**

- **Range:** 0.0 - 1.0
- **Default:** 0.7
- **Fungsi:** Mengontrol tingkat kreativitas AI
  - **Lower (0.0-0.3):** Respons lebih fokus dan faktual
  - **Higher (0.7-1.0):** Respons lebih kreatif dan variatif

#### **📏 Max Response Length**

- **Pilihan:** 256, 512, 1024, 2048 tokens
- **Default:** 512 tokens
- **Fungsi:** Membatasi panjang maksimal respons AI untuk efisiensi token

#### **🎯 Top-P (Nucleus Sampling)**

- **Range:** 0.1 - 1.0
- **Default:** 0.9
- **Fungsi:** Mengontrol keragaman pemilihan kata
  - **Lower:** Pemilihan kata lebih terprediksi
  - **Higher:** Pemilihan kata lebih beragam

#### **🔢 Top-K (Token Selection)**

- **Range:** 1 - 100
- **Default:** 40
- **Fungsi:** Menentukan jumlah token teratas yang dipertimbangkan

#### **📊 Real-time Usage Monitoring**

- **Token Usage Estimation:** Perkiraan penggunaan token per respons dan total
- **Cost Estimation:** Kalkulasi perkiraan biaya berdasarkan harga API Gemini
- **Conversation Counter:** Monitoring jumlah percakapan aktif (maksimal 3)

### 6\. 💰 Transparansi Biaya

CineBot menampilkan **estimasi biaya real-time** berdasarkan:

- Panjang respons yang dipilih
- Jumlah percakapan maksimal (3 conversation = 6 messages)
- Harga API Gemini Flash terkini (~$0.00015 per 1K tokens)

**Contoh Estimasi:**

- **Per Response:** 512 tokens = ~$0.000077
- **Total (3 conversations):** 3,072 tokens = ~$0.000461

## 🛠️ Teknologi yang Digunakan

- **Framework Aplikasi:** Streamlit
- **Model AI:** Google Gemini 2.5 Flash
- **Library:** `google-generativeai`, `langchain`
- **Bahasa:** Python

## � Mendapatkan Google AI API Key

**PENTING:** CineBot menggunakan Google Gemini API yang memerlukan API key pribadi. Anda perlu mendapatkan API key dari Google AI Studio.

### 📋 Langkah-langkah Mendapatkan API Key:

1. **Kunjungi Google AI Studio**

   - Buka link: **https://aistudio.google.com**
   - Login dengan akun Google Anda

2. **Buat API Key Baru**

   - Klik tombol "Get API Key" atau "Create API Key"
   - Pilih project Google Cloud atau buat yang baru
   - Copy API key yang dihasilkan

3. **Keamanan API Key**
   - ⚠️ **JANGAN** bagikan API key Anda kepada siapa pun
   - ⚠️ **JANGAN** commit API key ke repository publik
   - 💡 Simpan API key di tempat yang aman

### 💰 Informasi Biaya

- **Model:** Gemini 1.5 Flash
- **Harga:** ~$0.00015 per 1,000 tokens (sangat terjangkau)
- **Free Tier:** Google AI Studio menyediakan quota gratis untuk pengujian
- **Estimasi Penggunaan CineBot:** ~$0.0005 per sesi chat (3 percakapan)

## �🚀 Cara Menjalankan Proyek

Ikuti langkah-langkah berikut untuk menjalankan aplikasi ini di komputer lokal Anda.

1.  **Clone Repositori**

    ```bash
    git clone https://github.com/yogga18/chatbot-moviedb.git
    cd chatbot-moviedb
    ```

2.  **Buat Virtual Environment** (Direkomendasikan)

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Untuk macOS/Linux
    # .venv\Scripts\activate   # Untuk Windows
    ```

3.  **Instal Dependensi**
    Pastikan Anda memiliki file `requirements.txt`, lalu jalankan:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Aplikasi Streamlit**

    ```bash
    streamlit run movie_recomendation.py
    ```

5.  **Siapkan API Key**
    Dapatkan Google AI API Key dari [Google AI Studio](https://aistudio.google.com) (lihat section sebelumnya)

6.  **Buka Aplikasi**
    Buka browser Anda dan navigasikan ke `http://localhost:8501`. Masukkan Google AI API Key Anda di sidebar untuk memulai percakapan.

### 🔐 Memasukkan API Key di Aplikasi

1. Setelah aplikasi terbuka, lihat **sidebar di sebelah kiri**
2. Temukan field **"Google AI API Key"**
3. Paste API key yang sudah Anda dapatkan dari Google AI Studio
4. Aplikasi akan otomatis terkoneksi dan siap digunakan

> **💡 Tips:** API key akan tersimpan selama sesi browser aktif. Jika Anda menutup browser, Anda perlu memasukkan API key lagi.

## ⚙️ Cara Menggunakan Fitur Advanced

### 🎛️ Mengatur Parameter AI

1. **Buka Sidebar:** Di sebelah kiri aplikasi, temukan bagian "Response Settings"

2. **Sesuaikan Parameter:**

   - **Temperature:** Geser slider untuk mengatur kreativitas (0.7 = optimal)
   - **Max Response Length:** Pilih panjang respons yang diinginkan (512 = recommended)
   - **Top-P & Top-K:** Fine-tune untuk hasil yang lebih personal

3. **Monitor Usage:** Pantau estimasi token dan biaya di bagian "Token Usage"

### 💡 Tips Pengaturan Optimal

#### **Untuk Rekomendasi Film:**

- Temperature: 0.7-0.8 (balance kreatif & akurat)
- Max Length: 512-1024 (detail cukup)
- Top-P: 0.9 (keragaman baik)

#### **Untuk Informasi Faktual:**

- Temperature: 0.3-0.5 (lebih fokus)
- Max Length: 256-512 (ringkas)
- Top-P: 0.8 (lebih terprediksi)

#### **Untuk Diskusi Mendalam:**

- Temperature: 0.8-1.0 (kreatif)
- Max Length: 1024-2048 (detail)
- Top-P: 0.9-1.0 (sangat beragam)

## 📄 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file `LICENSE` untuk detail lebih lanjut.
