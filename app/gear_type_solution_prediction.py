def get_recommended_gear(species_name, region):
    species_gear_map = {
        "Caretta caretta": ["Circle hooks", "Acoustic pingers"],
        "Sardina pilchardus": ["Modified soak times", "Bycatch reduction devices (BRDs)"],
        "Squatina squatina": ["Bottom trawling", "Modified soak times"],
        "Rhinobatos cemiculus": ["Demersal longlines", "Bycatch reduction devices (BRDs)"],
        "Rhinobatos rhinobatos": ["Demersal longlines", "Bycatch reduction devices (BRDs)"],
        "Chimaera monstrosa": ["Trawling", "Modified soak times"],
    }
    
    if region == "Tunisia":
        gear = species_gear_map.get(species_name, ["Unknown gear"])
    else:
        gear = species_gear_map.get(species_name, ["Unknown gear"])

    return gear
