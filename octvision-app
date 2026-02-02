import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="OCTVision AI", layout="centered")
st.title("👁️ OCTVision Analyzer")
st.caption("Phân tích báo cáo OCT RNFL, GCC, Macula, Disc – BSCK2 Lê Hồng Hà")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.sidebar.warning("Vui lòng cấu hình GEMINI_API_KEY trong Secrets")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")   # model nhanh + chính xác với hình OCT

uploaded_files = st.file_uploader(
    "Upload báo cáo OCT (có thể nhiều ảnh cùng lúc)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    # Hiển thị tất cả ảnh
    for file in uploaded_files:
        image = Image.open(file)
        st.image(image, caption=file.name, use_container_width=True)

    if st.button("🔍 Phân tích OCT", type="primary"):
        with st.spinner('Đang phân tích bằng Gemini-1.5-Flash...'):
            images = [Image.open(f) for f in uploaded_files]
            
            prompt = """Bạn là BSCK2 chuyên khoa Glaucoma & Võng mạc. 
            Phân tích toàn bộ ảnh OCT (có thể là chuỗi theo dõi) với cấu trúc rõ ràng, ngắn gọn:

            1. Trích xuất thông số chính (bắt buộc có):
               - Signal Strength
               - Average RNFL, RNFL 4 quadrants + 12 clock-hours
               - GCC average + FLV%, GLV%
               - Macula thickness (nếu có)
               - ONH parameters: Disc area, Rim area, C/D ratio, Cup volume

            2. Nhận xét bất thường:
               - Mỏng RNFL ở vị trí nào? So với norm? Deviation map ra sao?
               - Tổn thương GCC? Macula? Đĩa thị?
               - Phù hợp glaucoma mức độ nào (suspect / early / moderate / severe) theo tiêu chuẩn HPA/IOPCC?

            3. Đánh giá tiến triển (nếu có ≥2 lần OCT):
               - Mỏng thêm bao nhiêu μm/năm ở RNFL/GCC?
               - Tốc độ tiến triển nhanh/chậm?

            4. Chẩn đoán gợi ý ngắn gọn (glaucoma / NTG / bệnh lý võng mạc / khác)

            5. Đề xuất cận lâm sàng tiếp theo (ví dụ: thị trường 24-2, fundus photo, gonioscopy, OCT lặp lại sau bao lâu…)

            6. Hướng điều trị/phác đồ cụ thể (ví dụ: nhãn áp mục tiêu ≤ ? mmHg, thuốc nào đầu tay, khi nào laser/phẫu thuật…)

            Viết bằng tiếng Việt, ngắn gọn, dùng gạch đầu dòng, dễ đọc cho bác sĩ lâm sàng.
            Lưu ý: Đây chỉ là hỗ trợ AI, không thay thế đánh giá bác sĩ.
            """

            response = model.generate_content([prompt] + images)
            
            st.subheader("Kết quả phân tích")
            st.markdown(response.text)
            st.markdown("---")
            st.markdown("**OCTVision AI – BSCK2 Lê Hồng Hà**")
