import streamlit as st
import google.generativeai as genai
from PIL import Image
import pypdf

# Page Config
st.set_page_config(page_title="Govt Exam MCQ Generator", page_icon="📝")

st.title("📝 Govt Exam MCQ Generator")
st.caption("RRB | SSC | NTA Exam Special")

# API Key Setup
api_key = st.text_input("अपनी Gemini API Key यहाँ डालें:", type="password")

SYSTEM_PROMPT = """
Role & Task:
आप मेरे निष्पक्ष (strict) Exam Paper Setter हैं। मैं आपको कोई इमेज (फोटो) या फिर पूरी PDF (पूरा चैप्टर) अपलोड करके दे सकता हूँ। आपको दिए गए कंटेंट को ध्यान से एनालाइज करना है और RRB, SSC, NTA व अन्य कॉम्पिटिटिव एग्जाम्स के लेटेस्ट पैटर्न के अनुसार परीक्षा-उपयोगी MCQs तैयार करने हैं।

Strict Rules:
1. Exam-Oriented Filtering: फालतू/गैर-जरूरी बातों पर सवाल न बनाएं। केवल वही प्रश्न बनाएं जो RRB, SSC, NTA एग्जाम्स में पूछे जाने लायक हों।
2. Question Estimate First: सबसे पहले बताएं कि इस इमेज/PDF से एग्जाम के दृष्टिकोण से कुल कितने उपयोगी और यूनिक (Unique) MCQs बन सकते हैं।
3. No Question Repetition: किसी भी प्रश्न या कॉन्सेप्ट को दोबारा न दोहराएं।
4. Ignore Figure/Diagram Labels: "चित्र 1.1 देखें" या डायग्राम नंबर पर आधारित बेतुके सवाल न बनाएं। केवल कांसेप्ट/फैक्ट पर ही सवाल बनाएं।
5. Zero External Knowledge in MCQs: प्रश्न और विकल्प केवल दिए गए कंटेंट पर ही आधारित होने चाहिए।

Output Format:
[शुरुआती विश्लेषण]
"इस कंटेंट से एग्जाम के दृष्टिकोण (RRB/SSC/NTA) से अधिकतम [X] उपयोगी यूनिक MCQs बन सकते हैं।"

[भाग 1: परीक्षा उपयोगी प्रश्न]
* प्रश्न (Question)
* (A) ऑप्शन 1  
* (B) ऑप्शन 2  
* (C) ऑप्शन 3  
* (D) ऑप्शन 4  

[भाग 2: Answer Key]
(सभी प्रश्नों के सही उत्तर यहाँ दें)

[भाग 3: अतिरिक्त जानकारी (Extra Knowledge)]
अगर इस टॉपिक से जुड़ी कोई महत्वपूर्ण जानकारी इमेज में नहीं है लेकिन एग्जाम के लिए जरूरी है, तो उन्हें "कंटेंट से अलग / एक्स्ट्रा पॉइंट्स" के रूप में बुलेट पॉइंट्स में लिखें।
"""

uploaded_file = st.file_uploader("Image या PDF अपलोड करें", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file and st.button("🚀 MCQs बनाएं", type="primary"):
    if not api_key:
        st.error("कृपया अपनी Gemini API Key डालें!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            file_type = uploaded_file.name.split(".")[-1].lower()
            
            with st.spinner("एनालाइज किया जा रहा है..."):
                if file_type in ["jpg", "jpeg", "png"]:
                    image = Image.open(uploaded_file)
                    response = model.generate_content([SYSTEM_PROMPT, image])
                else:
                    pdf_reader = pypdf.PdfReader(uploaded_file)
                    pdf_text = "".join([page.extract_text() or "" for page in pdf_reader.pages])
                    response = model.generate_content(f"{SYSTEM_PROMPT}\n\n[PDF CONTENT]\n{pdf_text}")
                
                st.markdown("---")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {str(e)}")
