from flask import Blueprint, jsonify
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from app.models import Port, Bycatch,Species
from app import db
import matplotlib
matplotlib.use('Agg')
import numpy as np
import os
from flasgger import swag_from


charts_folder = "./Charts"

visualization_bp = Blueprint('visualizations', __name__,url_prefix='/visualizations')


# Total Bycatch Quantity by Location
def generate_total_catch_by_location():
    result = db.session.query(Port.location, db.func.sum(Bycatch.quantity).label('total_catch'))\
                       .join(Bycatch, Bycatch.port_id == Port.port_id)\
                       .group_by(Port.location)\
                       .order_by(db.func.sum(Bycatch.quantity).desc()).all()  # Sort by total catch descending

    if not result:
        print("No data available for total catch by location.")
        return None

    locations = [r[0] for r in result]
    total_catch = [r[1] for r in result]
    print("Query Result:", result)  

    plt.figure(figsize=(12, 8))
    plt.bar(locations, total_catch, color='skyblue', width=0.7)
    plt.xlabel('Location')
    plt.ylabel('Total Catch')
    plt.title('Total Catch by Location')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')  
    plt.tight_layout()  

    # Save the plot to a BytesIO object to return as an image
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.savefig(os.path.join(charts_folder, 'Bycatch-by-Location.png'))

    img.seek(0)

    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return img_base64


@visualization_bp.route('/total-catch-by-location', methods=['GET'])
@swag_from({
    'tags': ['Visualizations'],
    'description': 'Returns a bar chart showing the total bycatch quantity by location.',
    'responses': {
        '200': {
            'description': 'Bar chart showing total bycatch by location',
            'content': {
                'application/json': {
                    'example': {
                        'chart': 'Base64 encoded image data'
                    }
                }
            }
        },
        '404': {
            'description': 'No data available for total catch by location.'
        }
    }
})
def total_catch_by_location():
    chart_base64 = generate_total_catch_by_location()
    if chart_base64 is None:
        return jsonify({'error': 'No data available for total catch by location.'}), 404
    return jsonify({'chart': chart_base64})

from datetime import datetime

# Bycatch Quantity Over Time

def generate_bycatch_trends():
    result = db.session.query(Bycatch.date_caught, db.func.sum(Bycatch.quantity).label('total_bycatch'))\
                       .group_by(Bycatch.date_caught).order_by(Bycatch.date_caught).all()
    
    if not result:
        return None  

    dates = [datetime.strptime(r[0], '%Y-%m-%d') if isinstance(r[0], str) else r[0] for r in result]
    bycatch = [r[1] for r in result]

   
    plt.figure(figsize=(12, 8))
    plt.plot(dates, bycatch, marker='o', color='orange', linewidth=2)
    plt.xlabel('Date')
    plt.ylabel('Bycatch Quantity')
    plt.title('Bycatch Trends Over Time')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()  

    img = BytesIO()
    plt.savefig(img, format='png')
    plt.savefig(os.path.join(charts_folder,'Bycatch-Over-Time.png'))
    img.seek(0)

    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return img_base64

@visualization_bp.route('/bycatchtime-trends', methods=['GET'])
@swag_from({
    'tags': ['Visualizations'],
    'description': 'Returns a line chart showing bycatch quantity trends over time.',
    'responses': {
        '200': {
            'description': 'Line chart showing bycatch trends over time.',
            'content': {
                'application/json': {
                    'example': {
                        'chart': 'Base64 encoded image data'
                    }
                }
            }
        },
        '404': {
            'description': 'No data available for bycatch trends.'
        }
    }
})
def get_bycatch_time_trends():
    chart_base64 = generate_bycatch_trends()
    if chart_base64 is None:
        return jsonify({'error': 'No data available for bycatch trends.'}), 404
    return jsonify({'chart': chart_base64})


# Species Mortality Rate Analysis
import numpy as np

