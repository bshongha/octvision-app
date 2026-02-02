import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Cấu hình giao diện và thương hiệu
st.set_page_config(page_title="AI OCT Analyzer - Dr. Hong Ha", layout="wide")
st.title("👁️ AI OCT Analyzer - BSCK2 Lê Hồng Hà")
st.markdown("---")

# 2. Quản lý API Key bảo mật
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        # Cấu hình Google Generative AI
        genai.configure(api_key=api_key)
        
        # Khai báo model (Dùng định danh chuẩn để tránh lỗi 404)
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

        # Giao diện tải file
        uploaded_files = st.file_uploader(
            "Tải ảnh báo cáo OCT (RNFL, GCC, Macula, Disc...)", 
            type=["jpg", "jpeg", "png"], 
            accept_multiple_files=True
        )

        if uploaded_files:
            images = []
            cols = st.columns(len(uploaded_files))
            for idx, uploaded_file in enumerate(uploaded_files):
                image = Image.open(uploaded_file)
                images.append(image)
                with cols[idx]:
                    st.image(image, caption=f"Ảnh: {uploaded_file.name}", use_container_width=True)

            if st.button("🚀 Bắt đầu Phân tích Chuyên sâu"):
                with st.spinner("Bác sĩ vui lòng đợi trong giây lát, AI đang phân tích dữ liệu OCT..."):
                    try:
                        # PROMPT TỐI ƯU HÓA CHUYÊN GIA (Chain of Thought)
                        prompt = """Bạn là chuyên gia nhãn khoa với 20 năm kinh nghiệm, chuyên phân tích OCT cho bệnh glaucoma và võng mạc. 
                        Hãy phân tích hình ảnh OCT đính kèm theo các bước sau:

                        1. **Quan sát tổng quát**: Mô tả loại OCT (e.g., RNFL, GCC, Macula, Disc) và chất lượng hình (signal strength, artifact nếu có).
                        2. **Trích xuất thông số chính**: Đọc chính xác từ hình, không đoán:
                           - RNFL thickness: Average, Temporal, Superior, Nasal, Inferior (μm, kèm mã màu xanh/vàng/đỏ nếu thấy).
                           - GCC/GCIPL thickness: Average, các phân vùng (μm).
                           - ONH parameters: Cup/Disc ratio (H/V), Rim area, Disc area.
                           - Đối chiếu: Signal strength, Asymmetry giữa hai mắt.
                        3. **Phân tích chẩn đoán**:
                           - Dấu hiệu glaucoma? (Thinning RNFL/GCC <5th percentile, focal loss, asymmetry >10μm). 
                           - Phân loại mức độ: Mild (RNFL avg >80μm), Moderate (60-80μm), Severe (<60μm).
                           - Các tổn thương khác: AMD (drusen, RPE), DME (cystoid edema), Macular hole, ERM. Lý do dựa trên hình ảnh.
                        4. **Tóm tắt chuyên môn**: 1-2 câu ngắn gọn kết luận tình trạng chính.
                        5. **Đề xuất lâm sàng**:
                           - Cận lâm sàng: VF Humphrey, Fundus photo, Pachymetry, Gonioscopy.
                           - Hướng điều trị gợi ý: Thuốc (Prostaglandin), Laser (SLT), hay Phẫu thuật (Trabeculectomy).

                        Lưu ý: Chỉ dựa vào hình ảnh cung cấp. Kết quả mang tính chất tham khảo y khoa.
                        Định dạng Output: Markdown chuyên nghiệp, dùng bullet points."""

                        # Gọi API với cấu hình ổn định nhất
                        response = model.generate_content([prompt] + images)
                        
                        # Hiển thị kết quả
                        st.success("Phân tích hoàn tất!")
                        st.markdown(response.text)
                        
                        # Chữ ký thương hiệu
                        st.markdown("---")
                        st.info("💡 **App phân tích thị trường - BSCK2 Lê Hồng Hà**")
                        
                    except Exception as e:
                        st.error(f"Lỗi khi xử lý dữ liệu: {str(e)}")
                        st.info("Mẹo: Hãy thử nhấn 'Reboot App' trong bảng điều khiển Streamlit.")
    except Exception as e:
        st.error(f"Lỗi hệ thống: {str(e)}")
else:
    st.warning("⚠️ Chưa tìm thấy API Key. Bác sĩ hãy dán 'GEMINI_API_KEY' vào mục Settings > Secrets của Streamlit.")
