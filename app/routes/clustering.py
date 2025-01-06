from flask import Blueprint, request, jsonify, current_app
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')

# Initialize the blueprint for clustering
clustering_bp = Blueprint('clustering', __name__)

def preprocess_species_data(species_data):
    df = pd.DataFrame(species_data)
    print("Columns in species data:", df.columns)  # Debugging line
    # Drop non-numeric columns like Species_Name, which are not needed for clustering
    df_numeric = df.drop(columns=['Species_Name'])

    # One-hot encode categorical columns like Habitat_Type and Conservation_Status
    df_encoded = pd.get_dummies(df_numeric, columns=["Habitat_Type", "Conservation_Status"], drop_first=True)

    return df_encoded


def cluster_species_kmeans(data, num_clusters=3):
    data = preprocess_species_data(data)

    # Ensure there is enough data to apply clustering
    if data.empty or data.shape[1] < 2:
        return None, None

    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    data['Cluster'] = kmeans.fit_predict(data)

    charts_folder = os.path.abspath('Charts')  # Adjust this to match the actual path to your Charts folder


    # Ensure plot is generated and saved
    if data.shape[1] >= 2:  # Ensure we have 2D or more data for plotting
        plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=data['Cluster'], cmap='viridis')
        plt.xlabel(data.columns[0])
        plt.ylabel(data.columns[1])
        plt.title('K-Means Clustering of Species')

        # Save the plot to a file
        plot_file_path = os.path.join(charts_folder, 'clustering_plot.png')
        plt.savefig(plot_file_path)

        # Save the plot to a BytesIO object for base64 encoding
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()  # Close the plot to avoid memory issues

        return img_base64, plot_file_path
    else:
        return None, None

@clustering_bp.route('/kmeans', methods=['POST'])
def kmeans():
    try:
        data = request.get_json()

        # Ensure the 'species_data' field is present
        if 'species_data' not in data:
            return jsonify({'error': 'Missing species_data field in the request.'}), 400

        species_data = pd.DataFrame(data['species_data'])
        num_clusters = data.get('num_clusters', 3)

        # Perform clustering and get the clustered data
        img_base64, plot_file_path = cluster_species_kmeans(species_data, num_clusters)
        
        if not img_base64:
            return jsonify({'error': 'Data not suitable for clustering or no data available.'}), 400
        
        # Return the clustered data and the plot as a base64 string
        response = {
            'clustered_data': species_data.to_dict(orient="records"),
            'chart': img_base64,  # Chart as a base64 string
            'chart_url': f"/charts/{os.path.basename(plot_file_path)}"  # URL to access the saved chart
        }
        
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