def generate_species_mortality_analysis():
    try:
        # Query species and mortality rate
        result = db.session.query(Species.scientific_name, Species.mortality_rate).all()

        if not result:
            raise ValueError("No data available for species mortality rates.")

        species = [r[0] for r in result]
        mortality_rate = [r[1] if r[1] is not None else 0 for r in result]

        # Sort data by mortality rate
        sorted_data = sorted(zip(species, mortality_rate), key=lambda x: x[1], reverse=True)
        species, mortality_rate = zip(*sorted_data)

        # Normalize mortality rates for color mapping
        normed_mortality_rate = np.array(mortality_rate) / max(mortality_rate)

        # Create a bar chart
        plt.figure(figsize=(12, 7))
        bars = plt.bar(species, mortality_rate, color=plt.cm.viridis(normed_mortality_rate))
        plt.xlabel('Species')
        plt.ylabel('Mortality Rate (%)')
        plt.title('Species Mortality Rate Analysis')
        plt.xticks(rotation=90)

        # Annotate bars with mortality rates
        for bar, rate in zip(bars, mortality_rate):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                     f'{rate:.1f}%', ha='center', va='bottom', fontsize=8)

        # Save the plot to a BytesIO object to return as an image
        img = BytesIO()
        plt.savefig(img, format='png')
        plt.savefig(os.path.join(charts_folder,'Species-Mortality-Analysis.png'))
        img.seek(0)

        # Convert the plot to a base64 string
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()

        return img_base64
    except Exception as e:
        print(f"Error generating species mortality analysis: {e}")
        return None


@visualization_bp.route('/speciesmortality-analysis', methods=['GET'])
@swag_from({
    'tags': ['Visualizations'],
    'description': 'Get a bar chart visualization of species mortality rates.',
    'responses': {
        '200': {
            'description': 'A base64-encoded image of the species mortality rate analysis chart.',
            'content': {
                'application/json': {
                    'example': {
                        'chart': 'base64_encoded_string_here'
                    }
                }
            }
        },
        '500': {
            'description': 'Failed to generate the species mortality analysis chart.',
            'content': {
                'application/json': {
                    'example': {
                        'error': 'Failed to generate species mortality analysis'
                    }
                }
            }
        }
    }
})
def get_species_mortality_analysis():
    chart_base64 = generate_species_mortality_analysis()
    if chart_base64:
        return jsonify({'chart': chart_base64})
    else:
        return jsonify({'error': 'Failed to generate species mortality analysis'}), 500


# Gear Type Efficiency Analysis
def generate_gear_efficiency():
    try:
        
        result = db.session.query(Bycatch.gear_type, db.func.avg(Bycatch.bpue).label('avg_bpue'))\
                           .group_by(Bycatch.gear_type).all()

        if not result:
            raise ValueError("No data available for gear type efficiency analysis.")

       
        gear_types = [r[0] for r in result]
        avg_bpue = [float(r[1]) if r[1] is not None else 0 for r in result]

        sorted_data = sorted(zip(gear_types, avg_bpue), key=lambda x: x[1], reverse=True)
        gear_types, avg_bpue = zip(*sorted_data)

        plt.figure(figsize=(12, 7))
        bars = plt.bar(gear_types, avg_bpue, color=plt.cm.plasma(np.array(avg_bpue) / max(avg_bpue)))
        plt.xlabel('Gear Type', fontsize=12)
        plt.ylabel('Average BPUE', fontsize=12)
        plt.title('Gear Type Efficiency (Average BPUE)', fontsize=14)
        plt.xticks(rotation=45, fontsize=10)

        
        for bar, bpue in zip(bars, avg_bpue):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                     f'{bpue:.2f}', ha='center', va='bottom', fontsize=10)

        img = BytesIO()
        plt.savefig(img, format='png')
        plt.savefig(os.path.join(charts_folder,'Gear_Type_Efficiency.png'))
        img.seek(0)

        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()

        return img_base64
    except Exception as e:
        print(f"Error generating gear efficiency analysis: {e}")
        return None

