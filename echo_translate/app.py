import streamlit as st
import asyncio
import edge_tts
import speech_recognition as sr
from fpdf import FPDF
import os
import io
import zipfile
import requests
from streamlit_mic_recorder import mic_recorder

# Sayfa Yapılandırması
st.set_page_config(page_title="Echo-Translate AI Pro", page_icon="🎤", layout="wide")

# Tasarım ve Başlık
st.title("🎤 Echo-Translate: Gelişmiş Sesli Tercüman")
st.markdown("""
**Echo-Translate**, yapay zeka destekli anlık sesli çeviri asistanıdır. 
Tarayıcınız üzerinden sesinizi kaydeder, istediğiniz dile tercüme eder, seslendirir ve çıktıları indirmenize imkan tanır.
""")

# Yan Menü (Ayarlar)
st.sidebar.header("⚙️ Ayarlar")

# Dil Seçenekleri
LANGUAGES = {
    "Türkçe": {"code": "tr", "voice": "tr-TR"},
    "İngilizce": {"code": "en", "voice": "en-US"},
    "Fransızca": {"code": "fr", "voice": "fr-FR"},
    "Almanca": {"code": "de", "voice": "de-DE"},
    "İspanyolca": {"code": "es", "voice": "es-ES"},
    "İtalyanca": {"code": "it", "voice": "it-IT"},
    "Arapça": {"code": "ar", "voice": "ar-SA"},
    "Portekizce": {"code": "pt", "voice": "pt-BR"},
    "Rusça": {"code": "ru", "voice": "ru-RU"},
    "Çince": {"code": "zh-cn", "voice": "zh-CN"},
    "Japonca": {"code": "ja", "voice": "ja-JP"}
}

source_lang_name = st.sidebar.selectbox("Kaynak Dil (Siz konuşun):", list(LANGUAGES.keys()), index=0)
target_lang_name = st.sidebar.selectbox("Hedef Dil (Tercüme):", list(LANGUAGES.keys()), index=1)

source_lang_info = LANGUAGES[source_lang_name]
target_lang_info = LANGUAGES[target_lang_name]

VOICE_NAMES = [
    "Zeynep (Kadın)", "Can (Erkek)", "Elif (Kadın)", "Emir (Erkek)", 
    "Derya (Kadın)", "Mert (Erkek)", "Selin (Kadın)", "Arda (Erkek)", 
    "Nil (Kadın)", "Bora (Erkek)"
]
selected_voice_name = st.sidebar.selectbox("Ses Tonu Seçin:", VOICE_NAMES)

async def get_edge_voices(language_code, gender):
    voices = await edge_tts.VoicesManager.create()
    target_voices = voices.find(Locale=language_code, Gender=gender)
    if not target_voices:
        target_voices = voices.find(Locale=language_code)
    return target_voices

async def synthesize_audio(text, voice_id, output_path):
    communicate = edge_tts.Communicate(text, voice_id)
    await communicate.save(output_path)

def translate_text(text, source_lang_code, target_lang_code):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang_code}&tl={target_lang_code}&dt=t&q={text}"
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            translated_text = "".join([part[0] for part in result[0]])
            return translated_text
        return f"Çeviri Hatası (Status: {response.status_code})"
    except Exception as e:
        return f"Hata: {str(e)}"

def create_pdf(original_text, translated_text, source_lang, target_lang):
    pdf = FPDF()
    pdf.add_page()
    font_path = r"C:\Windows\Fonts\arial.ttf"
    if os.path.exists(font_path):
        pdf.add_font("ArialUni", "", font_path)
        pdf.set_font("ArialUni", size=14)
    else:
        pdf.set_font("Helvetica", size=14)
    pdf.cell(200, 10, txt="Echo-Translate AI - Transkript", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"Kaynak Dil ({source_lang}): {original_text}")
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=f"Hedef Dil ({target_lang}): {translated_text}")
    return bytes(pdf.output())

def create_zip(mp3_content, pdf_content):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr("tercume_ses_kaydi.mp3", mp3_content)
        zip_file.writestr("tercume_transkript.pdf", pdf_content)
    return zip_buffer.getvalue()

def process_audio(audio_bytes):
    r = sr.Recognizer()
    audio_file = io.BytesIO(audio_bytes)
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
        try:
            # Sesi Metne Çevir
            text = r.recognize_google(audio_data, language=source_lang_info["code"])
            st.success(f"🎙️ Söylenen: {text}")

            # Tercüme Et
            translated_result = translate_text(text, source_lang_info["code"], target_lang_info["code"])
            st.write(f"🌐 Çeviri ({target_lang_name}): {translated_result}")

            # Ses Sentezleme
            gender = "Female" if "Kadın" in selected_voice_name else "Male"
            voices = asyncio.run(get_edge_voices(target_lang_info["voice"], gender))
            voice_index = (VOICE_NAMES.index(selected_voice_name) // 2) % len(voices)
            voice_id = voices[voice_index]['Name']
            
            output_file = "output.mp3"
            asyncio.run(synthesize_audio(translated_result, voice_id, output_file))
            st.audio(output_file, format="audio/mp3")

            # Kaydet
            pdf_bytes = create_pdf(text, translated_result, source_lang_name, target_lang_name)
            with open(output_file, "rb") as f:
                mp3_bytes = f.read()
            
            st.session_state['zip_data'] = create_zip(mp3_bytes, pdf_bytes)
            st.session_state['ready'] = True
        except Exception as e:
            st.error(f"⚠️ Bir hata oluştu: {e}")

# Ana Bölüm - Mikrofon Kaydı
st.subheader("🎙️ Kayda Başlayın")
audio_record = mic_recorder(
    start_prompt="🔴 Kaydı Başlat",
    stop_prompt="⬛ Kaydı Durdur",
    key='recorder',
    use_container_width=True
)

if audio_record:
    process_audio(audio_record['bytes'])

# İndirme Butonu
if 'ready' in st.session_state and st.session_state['ready']:
    st.divider()
    st.download_button(
        label="📥 Tüm Çıktıları İndir (MP3 + PDF)",
        data=st.session_state['zip_data'],
        file_name="echo_translate_paket.zip",
        mime="application/zip",
        use_container_width=True
    )

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Powered by Google Translate & Microsoft Edge TTS")
st.markdown("<br><br><br><br><hr><div style='text-align: center; color: gray;'>Designed by © 2026 Nejdet Tut</div>", unsafe_allow_html=True)
