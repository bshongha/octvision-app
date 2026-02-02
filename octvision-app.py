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
                    prompt = """Bạn là chuyên gia nhãn khoa với 20 năm kinh nghiệm, chuyên phân tích OCT cho bệnh glaucoma và võng mạc. Hãy phân tích hình ảnh OCT đính kèm theo các bước sau (Chain of Thought):

1. **Quan sát tổng quát**: Mô tả loại OCT (e.g., RNFL, GCC, Macula, Disc) và chất lượng hình (signal strength, artifact nếu có).

2. **Trích xuất thông số chính**: Đọc chính xác từ hình, không đoán:
   - RNFL thickness: Average, Temporal, Superior, Nasal, Inferior (μm, với color code xanh/vàng/đỏ).
   - GCC/GCIPL thickness: Average, sectors (Superior, Inferior, etc.) (μm).
   - ONH parameters: Cup/Disc ratio (horizontal/vertical), Rim area, Disc area.
   - Khác: Signal strength/Quality (e.g., 8/10), Asymmetry giữa hai mắt nếu có.

3. **Phân tích chẩn đoán**:
   - Có dấu hiệu glaucoma? (Thinning RNFL/GCC <5th percentile, focal loss, asymmetry >10μm). Nếu có, mức độ: Mild (RNFL avg >80μm), Moderate (60-80μm), Severe (<60μm).
   - Các tổn thương khác: AMD (drusen, RPE irregularity), DME (cystoid edema), Macular hole (full-thickness defect), ERM (membrane hyperreflective), v.v. Lý do từng dấu hiệu.
   - Tương quan: So sánh với norm database trong hình (e.g., below normal in red areas).

4. **Tóm tắt ngắn gọn**: 1-2 câu chính, e.g., "OCT cho thấy thinning RNFL superior, nghi glaucoma moderate ở mắt phải."

5. **Đề xuất**:
   - Cận lâm sàng tiếp theo: VF Humphrey nếu nghi glaucoma, Fundus photo/FA nếu nghi AMD, Pachymetry đo CCT, Gonioscopy kiểm góc, MRI nếu nghi optic neuropathy.
   - Phác đồ điều trị gợi ý: Nếu glaucoma mild - theo dõi IOP + thuốc nhỏ prostaglandin (e.g., Latanoprost qhs); moderate - laser SLT; severe - phẫu thuật trabeculectomy. Nếu khác, tham khảo chuyên khoa (e.g., tiêm anti-VEGF cho DME).

Lưu ý: Chỉ dựa vào hình ảnh, không thêm giả định. Kết quả tham khảo, khuyến nghị khám bác sĩ nhãn khoa ngay.
Output theo định dạng Markdown rõ ràng, dùng bullet points cho từng phần."""
                    response = model.generate_content([prompt] + images)
                    st.subheader("📋 Kết quả phân tích OCT")
                    st.markdown(response.text)
                    st.caption("App phân tích OCT - BSCK2 Lê Hồng Hà")
                except Exception as e:
                    st.error(f"Lỗi API: {str(e)}")
else:
    st.warning("Vui lòng thêm GEMINI_API_KEY vào Secrets")
