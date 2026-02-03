import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Cấu hình giao diện
st.set_page_config(page_title="AI OCT Analyzer - Dr. Hong Ha", layout="wide")
st.title("👁️ AI OCT Analyzer - BSCK2 Lê Hồng Hà")

# 2. Lấy API Key
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # SỬA LỖI 404: Khởi tạo model mà không chỉ định version ở đây
        model = genai.GenerativeModel("gemini-1.5-flash")

        uploaded_files = st.file_uploader(
            "Tải ảnh báo cáo OCT (RNFL, GCC, Macula...)", 
            type=["jpg", "jpeg", "png"], 
            accept_multiple_files=True
        )

        if uploaded_files:
            images = []
            for uploaded_file in uploaded_files:
                image = Image.open(uploaded_file)
                images.append(image)
                st.image(image, caption=f"Ảnh: {uploaded_file.name}", width=400)

            if st.button("🚀 Phân tích Chuyên sâu"):
                with st.spinner("AI đang thực hiện Chain of Thought phân tích OCT..."):
                    try:
                        prompt = """Bạn là chuyên gia nhãn khoa với 20 năm kinh nghiệm. Hãy phân tích OCT:
                        1. Quan sát tổng quát (loại OCT, chất lượng hình).
                        2. Trích xuất thông số (RNFL, GCC, ONH).
                        3. Phân tích chẩn đoán (Dấu hiệu glaucoma, mức độ, tổn thương võng mạc).
                        4. Tóm tắt và đề xuất hướng xử trí (thuốc, laser hoặc phẫu thuật).
                        Lưu ý: Chỉ dựa vào hình ảnh, kết quả mang tính tham khảo."""

                        # CƠ CHẾ DỰ PHÒNG THÔNG MINH:
                        # Thử chạy với version v1 trước để tránh lỗi 404/v1beta
                        try:
                            response = model.generate_content([prompt] + images, request_options={"api_version": "v1"})
                        except:
                            # Nếu thư viện cũ không hiểu "api_version", chạy lệnh mặc định
                            response = model.generate_content([prompt] + images)
                        
                        st.subheader("📋 Kết quả phân tích")
                        st.markdown(response.text)
                        st.divider()
                        st.info("App phân tích OCT - BSCK2 Lê Hồng Hà")
                        
                    except Exception as e:
                        st.error(f"Lỗi API: {str(e)}")
                        st.info("Mẹo: Bác sĩ hãy thử nhấn 'Reboot App' ở góc dưới bên phải.")
    except Exception as e:
        st.error(f"Lỗi hệ thống: {str(e)}")
else:
    st.sidebar.warning("Vui lòng cấu hình GEMINI_API_KEY trong mục Secrets.")
