import streamlit as st  # Import ở đầu tiên
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="GlaucoVision OCT Analyzer", layout="centered")
st.title("🛠️ GlaucoVision OCT Analyzer")

# Debug: Kiểm tra nếu secrets có load OK
st.write("**Debug: Secrets loaded?**", "GEMINI_API_KEY" in st.secrets)  # Nên hiển thị True nếu key có

api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    
    # Debug: List models khả dụng để xem và chọn đúng
    try:
        models = genai.list_models()
        available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
        st.write("Models khả dụng (debug):")
        st.write(available_models)
    except Exception as e:
        st.warning(f"Lỗi list models: {str(e)}")
    
    model = genai.GenerativeModel("gemini-1.5-flash")  # Giữ model này, hoặc thay từ list debug
    
    uploaded_files = st.file_uploader("Tải ảnh báo cáo OCT lên (Cirrus, Spectralis, Topcon, Avanti...)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if uploaded_files:
        images = []
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            images.append(image)
            st.image(image, caption=f"Ảnh OCT: {uploaded_file.name}", use_container_width=True)
        
        if st.button("🔍 Phân tích OCT"):
            with st.spinner("Đang phân tích báo cáo OCT..."):
                try:
                    prompt = """Bạn là chuyên gia nhãn khoa giàu kinh nghiệm. Hãy phân tích báo cáo OCT này một cách chi tiết, logic và có hệ thống:
                    1. **Trích xuất thông số chính** (đọc chính xác các con số):
                       - RNFL thickness (average + 4 quadrants)
                       - GCC / GCIPL thickness (average + sectors)
                       - ONH parameters (Cup/Disc ratio, Rim area, Disc area, Vertical CDR)
                       - Signal strength / Quality index
                       - Color coding (xanh/vàng/
