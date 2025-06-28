import streamlit as st
import os
import shutil
from predict_equation import predict_equation
from equation_solver import evaluate_equation

st.set_page_config(page_title="Handwritten Equation Solver")

st.title("Handwritten Equation Solver")
st.markdown("Upload an image of a handwritten math equation. We'll recognize and solve it for you!")

uploaded_file = st.file_uploader("Upload PNG Image", type=["png"])

if uploaded_file is not None:
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    image_path = os.path.join("uploads", uploaded_file.name)

    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(image_path, caption="Uploaded Equation Image", use_container_width=True)

    with st.spinner("Prediction in progress..."):
        predicted_equation = predict_equation(image_path)
        solution = evaluate_equation(predicted_equation)

    st.success("Prediction complete!")

    st.subheader("Predicted Equation:")
    st.code(predicted_equation, language="markdown")

    st.subheader("Solution:")
    st.code(solution, language="markdown")

    shutil.rmtree("uploads")
