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
                    prompt = """Bạn là chuyên gia nhãn khoa với 20 năm kinh nghiệm, chuyên OCT glaucoma và võng mạc. Phân tích hình OCT đính kèm theo Chain of Thought (nghĩ từng bước):

1. **Bước 1: Quan sát tổng quát**: Xác định loại scan (RNFL, GCC, Macula, Disc), chất lượng (signal strength ước tính nếu không có, artifact như blur/noise).

2. **Bước 2: Trích xuất thông số chính**: Đọc chính xác từ hình nếu có số; nếu không, ước tính dựa trên hình thái (e.g., thickness ~300μm nếu thickening). Bao gồm:
   - RNFL: Average + quadrants (μm, color: xanh bình thường, vàng borderline, đỏ bất thường).
   - GCC/GCIPL: Average + sectors.
   - ONH: C/D ratio, rim/disc area.
   - Signal/Quality: Số hoặc ước tính.
   - Color coding: Mô tả vùng xanh/vàng/đỏ/đen (fluid).

3. **Bước 3: Phân tích chẩn đoán**: Lý do từng bước.
   - Glaucoma: Thinning RNFL/GCC <5th percentile, asymmetry >10μm, focal loss – mức độ mild/moderate/severe dựa trên RNFL avg (>80/60-80/<60μm).
   - Khác: CSR (SRF dome-shaped), CME (cystoid spaces), AMD (drusen/RPE irregularity), Macular hole (break layers), ERM (hyperreflective membrane), etc.

4. **Bước 4: Tóm tắt ngắn gọn**: 1-2 câu chính.

5. **Bước 5: Đề xuất**:
   - Cận lâm sàng: VF cho glaucoma, FA cho CSR/AMD, MRI nếu nghi u.
   - Phác đồ: Glaucoma – thuốc IOP (prostaglandin qhs); CSR – theo dõi/PDT; CME – anti-VEGF/steroid.

Lưu ý: Nếu hình raw (không số), ước tính dựa trên hình thái học. Chỉ dựa vào hình, không đoán ngoài. Kết quả tham khảo, khám bác sĩ ngay.

Output Markdown: Sử dụng headings cho từng bước, bullet cho thông số."""
                    response = model.generate_content([prompt] + images)
                    st.subheader("📋 Kết quả phân tích OCT")
                    st.markdown(response.text)
                    st.caption("App phân tích OCT - BSCK2 Lê Hồng Hà")
                except Exception as e:
                    st.error(f"Lỗi API: {str(e)}")
else:
    st.warning("Vui lòng thêm GEMINI_API_KEY vào Secrets")
