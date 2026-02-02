import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Cấu hình giao diện
st.set_page_config(page_title="AI OCT Analyzer - Dr. Hong Ha", layout="wide")
st.title("👁️ AI OCT Analyzer - BSCK2 Lê Hồng Hà")

# 2. Quản lý API Key
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # GIẢI PHÁP ĐẶC TRỊ: Ép sử dụng v1 thay vì v1beta
        # Chúng ta dùng tham số 'models/gemini-1.5-flash' kèm cấu hình nội bộ
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        uploaded_files = st.file_uploader("Tải ảnh báo cáo OCT...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

        if uploaded_files:
            images = []
            for uploaded_file in uploaded_files:
                image = Image.open(uploaded_file)
                images.append(image)
                st.image(image, caption=uploaded_file.name, width=300)

            if st.button("🚀 Phân tích Chuyên sâu"):
                with st.spinner("AI đang phân tích..."):
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

                        # CÁCH GỌI HÀM ÉP PHIÊN BẢN V1
                        response = model.generate_content(
                            [prompt] + images,
                            request_options={"api_version": "v1"}
                        )
                        
                        st.subheader("📋 Kết quả phân tích OCT")
                        st.markdown(response.text)
                        st.divider()
                        st.info("App phân tích OCT - BSCK2 Lê Hồng Hà")
                        
                    except Exception as e:
                        # Nếu vẫn lỗi, thử cách gọi dự phòng không có options
                        try:
                            response = model.generate_content([prompt] + images)
                            st.markdown(response.text)
                        except:
                            st.error(f"Lỗi API (404/v1beta): {str(e)}")
                            st.info("💡 Mẹo cuối cùng: Hãy kiểm tra file requirements.txt xem đã có 'google-generativeai' chưa.")
    except Exception as e:
        st.error(f"Lỗi hệ thống: {str(e)}")
else:
    st.warning("Vui lòng cấu hình GEMINI_API_KEY trong Secrets.")
