import streamlit as st
from google import genai

st.title("💬 Movie Recommendation Chatbot")
st.caption("A simple and friendly chat using Google's Gemini Flash model (Max 3 chat history)")

# --- Sidebar ---
with st.sidebar:
    st.subheader("Settings")
    google_api_key = st.text_input("Google AI API Key", type="password")
    reset_button = st.button("Reset Conversation", help="Clear all messages and start fresh")
    st.info("💡 History limited to 3 conversations to save tokens", icon="ℹ️")

# --- API Key Check ---
if not google_api_key:
    st.info("Please add your Google AI API key in the sidebar to start chatting.", icon="🗝️")
    st.stop()

# --- Client Initialization ---
if ("genai_client" not in st.session_state) or (getattr(st.session_state, "_last_key", None) != google_api_key):
    try:
        st.session_state.genai_client = genai.Client(api_key=google_api_key)
        st.session_state._last_key = google_api_key
        st.session_state.pop("chat", None)
        st.session_state.pop("messages", None)
    except Exception as e:
        st.error(f"Invalid API Key: {e}")
        st.stop()

# --- System Prompt for Movie Expert ---
MOVIE_EXPERT_PROMPT = """
Kamu adalah seorang ahli film dan database movie terbaik di dunia dengan pengetahuan mendalam tentang:

🎬 **KEAHLIAN UTAMA:**
- Seluruh film dari tahun 1890-2024 (klasik hingga terbaru)
- TV Series, Drama, Anime, Documentary, dan semua format audio-visual
- Cast, crew, sutradara, produser, dan semua orang di industri film
- Genre, sub-genre, dan klasifikasi film yang detail
- Rating dari berbagai platform (IMDb, Rotten Tomatoes, Metacritic, dll)
- Box office, budget, dan aspek bisnis film
- Festival film, penghargaan (Oscar, Golden Globe, Cannes, dll)
- Platform streaming (Netflix, HBO, Disney+, Prime Video, dll)

🎯 **GAYA KOMUNIKASI:**
- Ramah, antusias, dan mudah dipahami
- Berikan rekomendasi yang personal dan relevan
- Sertakan rating, tahun rilis, genre, dan cast utama
- Jelaskan mengapa film/series tersebut cocok untuk user
- Berikan alternatif jika user tidak suka dengan rekomendasi

📋 **FORMAT JAWABAN:**
Selalu struktur jawaban dengan:
1. **Rekomendasi Utama** (1-3 film/series)
2. **Detail singkat** (plot, cast, rating)
3. **Mengapa cocok** untuk user
4. **Platform** dimana bisa ditonton
5. **Rekomendasi tambahan** jika ada
6. ** Jawab dengan ringkas, padat, dan jelas **

🚫 **BATASAN:**
- HANYA jawab tentang film, TV series, dan industri entertainment
- Jika ditanya di luar topik, katakan: "Maaf, saya hanya ahli film dan rekomendasi tontonan 🎬"

Mulai setiap percakapan dengan semangat dan siap memberikan rekomendasi terbaik!
"""

# --- Helper Functions ---
def limit_chat_history(messages, max_conversations=3):
    """Limit chat history to max_conversations (user+assistant pairs)."""
    max_messages = max_conversations * 2
    return messages[-max_messages:] if len(messages) > max_messages else messages

def is_movie_related(query: str) -> bool:
    """
    Validasi apakah query masih dalam domain MovieDB.
    Menggunakan daftar kata kunci yang lebih luas.
    """
    keywords = [
        # Umum
        "film", "movie", "tontonan", "cinema", "bioskop", "layar lebar", "box office",
        
        # Jenis konten
        "serial", "series", "tv show", "drama", "anime", "anim", "cartoon", "animation",
        "documentary", "docuseries", "sitcom", "miniseries", "season", "episode",
        
        # Orang
        "aktor", "aktris", "pemeran", "cast", "bintang film", "sutradara", "director",
        "produser", "penulis naskah", "screenwriter", "cinematographer", "aktor utama",
        "aktor pendukung", "cameo",
        
        # Aspek film
        "genre", "rekomendasi", "rating", "review", "ulasan", "trailer", "soundtrack",
        "poster", "sinopsis", "alur cerita", "plot", "premis", "karakter", "tokoh",
        "visual effect", "vfx", "cinematography", "durasi", "rilis", "tayang",
        
        # Platform streaming
        "netflix", "hbo", "hbo max", "disney", "disney+", "prime video", "amazon prime",
        "hulu", "apple tv", "apple tv+", "paramount+", "peacock", "viu", "iflix",
        
        # Penghargaan
        "oscar", "academy award", "golden globe", "bafta", "cannes", "sundance",
        "festival film", "piala citra"
    ]
    
    q = query.lower()
    return any(kw in q for kw in keywords)

def create_movie_expert_chat():
    """Create a new chat session with movie expert system prompt."""
    chat = st.session_state.genai_client.chats.create(model="gemini-2.5-flash")
    # Send system prompt as first message to establish expertise
    chat.send_message(MOVIE_EXPERT_PROMPT)
    return chat

# --- Session State ---
if "chat" not in st.session_state:
    st.session_state.chat = create_movie_expert_chat()

if "messages" not in st.session_state:
    st.session_state.messages = []

if reset_button:
    st.session_state.pop("chat", None)
    st.session_state.pop("messages", None)
    st.session_state.chat = create_movie_expert_chat()
    st.rerun()

st.session_state.messages = limit_chat_history(st.session_state.messages)

# --- Display Past Messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.session_state.messages:
    conversation_count = len(st.session_state.messages) // 2
    with st.sidebar:
        st.text(f"Current conversations: {conversation_count}/3")

# --- Chat Input ---
prompt = st.chat_input("Tanyakan rekomendasi film atau series...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Domain Validation ---
    if not is_movie_related(prompt):
        answer = "Maaf, saya hanya ahli film dan rekomendasi tontonan 🎬. Silakan tanyakan tentang film, series, atau apapun yang berhubungan dengan dunia entertainment!"
    else:
        try:
            # Reset chat if history too long
            if len(st.session_state.messages) > 6:
                st.session_state.chat = create_movie_expert_chat()
                recent_messages = limit_chat_history(st.session_state.messages[:-1], 2)
                for msg in recent_messages:
                    if msg["role"] == "user":
                        st.session_state.chat.send_message(msg["content"])

            response = st.session_state.chat.send_message(prompt)
            answer = response.text if hasattr(response, "text") else str(response)

        except Exception as e:
            answer = f"An error occurred: {e}"

    # --- Display Assistant Response ---
    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.messages = limit_chat_history(st.session_state.messages)