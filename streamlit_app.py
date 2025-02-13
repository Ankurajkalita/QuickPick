import streamlit as st
import ollama
import json
from datetime import datetime

# Function to generate a recipe
def generate_recipe(ingredients, ration, dietary_preferences, cuisine_type, cooking_time, complexity_level, health_goals):
    """Generates a personalized recipe based on user preferences."""
    
    prompt = (
        f"Generate a personalized recipe using the following ingredients: {', '.join(ingredients)}. "
        f"Consider a {ration} ration plan with a focus on {cuisine_type} cuisine. "
        f"Ensure the recipe aligns with the following dietary preferences: {', '.join(dietary_preferences)}. "
        f"Limit the cooking time to {cooking_time} minutes and keep it {complexity_level} in difficulty. "
        f"Optimize the recipe for these health goals: {', '.join(health_goals)}. "
        "Provide a step-by-step cooking process, estimated preparation time, and nutritional breakdown."
    )

    try:
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        return response.get("message", {}).get("content", "⚠️ No response from AI. Try again.")
    except Exception as e:
        return f"⚠️ Error generating recipe: {str(e)}"

# Function to save recipe as a text file
def save_recipe(recipe):
    """Generates a downloadable text file for the recipe."""
    file_name = "generated_recipe.txt"
    with open(file_name, "w") as file:
        file.write(recipe)
    return file_name

# Streamlit UI
st.set_page_config(page_title="QuickPick Recipes", layout="wide")
st.markdown("🍽️ <h1 style='color: white;'>Welcome to QuickPick Recipes</h1>", unsafe_allow_html=True)

# Sidebar for user input
st.sidebar.header("User Preferences")

ingredients = st.text_area("Enter available ingredients (comma-separated)")
ration = st.sidebar.selectbox("Select your ration period", ["Daily", "Weekly", "Monthly"])
dietary_preferences = st.sidebar.multiselect("Select dietary preferences", ["Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo", "Low-Carb", "High-Protein"])
cuisine_type = st.sidebar.selectbox("Select preferred cuisine", ["Italian", "Mexican", "Indian", "Chinese", "Mediterranean", "American", "Thai", "Japanese"])
cooking_time = st.sidebar.slider("Maximum Cooking Time (minutes)", min_value=5, max_value=120, value=30, step=5)
complexity_level = st.sidebar.radio("Select Complexity Level", ["Easy", "Medium", "Hard"])
health_goals = st.sidebar.multiselect("Select Health Goals", ["Weight Loss", "Muscle Gain", "Heart Health", "Diabetes-Friendly", "Immunity Boost", "Balanced Nutrition"])

# Fix for Threading Issue: Use session state
if "recipe_output" not in st.session_state:
    st.session_state.recipe_output = ""

# Generate Recipe Button
if st.sidebar.button("Generate Recipe"):
    if ingredients.strip():
        ingredient_list = [i.strip() for i in ingredients.split(",")]
        st.session_state.recipe_output = generate_recipe(ingredient_list, ration, dietary_preferences, cuisine_type, cooking_time, complexity_level, health_goals)

# Display Recipe if generated
if st.session_state.recipe_output:
    st.subheader("📜 Generated Recipe:")
    st.markdown(st.session_state.recipe_output)

    # Save and Download Recipe
    file_name = save_recipe(st.session_state.recipe_output)
    with open(file_name, "r") as file:
        st.download_button(label="📥 Download Recipe", data=file, file_name=file_name, mime="text/plain")

    st.caption(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Function to add background image
def add_bg_from_local():
    bg_image = "https://images.unsplash.com/photo-1592457711340-2412dc07b733?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    st.markdown(
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
