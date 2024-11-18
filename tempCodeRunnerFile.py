from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import nbformat
from nbformat import read, NO_CONVERT

# Set your API key
os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

app = Flask(__name__)

# Initialize the model
model = genai.GenerativeModel("models/gemini-pro")

# Function to generate recommendations
def generate_recommendation(dietary_preferences, fitness_goals, lifestyle_factors, dietary_restrictions,
                            health_conditions, user_query):
    prompt = f"""
    Can you suggest a comprehensive plan that includes diet and workout options for better fitness?
    for this user:
    dietary preferences: {dietary_preferences},
    fitness goals: {fitness_goals},
    lifestyle factors: {lifestyle_factors},
    dietary restrictions: {dietary_restrictions},
    health conditions: {health_conditions},
    user query: {user_query},

    Based on the above user’s dietary preferences, fitness goals, lifestyle factors, dietary restrictions, and health conditions provided, create a customized plan that includes:

    Diet Recommendations: RETURN LIST
    5 specific diet types suited to their preferences and goals.

    Workout Options: RETURN LIST
    5 workout recommendations that align with their fitness level and goals.

    Meal Suggestions: RETURN LIST
    5 breakfast ideas.

    5 dinner options.

    Additional Recommendations: RETURN LIST
    Any useful snacks, supplements, or hydration tips tailored to their profile.
    """

    response = model.generate_content(prompt)
    return response.text if response else "No response from the model."

@app.route('/')
def index():
    return render_template('index.html', recommendations=None)

@app.route('/recommendations', methods=['POST'])
def recommendations():
    if request.method == "POST":
        # Collect form data
        dietary_preferences = request.form['dietary_preferences']
        fitness_goals = request.form['fitness_goals']
        lifestyle_factors = request.form['lifestyle_factors']
        dietary_restrictions = request.form['dietary_restrictions']
        health_conditions = request.form['health_conditions']
        user_query = request.form['user_query']

        # Generate recommendations using the model
        recommendations_text = generate_recommendation(
            dietary_preferences, fitness_goals, lifestyle_factors, dietary_restrictions, health_conditions, user_query
        )

        # Parse the results for display
        recommendations = {
            "diet_types": [],
            "workouts": [],
            "breakfasts": [],
            "dinners": [],
            "additional_tips": []
        }

        print("text : ", recommendations_text)

        # Split and map responses based on keywords
        current_section = None
        for line in recommendations_text.splitlines():
            if "Diet Recommendations:" in line:
                current_section = "diet_types"
            elif "Workout Options:" in line:
                current_section = "workouts"
            elif "Meal Suggestions:" in line:
                current_section = "breakfasts"
            elif "Dinner Options:" in line:
                current_section = "dinners"
            elif "Additional Recommendations:" in line:
                current_section = "additional_tips"
            elif line.strip() and current_section:
                recommendations[current_section].append(line.strip())
                
        print("dict : ", recommendations)
        return render_template('index.html', recommendations=recommendations)

def read_ipynb(file_path):
    """Reads and parses the contents of a Jupyter Notebook."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        return notebook
    except Exception as e:
        return {"error": str(e)}

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    if not file.filename.endswith('.ipynb'):
        return "Invalid file type. Please upload a .ipynb file", 400

    try:
        # Read and parse the .ipynb file
        notebook = read(file.stream, as_version=NO_CONVERT)

        # Extract content from the notebook
        content = "\n".join(cell.source for cell in notebook.cells if cell.cell_type == 'markdown' or cell.cell_type == 'code')

        # Generate recommendations using the model
        recommendations_text = generate_recommendation(
            dietary_preferences="", fitness_goals="", lifestyle_factors="", dietary_restrictions="", health_conditions="", user_query=content
        )

        # Parse the results for display
        recommendations = {
            "diet_types": [],
            "workouts": [],
            "breakfasts": [],
            "dinners": [],
            "additional_tips": []
        }

        print("text : ", recommendations_text)

        # Split and map responses based on keywords
        current_section = None
        for line in recommendations_text.splitlines():
            if "Diet Recommendations:" in line:
                current_section = "diet_types"
            elif "Workout Options:" in line:
                current_section = "workouts"
            elif "Meal Suggestions:" in line:
                current_section = "breakfasts"
            elif "Dinner Options:" in line:
                current_section = "dinners"
            elif "Additional Recommendations:" in line:
                current_section = "additional_tips"
            elif line.strip() and current_section:
                recommendations[current_section].append(line.strip())

        print("dict : ", recommendations)
        return render_template('index.html', recommendations=recommendations)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
