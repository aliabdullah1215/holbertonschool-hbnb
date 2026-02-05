from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # -------- User methods --------
    def create_user(self, user_data):
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            is_admin=user_data.get('is_admin', False)
        )
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        if "password" in data:
            user_to_hash = User()
            user_to_hash.hash_password(data["password"])
            data["password"] = user_to_hash.password
        return self.user_repo.update(user_id, data)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    # -------- Place methods --------
    def create_place(self, data):
        amenities_ids = data.pop('amenities', [])
        place = Place(**data)
        
        for amenity_id in amenities_ids:
            amenity = self.get_amenity(amenity_id)
            if amenity:
                place.amenities.append(amenity)
        
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        if 'amenities' in data:
            amenity_ids = data.pop('amenities')
            place.amenities = []
            for a_id in amenity_ids:
                amenity = self.get_amenity(a_id)
                if amenity:
                    place.amenities.append(amenity)

        for key, value in data.items():
            if hasattr(place, key):
                setattr(place, key, value)

        return self.place_repo.update(place.id, place)

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    # -------- Amenity methods --------
    def create_amenity(self, amenity_data):
        if isinstance(amenity_data, dict):
            amenity = Amenity(**amenity_data)
        else:
            amenity = Amenity(name=amenity_data)
            
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        return self.amenity_repo.update(amenity_id, data)

    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)

    # --- New Method for Linking Place and Amenity ---
    def add_amenity_to_place(self, place_id, amenity_id):
        """Links an amenity to a specific place"""
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)
        
        if not place or not amenity:
            return None
            
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            # We pass the updated object back to the repository to commit changes
            return self.place_repo.update(place.id, place)
        return place

    # -------- Review methods --------
    def create_review(self, data):
        place = self.get_place(data['place_id'])
        if not place:
            raise ValueError("Place not found")
        
        if str(place.owner_id) == str(data['user_id']):
            raise ValueError("You cannot review your own place")

        existing_reviews = self.get_all_reviews()
        for r in existing_reviews:
            if str(r.place_id) == str(data['place_id']) and str(r.user_id) == str(data['user_id']):
                raise ValueError("You have already reviewed this place")

        review = Review(
            text=data['text'],
            rating=data.get('rating'),
            place_id=data['place_id'],
            user_id=data['user_id']
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Fetches all reviews for a specific place"""
        all_reviews = self.get_all_reviews()
        return [r for r in all_reviews if str(r.place_id) == str(place_id)]

    def update_review(self, review_id, data):
        return self.review_repo.update(review_id, data)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
