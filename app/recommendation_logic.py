from app.models import User, Bycatch, Recommendation, Species, Port, db

def generate_recommendations(user_id):
    user = User.query.get(user_id)

    # Ensure the user exists
    if not user:
        return "User not found."

    recommendations = []
    recommended_species = set()

    def add_recommendation(species, content):
        """Helper function to add a recommendation if not already recommended."""
        if species.species_id not in recommended_species:
            recommendations.append(
                Recommendation(
                    user_id=user_id,
                    content=content
                )
            )
            recommended_species.add(species.species_id)

    # Recommendation logic for different user backgrounds
    if user.background == 'RESEARCHER':
        # Researcher-focused recommendation
        bycatch_data = Bycatch.query.order_by(Bycatch.quantity.desc()).limit(3).all()

        for catch in bycatch_data:
            species = catch.species
            if species.mortality_rate > 0.5:
                add_recommendation(
                    species,
                    f"Highly recommended: {species.common_name} ({species.scientific_name}), high bycatch quantity recorded at port {catch.port_id}. Consider monitoring this species closely."
                )
            else:
                add_recommendation(
                    species,
                    f"Consider researching {species.common_name} ({species.scientific_name}), though it has a lower mortality rate, it is frequently caught."
                )
    
    elif user.background == 'NGO':
        # NGO-focused recommendation
        bycatch_data = (
            Bycatch.query
            .join(Species)
            .filter(Species.mortality_rate > 0.5)
            .order_by(Bycatch.quantity.desc())
            .limit(3)
            .all()
        )

        for catch in bycatch_data:
            species = catch.species
            if species.iucn_status in ['Endangered', 'Vulnerable', 'Near Threatened', 'Least Concern']:
                add_recommendation(
                    species,
                    f"Urgent recommendation: {species.common_name} ({species.scientific_name}) with a high mortality rate and endangered status. Requires conservation efforts at port {catch.port_id}."
                )
            else:
                add_recommendation(
                    species,
                    f"Recommended for further monitoring: {species.common_name} ({species.scientific_name}) due to high bycatch rate."
                )
    
    else:  # Default recommendations for other users
        bycatch_data = Bycatch.query.order_by(Bycatch.quantity.desc()).limit(3).all()

        for catch in bycatch_data:
            species = catch.species
            port = Port.query.filter_by(port_id=catch.port_id).first()
            add_recommendation(
                species,
                f"At port {port.name}, consider observing {species.common_name} ({species.scientific_name}), which has been frequently caught. Gear type used: {catch.gear_type}. Regular monitoring is advised."
            )

    # Fishing method-specific recommendations 
    gear_bycatch = (
        Bycatch.query
        .with_entities(Bycatch.gear_type, db.func.sum(Bycatch.quantity).label('total_quantity'))
        .group_by(Bycatch.gear_type)
        .order_by(db.desc('total_quantity'))
        .limit(3)
        .all()
    )

    for gear_type, total_quantity in gear_bycatch:
        recommendations.append(
            Recommendation(
                user_id=user_id,
                content=f"The fishing method '{gear_type}' has caught a total of {total_quantity} individuals. Consider optimizing or regulating its use to minimize bycatch."
            )
        )

    if recommendations:
        db.session.bulk_save_objects(recommendations)
        db.session.commit()
    else:
        return "No recommendations generated."
