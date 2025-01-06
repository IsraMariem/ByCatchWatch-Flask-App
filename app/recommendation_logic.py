from app.models import User, Bycatch, Recommendation, db

def generate_recommendations(user_id):
    user = User.query.get(user_id)
    
    # Initialize an empty list to store recommendations
    recommendations = []
    
    

    # Placeholder logic for generating recommendations based on the user's background
    if user.background == 'RESEARCHER':
        # Recommend species with the highest quantities of bycatch, prioritized by their vulnerability or rarity
        bycatch_data = Bycatch.query.order_by(Bycatch.quantity.desc()).limit(5).all()
        
        # Refine the logic to recommend species with high mortality rates or rare species
        for catch in bycatch_data:
            species = catch.species
            if species.mortality_rate > 0.5:  # Prioritize species with high mortality rates
                recommendations.append(
                    Recommendation(
                        user_id=user_id,
                        content=f"Highly recommended: {species.common_name} ({species.scientific_name}), high bycatch quantity recorded at port {catch.port_id}. Consider monitoring this species closely."
                    )
                )
            else:
                recommendations.append(
                    Recommendation(
                        user_id=user_id,
                        content=f"Consider researching {species.common_name} ({species.scientific_name}), though it has a lower mortality rate, it is frequently caught."
                    )
                )
                
    elif user.background == 'NGO':
        # Recommend species with high mortality rates or those endangered (IUCN Red List)
        bycatch_data = Bycatch.query.join(Species).filter(Species.mortality_rate > 0.5).limit(5).all()
        
        for catch in bycatch_data:
            species = catch.species
            if species.iucn_status in ['Endangered', 'Vulnerable', 'Near Threatened','Least Concern']:  # Critically Endangered, Endangered, Vulnerable
                recommendations.append(
                    Recommendation(
                        user_id=user_id,
                        content=f"Urgent recommendation: {species.common_name} ({species.scientific_name}) with a high mortality rate and endangered status. Requires conservation efforts at port {catch.port_id}."
                    )
                )
            else:
                recommendations.append(
                    Recommendation(
                        user_id=user_id,
                        content=f"Recommended for further monitoring: {species.common_name} ({species.scientific_name}) due to high bycatch rate."
                    )
                )
                
    else:
        # Default recommendation logic for other users
        # For example, recommend species with notable historical catches
        bycatch_data = Bycatch.query.order_by(Bycatch.quantity.desc()).limit(2).all()
        
        for catch in bycatch_data:
            species = catch.species
            recommendations.append(
                Recommendation(
                    user_id=user_id,
                    content=f"Consider observing {species.common_name} ({species.scientific_name}), which has been frequently caught at {catch.port_id}. Regular monitoring is advised."
                )
            )

    # Add all recommendations to the session in one go to minimize database queries
    db.session.bulk_save_objects(recommendations)
    db.session.commit()