@visualization_bp.route('/gearefficiency', methods=['GET'])
@swag_from({
    'tags': ['Visualizations'],
    'description': 'Get a bar chart visualization of gear type efficiency (Average BPUE).',
    'responses': {
        '200': {
            'description': 'A base64-encoded image of the gear type efficiency analysis chart.',
            'content': {
                'application/json': {
                    'example': {
                        'chart': 'base64_encoded_string_here'
                    }
                }
            }
        },
        '500': {
            'description': 'Failed to generate the gear efficiency analysis chart.',
            'content': {
                'application/json': {
                    'example': {
                        'error': 'Failed to generate gear efficiency analysis'
                    }
                }
            }
        }
    }
})
def get_gear_efficiency():
    chart_base64 = generate_gear_efficiency()
    if chart_base64:
        return jsonify({'chart': chart_base64})
    else:
        return jsonify({'error': 'Failed to generate gear efficiency analysis'}), 500


def generate_catch_distribution():
    result = db.session.query(Species.common_name, Port.name, db.func.sum(Bycatch.quantity).label('total_catch'))\
                       .join(Bycatch, Bycatch.species_id == Species.species_id)\
                       .join(Port, Port.port_id == Bycatch.port_id)\
                       .group_by(Species.common_name, Port.name).all()
    
    species = [r[0] for r in result]
    ports = list(set(r[1] for r in result))  # Get unique ports
    total_catch = {s: {p: 0 for p in ports} for s in species}

    # Fill total_catch data (species -> port -> total_catch)
    for s, p, t in result:
        total_catch[s][p] = t

    species_list = list(species)
    ports_list = list(ports)
    catch_data = []

    for s in species_list:
        catch_data.append([total_catch[s][p] for p in ports_list])

  
    x = np.arange(len(species_list)) 
    width = 0.5  # Width of each bar

    fig, ax = plt.subplots(figsize=(14, 9))

    
    bottom = np.zeros(len(species_list))  # Start from 0 for each bar

    for i, port in enumerate(ports_list):
        ax.bar(x, [catch_data[j][i] for j in range(len(species_list))], width, bottom=bottom, label=port)
        bottom += np.array([catch_data[j][i] for j in range(len(species_list))])  # Update bottom for stacking

    # Labels and titles
    ax.set_xlabel('Species')
    ax.set_ylabel('Total Catch')
    ax.set_title('Catch Distribution by Species and Port')
    ax.set_xticks(x)
    ax.set_xticklabels(species_list, rotation=90)
    ax.legend(title='Port')

    # Save the plot to a BytesIO object to return as an image
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.savefig(os.path.join(charts_folder,'Catch-Distribution.png'))

    img.seek(0)

    # Convert the plot to a base64 string
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return img_base64

@visualization_bp.route('/catch-distribution', methods=['GET'])
@swag_from({
    'tags': ['Visualizations'],
    'description': 'Get a stacked bar chart visualization of catch distribution by species and port.',
    'responses': {
        '200': {
            'description': 'A base64-encoded image of the catch distribution chart.',
            'content': {
                'application/json': {
                    'example': {
                        'chart': 'base64_encoded_string_here'
                    }
                }
            }
        },
        '500': {
            'description': 'Failed to generate the catch distribution chart.',
            'content': {
                'application/json': {
                    'example': {
                        'error': 'Failed to generate catch distribution analysis'
                    }
                }
            }
        }
    }
})
def get_catch_distribution():
    chart_base64 = generate_catch_distribution()
    return jsonify({'chart': chart_base64})



def generate_iucn_status_analysis():
    # Query species IUCN status and estimated catch
    result = db.session.query(Species.iucn_status, Species.estimated_catch).all()
    
    statuses = [r[0] for r in result]
    estimated_catch = [r[1] for r in result]

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(statuses, estimated_catch, color='red')
    plt.xlabel('IUCN Status')
    plt.ylabel('Estimated Catch')
    plt.title('Species IUCN Status vs Estimated Catch')
    plt.xticks(rotation=45)

    # Save the plot to a BytesIO object to return as an image
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.savefig(os.path.join(charts_folder,'Species IUCN Status vs Estimated Catch.png'))

    img.seek(0)

    # Convert the plot to a base64 string
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return img_base64

