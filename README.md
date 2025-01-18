Here’s the complete and updated `README.md` file in a single block for easy copy-pasting:

```markdown
# ByCatch Flask App

## Description
This is a Flask application designed to analyze bycatch data, provide gear recommendations, and visualize the results using various charts and graphs. The app also includes clustering functionality to group species based on shared characteristics and predict optimal fishing gear for specific species and regions.

## Features
- **Bycatch Data Analysis**: Analyze bycatch data to identify trends and patterns.
- **Gear Recommendation**: Recommend fishing gear based on species and region to minimize bycatch.
- **Clustering**: Group species into clusters using K-Means clustering for better insights.
- **Visualization**: Generate scatter plots and Elbow Method plots for clustering results.
- **API Documentation**: Detailed API documentation using Swagger/OpenAPI specifications.
- **Docker Support**: Containerized for easy deployment using Docker.

## Changes Made
- Initial commit with app structure.
- Added functionality for bycatch data processing.
- Integrated chart visualization for bycatch statistics.
- Set up Docker containerization and environment variables.
- Added clustering functionality using K-Means.
- Implemented gear recommendation logic.
- Added API documentation using Flasgger.

## Installation
Follow these steps to set up the project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/IsraMariem/ByCatch-Flask-App.git
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the app**:
   ```bash
   flask run
   ```

6. **Access the API documentation**:
   Open your browser and navigate to `http://127.0.0.1:5000/apidocs` to view the Swagger UI.

## Docker Setup
To run the app using Docker:

1. **Build the Docker image**:
   ```bash
   docker build -t bycatch-flask-app .
   ```

2. **Run the Docker container**:
   ```bash
   docker run -p 5000:5000 bycatch-flask-app
   ```

3. **Access the app**:
   Open your browser and navigate to `http://127.0.0.1:5000`.


## API Endpoints

![API - EndPoints](https://github.com/user-attachments/assets/75d9f51b-8b22-4b9a-a0a1-5c5161e7b4a7)

