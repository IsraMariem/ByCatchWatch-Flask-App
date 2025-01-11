import os
import base64
from io import BytesIO
from flask import Blueprint, request, jsonify, current_app
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

clustering_bp = Blueprint('clustering', __name__)

def preprocess_species_data(species_data):
    df = pd.DataFrame(species_data)
    print("Columns in species data:", df.columns)  
    
    df_numeric = df.drop(columns=['Species_Name'])

    df_encoded = pd.get_dummies(df_numeric, columns=["Habitat_Type", "Conservation_Status"], drop_first=True)

    return df_encoded


def cluster_species_kmeans(data, num_clusters=3):
    data = preprocess_species_data(data)

    if data.empty or data.shape[1] < 2:
        return None, None

    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    data['Cluster'] = kmeans.fit_predict(data)

    charts_folder = os.path.abspath('Charts')
    if not os.path.exists(charts_folder):
        os.makedirs(charts_folder)  

    if data.shape[1] >= 2: 
        plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=data['Cluster'], cmap='viridis')
        plt.xlabel(data.columns[0])
        plt.ylabel(data.columns[1])
        plt.title('K-Means Clustering of Species')

       
        plot_file_path = os.path.join(charts_folder, 'clustering_plot.png')
        plt.savefig(plot_file_path)

        # Save the plot to a BytesIO object for base64 encoding
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()  

        return img_base64, plot_file_path
    else:
        return None, None


def preprocess_species_data2(species_data):
    df = pd.DataFrame(species_data)
    print("Columns in species data:", df.columns)  
    
    
    df_numeric = df.drop(columns=['Species_Name'])

    
    df_encoded = pd.get_dummies(df_numeric, columns=["Habitat_Type", "Conservation_Status","Fishing_Gear_Type"], drop_first=True)

    return df_encoded



@clustering_bp.route('/kmeans', methods=['POST'])
def kmeans():
    try:
        data = request.get_json()

        
        if 'species_data' not in data:
            return jsonify({'error': 'Missing species_data field in the request.'}), 400

        species_data = pd.DataFrame(data['species_data'])
        num_clusters = data.get('num_clusters', 3)

        
        img_base64, plot_file_path = cluster_species_kmeans(species_data, num_clusters)
        
        if not img_base64:
            return jsonify({'error': 'Data not suitable for clustering or no data available.'}), 400
        
       
        response = {
            'clustered_data': species_data.to_dict(orient="records"),
            'chart': img_base64,  
            'chart_url': f"/charts/{os.path.basename(plot_file_path)}"
        }
        
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@clustering_bp.route('/cluster_analysis', methods=['POST'])
def cluster_analysis():
    try:
        data = request.get_json()

        if 'species_data' not in data:
            return jsonify({'error': 'Missing species_data field in the request.'}), 400

        species_data = pd.DataFrame(data['species_data'])
        num_clusters = data.get('num_clusters', 3)

        processed_data = preprocess_species_data2(species_data)
        kmeans = KMeans(n_clusters=num_clusters, random_state=0)
        processed_data['Cluster'] = kmeans.fit_predict(processed_data)

        # cluster centers and number of items in each cluster
        cluster_centers = kmeans.cluster_centers_.tolist()
        cluster_counts = processed_data['Cluster'].value_counts().to_dict()

       
        charts_folder = os.path.abspath('Charts')
        if not os.path.exists(charts_folder):
            os.makedirs(charts_folder)  

        # Create a scatter plot
        plt.scatter(processed_data.iloc[:, 0], processed_data.iloc[:, 1], c=processed_data['Cluster'], cmap='viridis')
        plt.xlabel(processed_data.columns[0])
        plt.ylabel(processed_data.columns[1])
        plt.title('K-Means Clustering of Species')

        plot_file_path = os.path.join(charts_folder, 'cluster_analysis_plot.png')
        plt.savefig(plot_file_path)
        plt.close()  
        
        response = {
            'cluster_centers': cluster_centers,
            'cluster_counts': cluster_counts
        }
        
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@clustering_bp.route('/optimal_clusters', methods=['POST'])
def optimal_clusters():
    try:
        data = request.get_json()

        if 'species_data' not in data:
            return jsonify({'error': 'Missing species_data field in the request.'}), 400

        species_data = pd.DataFrame(data['species_data'])
        processed_data = preprocess_species_data2(species_data)

        # Calculate WCSS (Within-Cluster Sum of Squares) for different cluster counts
        wcss = []
        for i in range(1, 11):
            kmeans = KMeans(n_clusters=i, random_state=0)
            kmeans.fit(processed_data)
            wcss.append(kmeans.inertia_)

        # Generate an elbow plot
        plt.figure()
        plt.plot(range(1, 11), wcss, marker='o')
        plt.title('Elbow Method for Optimal Clusters')
        plt.xlabel('Number of Clusters')
        plt.ylabel('WCSS')

        # Save the plot as a PNG file in the Charts folder
        charts_folder = 'Charts'
        if not os.path.exists(charts_folder):
            os.makedirs(charts_folder)  # Create the Charts folder if it doesn't exist

        plot_filename = os.path.join(charts_folder, 'elbow_plot.png')
        plt.savefig(plot_filename, format='png')
        plt.close()

        # Return the file path in the response
        return jsonify({'message': f'Plot saved as {plot_filename}'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
