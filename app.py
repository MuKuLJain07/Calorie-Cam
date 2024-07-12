import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# loading environment variables
load_dotenv()

# configuring google-gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])

    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        byteData = uploaded_file.getvalue()

        image_part = [
            {
                "mime_type": uploaded_file.type,
                "data": byteData
            }
        ]

        return image_part
    else:
        raise FileNotFoundError("Image file not found!")
    


# streamlit app

# Set the page configuration
st.set_page_config(
    page_title="CalorieCam",
    page_icon=":camera:",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# Add a title and description
st.title("📸 Calorie-Cam")
st.write("""
### Upload your image file
This app allows you to upload image files and submit them for processing. 
Supported formats: JPG, PNG, JPEG, WEBP.
""")

# Add some space
st.markdown("##")

# Create a file uploader for images
uploaded_file = st.file_uploader(
    "Choose an image file",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=False,
    help="Upload a single image file in JPG, JPEG, PNG, or WEBP format."
)

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)



# Add some space
st.markdown("##")


# Create a submit button
if st.button("Submit", type="primary") and uploaded_file is not None:
    input_prompt = '''
    You are an expert nutritionist. Your task is to identify all the food items present in the provided image
    and provide the total calorie count of the food. You also need to provide details of each food item 
    individually in the below format.

    1. Item 1 : no of calorie contribution of the item in the total image
    2. Item 2 : no of calorie contribution of the item in the total image
    -----
    -----


    Finally give you final verdict whether the food is healthy or not and also mention the percentage split of
    the ratio of protein, carbohydrates, fats, vitamins, minerals and fibres along with the actual quantity of that nutrient.
    
    Ex -
    Protein : 30gm (5%)
    Carbohydrate : 100gm(20%)
    ----
    ----
    

    You can also suggest some good additions to this diet to make it healthy or suggest some related healthy recipe
    '''

    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.write(response)
else:
    st.warning("Please upload a file before submitting.")

# Add a footer
st.markdown("""
    <style>
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px; /* Adjust as needed */
    }
    </style>
    <div class="centered">
        Calorie-Cam | Developed with Mr. Mukul Jain
    </div>
""", unsafe_allow_html=True)

