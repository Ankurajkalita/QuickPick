import streamlit as st
import ollama
import json
from datetime import datetime

def generate_recipe(ingredients, ration, dietary_preferences, cuisine_type, cooking_time, complexity_level, health_goals):
    prompt = (
        f"Generate a personalized recipe using the following ingredients: {', '.join(ingredients)}. "
        f"Consider a {ration} ration plan with a focus on {cuisine_type} cuisine. "
        f"Ensure the recipe aligns with the following dietary preferences: {', '.join(dietary_preferences)}. "
        f"Limit the cooking time to {cooking_time} minutes and keep it {complexity_level} in difficulty. "
        f"Optimize the recipe for these health goals: {', '.join(health_goals)}. "
        "Provide a step-by-step cooking process, estimated preparation time, and nutritional breakdown."
    )
    
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

def save_recipe(recipe):
    """Generates a downloadable text file for the recipe."""
    file_name = "generated_recipe.txt"
    with open(file_name, "w") as file:
        file.write(recipe)
    return file_name



def generate_shopping_list(ingredients, recipe):
    prompt = (
        f"Based on the following recipe: {recipe}, and given ingredients: {', '.join(ingredients)}, "
        "generate a shopping list of additional ingredients required to complete the recipe."
    )
    
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

# Streamlit UI
st.set_page_config(page_title="Welcome to QuickPick Recipes", layout="wide")
st.title("🍽️ Welcome to QuickPick Recipes")

# Sidebar for user input
st.sidebar.header("User Preferences")

ingredients = st.text_area("Enter available ingredients (comma-separated)")
ration = st.sidebar.selectbox("Select your ration period", ["Daily", "Weekly", "Monthly"])
dietary_preferences = st.sidebar.multiselect("Select dietary preferences", ["Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo", "Low-Carb", "High-Protein"])
cuisine_type = st.sidebar.selectbox("Select preferred cuisine", ["Italian", "Mexican", "Indian", "Chinese", "Mediterranean", "American", "Thai", "Japanese"])
cooking_time = st.sidebar.slider("Maximum Cooking Time (minutes)", min_value=5, max_value=120, value=30, step=5)
complexity_level = st.sidebar.radio("Select Complexity Level", ["Easy", "Medium", "Hard"])
health_goals = st.sidebar.multiselect("Select Health Goals", ["Weight Loss", "Muscle Gain", "Heart Health", "Diabetes-Friendly", "Immunity Boost", "Balanced Nutrition"])

# Generate recipe button
if st.sidebar.button("Generate Recipe"):
    if ingredients:
        ingredient_list = [i.strip() for i in ingredients.split(",")]
        recipe = generate_recipe(ingredient_list, ration, dietary_preferences, cuisine_type, cooking_time, complexity_level, health_goals)
        
        st.subheader("📜 Generated Recipe:")
        st.markdown(recipe)
        st.caption(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

         # Save Recipe Feature
        file_name = save_recipe(recipe)
        with open(file_name, "r") as file:
            st.download_button(label="📥 Download Recipe", data=file, file_name=file_name, mime="text/plain")
        
        st.caption(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        

    else:
        st.sidebar.warning("Please enter at least one ingredient.")


# Function to add background image
def add_bg_from_local():
    bg_image = "https://images.unsplash.com/photo-1592457711340-2412dc07b733?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        f"""
        <style>
        .stApp {{
            background-image: url({bg_image});
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local()
