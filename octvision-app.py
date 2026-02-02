import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="GlaucoVision OCT Analyzer", layout="centered")
st.title("🛠️ GlaucoVision OCT Analyzer")

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
    
    model = genai.GenerativeModel("gemini-1.5-flash")  # Sửa thành model chuẩn, không -latest

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
                       - Color coding (xanh/vàng/đỏ) ở các vùng quan trọng

                    2. **Chẩn đoán & Phân loại**:
                       - Có tổn thương glaucoma không? (thinning RNFL/GCC, asymmetry, focal loss)
                       - Nếu có, ước lượng mức độ: Mild / Moderate / Severe
                       - Các tổn thương khác (nếu có): AMD, DME, macular hole, ERM, vitreomacular traction, drusen, CSR, optic neuropathy, v.v.

                    3. **Tóm tắt ngắn gọn** (1-2 câu): Tình trạng chính là gì?

                    4. **Đề xuất**:
                       - Cận lâm sàng cần làm tiếp theo (VF, pachymetry, gonioscopy, fundus photo, FA, MRI...).
                       - Hướng điều trị / phác đồ gợi ý (theo giai đoạn nếu là glaucoma).

                    Lưu ý: Đây chỉ là hỗ trợ, không thay thế chẩn đoán bác sĩ.
                    """

                    response = model.generate_content([prompt] + images)
                    st.subheader("📋 Kết quả phân tích OCT")
                    st.markdown(response.text)
                    st.caption("App phân tích OCT - BSCK2 Lê Hồng Hà")
                except Exception as e:
                    st.error(f"Lỗi API: {str(e)}")
else:
    st.warning("Vui lòng thêm GEMINI_API_KEY vào Secrets")
