import os
import google.generativeai as genai
from flask import Flask, render_template, request

# Configure Google Gemini API key
genai.configure(api_key="AIzaSyDPEmMCCaRRjpdLOCsGS3TkUz91QaG5eLQ")

# Initialize Flask app
app = Flask(__name__)

# Flask route for the main page
@app.route("/", methods=["GET", "POST"])
def index():
    pickup_lines = []
    if request.method == "POST":
        # Get user input
        topic = request.form.get("topic", "love")
        flirtiness = request.form.get("flirtiness", "5")
        
        # Validate flirtiness input
        try:
            flirtiness = int(flirtiness)
            if flirtiness < 0 or flirtiness > 10:
                flirtiness = 5  # Default to medium flirtiness
        except ValueError:
            flirtiness = 5  # Default to medium flirtiness if invalid input

        # Generate pickup lines
        pickup_lines = generate_pickup_lines(topic, flirtiness)

    return render_template("index.html", pickup_lines=pickup_lines)

# Function to generate 5 pickup lines
def generate_pickup_lines(topic, flirtiness):
    prompt_template = (
        f"Create a unique pickup line about '{topic}' with a flirtiness level of {flirtiness}/10. "
        f"Make it fun and creative!"
    )
    pickup_lines = []
    try:
        # Use Google Gemini API to generate 5 pickup lines
        model = genai.GenerativeModel("gemini-1.5-flash")
        for _ in range(5):
            response = model.generate_content(prompt_template)
            if hasattr(response, 'text') and response.text:
                pickup_lines.append(response.text.strip())
            else:
                pickup_lines.append("No response text received from the API. Please try again later.")
    except Exception as e:
        print(f"Error generating pickup lines: {e}")
        pickup_lines = ["Oops! Something went wrong. Please try again."]
    
    return pickup_lines

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5001)





