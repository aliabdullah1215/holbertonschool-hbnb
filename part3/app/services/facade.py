from app.persistence.repository import InMemoryRepository
from app.services.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        # Repositories
        self.user_repo = UserRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

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
        # Hash password if updating
        if "password" in data:
            temp_user = User()
            temp_user.hash_password(data["password"])
            data["password"] = temp_user.password
        return self.user_repo.update(user_id, data)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    # -------- Place methods --------
    def create_place(self, data):
        owner = self.get_user(data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=data['title'],
            description=data.get('description', ''),
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            owner_id=data['owner_id']
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        return self.place_repo.update(place_id, data)

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    # -------- Review methods --------
    def create_review(self, data):
        review = Review(
            text=data['text'],
            place_id=data['place_id'],
            user_id=data['user_id']
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, data):
        return self.review_repo.update(review_id, data)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)

    # -------- Amenity methods --------
    def create_amenity(self, name):
        amenity = Amenity(name)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        return self.amenity_repo.update(amenity_id, data)

    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)
