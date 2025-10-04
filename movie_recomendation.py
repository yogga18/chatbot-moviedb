import streamlit as st
from google import genai

# --- Page Configuration ---
st.set_page_config(
    page_title="CineBot - Movie Recommendation AI",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 CineBot")
st.caption("Asisten AI Pribadimu untuk Rekomendasi Film & TV Series (Optimized Token Usage)")

# --- Sidebar ---
with st.sidebar:
    st.subheader("⚙️ Settings")
    google_api_key = st.text_input("Google AI API Key", type="password")
    reset_button = st.button("🔄 Reset Conversation", help="Clear all messages and start fresh")
    
    st.markdown("---")
    
    # --- Generation Parameters ---
    st.subheader("🎛️ Response Settings")
    
    temperature = st.slider(
        "🌡️ Temperature (Creativity)", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.7,  # Sweet spot untuk rekomendasi
        step=0.1,
        help="Lower = more focused, Higher = more creative"
    )
    
    max_tokens = st.selectbox(
        "📏 Max Response Length",
        options=[256, 512, 1024, 2048],
        index=1,  # Default 512 tokens
        help="Maximum length of AI response"
    )
    
    top_p = st.slider(
        "🎯 Top-p (Nucleus Sampling)",
        min_value=0.1,
        max_value=1.0,
        value=0.9,  # Good balance
        step=0.1,
        help="Controls diversity of word selection"
    )
    
    top_k = st.slider(
        "🔢 Top-k (Token Selection)",
        min_value=1,
        max_value=100,
        value=40,  # Standard value
        step=5,
        help="Number of top tokens to consider"
    )
    
    st.markdown("---")
    
    # --- Token Usage Info ---
    st.subheader("📊 Token Usage")
    estimated_tokens_per_response = max_tokens
    estimated_total = estimated_tokens_per_response * 6  # Max 3 conversations (6 messages)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Per Response", f"{estimated_tokens_per_response:,}")
    with col2:
        st.metric("Total (3 conv.)", f"{estimated_total:,}")
    
    # Calculate cost estimation (approximate)
    cost_per_1k_tokens = 0.00015  # Gemini Flash pricing (approximate)
    estimated_cost = (estimated_total / 1000) * cost_per_1k_tokens
    st.metric("Est. Cost ($)", f"${estimated_cost:.6f}")
    
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
        st.success("✅ API Client initialized successfully!")
    except Exception as e:
        st.error(f"❌ Invalid API Key: {e}")
        st.stop()

# --- System Prompt for Movie Expert ---
MOVIE_EXPERT_PROMPT = f"""
Kamu adalah CineBot, seorang ahli film dan database movie terbaik di dunia dengan pengetahuan mendalam tentang:

🎬 **KEAHLIAN UTAMA:**
- Seluruh film dari tahun 1890-2024 (klasik hingga terbaru)
- TV Series, Drama, Anime, Documentary, dan semua format audio-visual
- Cast, crew, sutradara, produser, dan semua orang di industri film
- Genre, sub-genre, dan klasifikasi film yang detail
- Rating dari berbagai platform (IMDb, Rotten Tomatoes, Metacritic, dll)
- Box office, budget, dan aspek bisnis film
- Festival film, penghargaan (Oscar, Golden Globe, Cannes, dll)
- Platform streaming (Netflix, HBO, Disney+, Prime Video, Viu, iQiyi, dll)

🎯 **GAYA KOMUNIKASI:**
- Ramah, antusias, dan mudah dipahami
- Berikan rekomendasi yang personal dan relevan
- Sertakan rating, tahun rilis, genre, dan cast utama
- Jelaskan mengapa film/series tersebut cocok untuk user
- Berikan alternatif jika user tidak suka dengan rekomendasi

📋 **FORMAT JAWABAN (WAJIB DIIKUTI):**
1. **🎯 Rekomendasi Utama** (1-3 judul)
2. **📝 Detail Singkat** (plot, cast, rating)
3. **✨ Mengapa Cocok** untuk user
4. **📺 Platform** streaming yang tersedia
5. **🔄 Alternatif** lain (opsional)

🚫 **BATASAN PENTING:**
- HANYA jawab tentang film, TV series, dan industri entertainment
- Jika ditanya di luar topik, katakan: "Maaf, saya hanya ahli film dan rekomendasi tontonan 🎬"
- MAKSIMAL {max_tokens} tokens per response
- Prioritaskan informasi penting dan relevan
- Jawab dengan ringkas, padat, dan jelas

🎬 Ready to help with the best movie recommendations!
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
        "film", "movie", "tontonan", "cinema", "bioskop", "layar lebar", "box office", "sinema",
        
        # Jenis konten
        "serial", "series", "tv show", "drama", "anime", "anim", "cartoon", "animation",
        "documentary", "docuseries", "sitcom", "miniseries", "season", "episode", "web series",
        
        # Orang
        "aktor", "aktris", "pemeran", "cast", "bintang film", "sutradara", "director",
        "produser", "penulis naskah", "screenwriter", "cinematographer", "aktor utama",
        "aktor pendukung", "cameo", "artis", "selebriti", "celebrity",
        
        # Aspek film
        "genre", "rekomendasi", "rating", "review", "ulasan", "trailer", "soundtrack",
        "poster", "sinopsis", "alur cerita", "plot", "premis", "karakter", "tokoh",
        "visual effect", "vfx", "cinematography", "durasi", "rilis", "tayang", "premiere",
        
        # Platform streaming
        "netflix", "hbo", "hbo max", "disney", "disney+", "prime video", "amazon prime",
        "hulu", "apple tv", "apple tv+", "paramount+", "peacock", "viu", "iflix", "iqiyi",
        "youtube", "youtube premium", "crunchyroll", "funimation", "wakanim",
        
        # Penghargaan
        "oscar", "academy award", "golden globe", "bafta", "cannes", "sundance",
        "festival film", "piala citra", "ffi", "emmy", "sag awards"
    ]
    
    q = query.lower()
    return any(kw in q for kw in keywords)

def create_movie_expert_chat():
    """Create a new chat session with movie expert system prompt and generation config."""
    
    # Generation configuration for consistent, focused responses
    generation_config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_tokens,
        "response_mime_type": "text/plain",
    }
    
    try:
        # Try to create chat with generation config
        chat = st.session_state.genai_client.chats.create(
            model="gemini-2.5-flash"  # Updated to latest model
        )
        
        # Send system prompt as first message to establish expertise
        chat.send_message(MOVIE_EXPERT_PROMPT)
        return chat
        
    except Exception as e:
        # Fallback: create chat without config if not supported
        st.warning(f"⚠️ Using fallback configuration: {str(e)[:100]}...")
        try:
            chat = st.session_state.genai_client.chats.create(model="gemini-2.5-flash")
            chat.send_message(MOVIE_EXPERT_PROMPT)
            return chat
        except Exception as e2:
            st.error(f"❌ Chat creation failed: {e2}")
            return None

# --- Session State Management ---
if "chat" not in st.session_state:
    st.session_state.chat = create_movie_expert_chat()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_tokens_used" not in st.session_state:
    st.session_state.total_tokens_used = 0

# Handle reset button
if reset_button:
    st.session_state.pop("chat", None)
    st.session_state.pop("messages", None)
    st.session_state.total_tokens_used = 0
    st.session_state.chat = create_movie_expert_chat()
    st.rerun()

# Apply history limit
st.session_state.messages = limit_chat_history(st.session_state.messages)

# --- Display Past Messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Display conversation count in sidebar
if st.session_state.messages:
    conversation_count = len(st.session_state.messages) // 2
    with st.sidebar:
        st.markdown("---")
        st.subheader("💬 Chat Status")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Conversations", f"{conversation_count}/3")
        with col2:
            st.metric("Messages", len(st.session_state.messages))

# --- Chat Input ---
prompt = st.chat_input("🎬 Tanyakan rekomendasi film, series, atau apapun tentang dunia entertainment...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Domain validation
    if not is_movie_related(prompt):
        answer = """
        🎬 **Maaf, saya hanya ahli film dan rekomendasi tontonan!**
        
        Silakan tanyakan tentang:
        - Rekomendasi film atau TV series
        - Informasi aktor, sutradara, atau cast
        - Rating dan review film
        - Platform streaming
        - Genre dan kategori film
        - Penghargaan dan festival film
        
        Apa yang ingin Anda tanyakan tentang dunia entertainment? 🍿
        """
    else:
        try:
            # Reset chat if history too long
            if len(st.session_state.messages) > 6:
                st.session_state.chat = create_movie_expert_chat()
                recent_messages = limit_chat_history(st.session_state.messages[:-1], 2)
                for msg in recent_messages:
                    if msg["role"] == "user":
                        st.session_state.chat.send_message(msg["content"]) # type: ignore

            # Send message with spinner for better UX
            with st.spinner("🎬 Mencari rekomendasi terbaik untuk Anda..."):
                response = st.session_state.chat.send_message(prompt) # type: ignore
                answer = response.text if hasattr(response, "text") else str(response)
                
                # Estimate tokens used (rough approximation)
                estimated_tokens = len(answer.split()) * 1.3  # Rough token estimation
                st.session_state.total_tokens_used += estimated_tokens

        except Exception as e:
            answer = f"""
            ❌ **Terjadi kesalahan saat memproses permintaan Anda**
            
            **Error:** {str(e)[:200]}...
            
            **Saran:**
            - Pastikan API key Anda valid
            - Coba refresh halaman
            - Coba dengan pertanyaan yang lebih sederhana
            
            Silakan coba lagi! 🔄
            """

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(answer)

    # Add assistant message and apply limits
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.messages = limit_chat_history(st.session_state.messages)

# --- Footer Info in Sidebar ---
with st.sidebar:
    st.markdown("---")
    st.subheader("📋 Current Configuration")
    
    config_info = f"""
    **🌡️ Temperature:** {temperature}  
    **📏 Max Tokens:** {max_tokens:,}  
    **🎯 Top-p:** {top_p}  
    **🔢 Top-k:** {top_k}  
    
    **💰 Cost Estimation:**
    - Per response: ~${(max_tokens/1000)*cost_per_1k_tokens:.6f}
    - Total (3 conv.): ~${estimated_cost:.6f}
    """
    
    st.markdown(config_info)
    
    # Performance indicator
    if st.session_state.messages:
        avg_response_length = sum(len(msg["content"]) for msg in st.session_state.messages if msg["role"] == "assistant") // max(1, len([msg for msg in st.session_state.messages if msg["role"] == "assistant"]))
        st.metric("Avg Response Length", f"{avg_response_length} chars")

# --- Quick Tips at Bottom ---
if not st.session_state.messages:
    st.markdown("---")
    st.subheader("💡 Tips untuk Mendapatkan Rekomendasi Terbaik")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎯 Spesifik Genre:**
        - "Film action terbaru 2024"
        - "Drama Korea romantis"
        - "Anime dengan rating tinggi"
        """)
    
    with col2:
        st.markdown("""
        **👥 Based on Preference:**
        - "Film seperti Inception"
        - "Series mirip Breaking Bad"
        - "Film Tom Hanks terbaik"
        """)
    
    with col3:
        st.markdown("""
        **📺 Platform Spesifik:**
        - "Film bagus di Netflix"
        - "Series HBO terbaik"
        - "Anime di Crunchyroll"
        """)