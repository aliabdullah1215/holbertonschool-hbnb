from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        # Repositories
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # -------- User methods --------
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        return self.user_repo.update(user_id, data)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # -------- Amenity methods --------
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
        self.amenity_repo.update(amenity_id, amenity)
        return amenity

    # -------- Place methods --------
    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("owner not found")

        place = Place(
            title=place_data.get('title'),
            owner=owner,
            description=place_data.get('description', ''),
            price=place_data.get('price', 0.0),
            latitude=place_data.get('latitude', None),
            longitude=place_data.get('longitude', None)
        )

        amenity_ids = place_data.get('amenities', [])
        if amenity_ids:
            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError("amenity not found")
                place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None

        if 'title' in place_data:
            place.title = place_data['title']
        if 'description' in place_data:
            place.description = place_data['description']
        if 'price' in place_data:
            place.price = place_data['price']
        if 'latitude' in place_data:
            place.latitude = place_data['latitude']
        if 'longitude' in place_data:
            place.longitude = place_data['longitude']

        if 'owner_id' in place_data:
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError("owner not found")
            place.owner = owner

        if 'amenities' in place_data:
            new_ids = place_data['amenities'] or []
            new_amenities = []
            for amenity_id in new_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError("amenity not found")
                new_amenities.append(amenity)
            place.amenities = new_amenities

        self.place_repo.update(place_id, place)
        return place

    # -------- Review methods --------
    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        user = self.get_user(user_id)
        place = self.get_place(place_id)

        if not user:
            raise ValueError("user not found")
        if not place:
            raise ValueError("place not found")

        review = Review(
            place=place,
            user=user,
            text=review_data.get('text'),
            rating=review_data.get('rating')
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        reviews = self.get_all_reviews()
        return [r for r in reviews if r.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']
        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
