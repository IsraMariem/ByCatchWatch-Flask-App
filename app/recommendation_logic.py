from app.models import User, Bycatch, Recommendation, db

def generate_recommendations(user_id):
    user = User.query.get(user_id)
    
    # Placeholder logic for generating recommendations
    # For example, we can recommend species based on the user's background
    if user.background == 'RESEARCHER':
        # Example logic: Recommend species with the highest quantities of bycatch
        bycatch_data = Bycatch.query.order_by(Bycatch.quantity.desc()).limit(5).all()
    elif user.background == 'NGO':
        # Example logic: Recommend species with high mortality rate
        bycatch_data = Bycatch.query.join(Species).filter(Species.mortality_rate > 0.5).limit(5).all()
    else:
        # Default recommendation for others
        bycatch_data = Bycatch.query.limit(5).all()
    
    # Create a recommendation for the user
    for catch in bycatch_data:
        recommendation = Recommendation(user_id=user_id, content=f"Recommended species: {catch.species_id} caught at {catch.port_id}")
        db.session.add(recommendation)
    
    db.session.commit()
