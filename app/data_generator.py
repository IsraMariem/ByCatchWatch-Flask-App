from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app import create_app, db
from app.models import Port, Species, Bycatch, Report
from faker import Faker
import random

# Initialize Faker instance for generating random data
fake = Faker()

# Sample Data
ports_data = [
    {
        "port_id": "TNBZ24",
        "name": "Bizerte Port",
        "size": "Large",
        "latitude": 37.28,
        "longitude": 9.87,
        "authority_name": "OMMP",
        "phone": "+216 71 735 812",
        "email": "br.bizerte@douane.gov.tn"
    },
    # Add more ports here if needed
]

species_data = [
    {
        "species_id": "SP001",
        "scientific_name": "Caretta caretta",
        "common_name": "Loggerhead Turtle",
        "iucn_status": "Endangered",
        "estimated_catch": 1500,
        "origin": "Migratory",
        "mortality_rate": 0.2
    },
    {
        "species_id": "SP002",
        "scientific_name": "Sardina pilchardus",
        "common_name": "Sardine",
        "iucn_status": "Endangered",
        "estimated_catch": 7000,
        "origin": "Migratory",
        "mortality_rate": 0.25
    },
    # Add more species here if needed
]

bycatch_methods = [
    "Kiss trawling", "Bottom trawling", "Demersal longlines", "Pelagic longlines",
    "Trawling", "Drift Nets", "Cast Nets", "Trap fishing", "Purse seines", "Longlining"
]

def generate_bycatch_data(port_id, species_id):
    return {
        "bycatch_id": uuid.uuid4(),  # Changed to uuid
        "port_id": port_id,
        "species_id": species_id,
        "gear_type": random.choice(bycatch_methods),
        "quantity": random.randint(1, 100),
        "bpue": round(random.uniform(0.1, 1.5), 2),
        "total_catch": random.randint(50, 200),
        "date_caught": fake.date_this_decade()
    }

def generate_report_data(bycatch_id, species_id):
    return {
        "report_id": uuid.uuid4(),  # Changed to uuid
        "species_id": species_id,
        "bycatch_id": bycatch_id,
        "reporter_name": fake.name(),
        "contact_info": fake.phone_number(),
        "remarks": fake.text(),
        "gear_type": random.choice(bycatch_methods),
        "quantity": random.randint(1, 50),
        "date": fake.date_this_year()
    }

def insert_data():
    # Insert Port data
    for port in ports_data:
        port_entry = Port(**port)
        db.session.add(port_entry)
    
    # Insert Species data
    for species in species_data:
        species_entry = Species(**species)
        db.session.add(species_entry)
    
    # Insert Bycatch and Report data
    for _ in range(40):  # Generate 40 rows of Bycatch and Report data
        port_id = random.choice(ports_data)["port_id"]
        species = random.choice(species_data)
        species_id = species["species_id"]
        
        # Generate Bycatch data
        bycatch_data = generate_bycatch_data(port_id, species_id)
        bycatch_entry = Bycatch(**bycatch_data)
        db.session.add(bycatch_entry)
        
        # Generate Report data
        report_data = generate_report_data(bycatch_entry.bycatch_id, species_id)
        report_entry = Report(**report_data)
        db.session.add(report_entry)

    # Commit the data to the database
    db.session.commit()

if __name__ == "__main__":
    app = create_app()  # Ensure you are using the app's factory function
    with app.app_context():  # Set up the application context
        insert_data()
        print("Data insertion complete.")