@visualization_bp.route('/spstatus-analysis', methods=['GET'])
@swag_from({
    'tags': ['Visualizations'],
    'description': 'Get a stacked bar chart visualization of catch distribution by species and port.',
    'responses': {
        '200': {
            'description': 'A base64-encoded image of the catch distribution chart.',
            'content': {
                'application/json': {
                    'example': {
                        'chart': 'base64_encoded_string_here'
                    }
                }
            }
        },
        '500': {
            'description': 'Failed to generate the catch distribution chart.',
            'content': {
                'application/json': {
                    'example': {
                        'error': 'Failed to generate catch distribution analysis'
                    }
                }
            }
        }
    }
})
def get_iucn_status_analysis():
    chart_base64 = generate_iucn_status_analysis()
    return jsonify({'chart': chart_base64})




# Combine all charts into one dashboard image
def generate_dashboard():
    # 1. Total Catch by Location
    total_catch_chart = generate_total_catch_by_location()
    # 2. Bycatch Trends Over Time
    bycatch_trends_chart = generate_bycatch_trends()
    # 3. Species Mortality Analysis
    species_mortality_chart = generate_species_mortality_analysis()
    # 4. Gear Type Efficiency
    gear_efficiency_chart = generate_gear_efficiency()
    # 5. Catch Distribution
    catch_distribution_chart = generate_catch_distribution()
    # 6. IUCN Status Analysis
    iucn_status_chart = generate_iucn_status_analysis()

    # Combine charts into one image
    fig, axs = plt.subplots(3, 2, figsize=(14, 12))  # 3 rows, 2 columns grid
    
    # List of charts
    charts = [
        total_catch_chart,
        bycatch_trends_chart,
        species_mortality_chart,
        gear_efficiency_chart,
        catch_distribution_chart,
        iucn_status_chart
    ]

    # Plot each chart in the grid
    for i, ax in enumerate(axs.flat):
        if charts[i]:
            # Plot the chart (decode base64 to image and display)
            img_data = base64.b64decode(charts[i])
            img = BytesIO(img_data)
            ax.imshow(plt.imread(img), aspect='auto')
            ax.axis('off')  # Hide axes
        else:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=14)

    plt.tight_layout()
    
    # Save the combined image to a PNG file
    img_path = 'dashboard.png'
    plt.savefig(os.path.join(charts_folder,img_path))

    # Save the plot to a BytesIO object to return as an image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Convert the plot to a base64 string
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return img_base64, img_path

# Dashboard Endpoint
@visualization_bp.route('/dashboard', methods=['GET'])
@swag_from({
    'tags': ['Visualizations'],
    'description': 'Generate a dashboard combining multiple visualizations (Total Catch, Bycatch Trends, Species Mortality, Gear Efficiency, Catch Distribution, IUCN Status Analysis) into one image.',
    'responses': {
        '200': {
            'description': 'A base64-encoded image of the dashboard containing multiple charts.',
            'content': {
                'application/json': {
                    'example': {
                        'chart': 'base64_encoded_dashboard_image_here',
                        'image_path': 'dashboard.png'
                    }
                }
            }
        },
        '500': {
            'description': 'Failed to generate the dashboard.',
            'content': {
                'application/json': {
                    'example': {
                        'error': 'Failed to generate dashboard'
                    }
                }
            }
        }
    }
})
def dashboard():
    chart_base64, img_path = generate_dashboard()

    if chart_base64:
        return jsonify({
            'chart': chart_base64,
            'image_path': img_path
        })
    else:
        return jsonify({'error': 'Failed to generate dashboard'}), 500