api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

    # === DEBUG: Xem version SDK và list models thực tế ===
    st.write("**SDK version:**", genai.__version__)
    try:
        models = genai.list_models()
        available = [m.name for m in models if "generateContent" in m.supported_generation_methods]
        st.write("**Models khả dụng:**", available)
    except Exception as e:
        st.warning(f"Lỗi list models: {e}")

    # === SỬA MODEL Ở ĐÂY ===
    model = genai.GenerativeModel("gemini-flash-latest")        # ← Ưu tiên dùng cái này
    # model = genai.GenerativeModel("gemini-2.5-flash")         # ← Hoặc thử cái này nếu trên không chạy

    # Phần upload và button giữ nguyên như code bạn đang có...
    uploaded_files = st.file_uploader("Tải ảnh báo cáo OCT lên...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        images = []
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            images.append(image)
            st.image(image, caption=f"Ảnh OCT: {uploaded_file.name}", use_container_width=True)

        if st.button("🔍 Phân tích OCT"):
            with st.spinner("Đang phân tích báo cáo OCT..."):
                try:
                    prompt = """Bạn là chuyên gia nhãn khoa..."""  # prompt của bạn giữ nguyên

                    response = model.generate_content([prompt] + images)
                    st.subheader("📋 Kết quả phân tích OCT")
                    st.markdown(response.text)
                    st.caption("App phân tích OCT - BSCK2 Lê Hồng Hà")
                except Exception as e:
                    st.error(f"Lỗi API: {str(e)}")
else:
    st.warning("Vui lòng thêm GEMINI_API_KEY vào Secrets")
