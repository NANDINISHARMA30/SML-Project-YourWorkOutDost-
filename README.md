# SML-Project-YourWorkOutDost-
This project is a Web Application designed to provide personalized diet and workout recommendations to users based on their dietary preferences, fitness goals, lifestyle factors, dietary restrictions, and health conditions. The application integrates machine learning through Google's Generative AI API to generate tailored recommendations and allows users to upload Jupyter notebooks for additional data handling or analysis. This project involved building a convolutional neural network (CNN) to classify 10 types of gym equipment. The dataset contained 359 training images and 80 validation images, with preprocessing techniques such as resizing, normalization, and data augmentation applied.(Gym Equipment ImageRecognition ). The goal of this project is to classify gym equipment into 10 distinct categories using a custom-built CNN. The dataset is organized into separate folders for each class and stored on Google Drive

 Backend:
- Framework: Flask,pycharm
- API Integration: 
  - Google Generative AI for generating fitness and diet plans.
  - API key securely set via environment variables.

- Functions:
  -  Creates a structured prompt for the AI model and parses its response.
  - Flask routes for handling web pages and file uploads.

 Frontend:
•	HTML & CSS:
                  - A responsive form collects user data and uploads files.
                  - Interactive modals display categorized AI-generated recommendations.
                  - JavaScript: Handles modal interactions and ensures a smooth user experience.


  TensorFlow with Keras 
        - Architecture:
•	 Input Layer: Accepts images of shape (128, 128, 3).
•	Convolutional Layers:
o	Three layers with 32, 64, and 128 filters, kernel size (3x3).
•	Pooling Layers: Max pooling (2x2) to down-sample feature maps.
•	Dense Layers:
o	Flattened layer followed by a 128-unit dense layer with ReLU activation.
o	Output layer with softmax activation for classification into 10 categories.
•  Output Classes: Automatically inferred from folder names.
