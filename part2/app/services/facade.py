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
        return self.amenity_repo.update(amenity_id, amenity_data)

    # -------- Place methods --------
def create_place(self, place_data):
    # Validate owner
    owner_id = place_data.get('owner_id')
    owner = self.get_user(owner_id)
    if not owner:
        raise ValueError("owner not found")

    # Create place (Place expects owner object)
    place = Place(
        title=place_data.get('title'),
        owner=owner,
        description=place_data.get('description', ''),
        price=place_data.get('price', 0.0),
        latitude=place_data.get('latitude', None),
        longitude=place_data.get('longitude', None)
    )

    # Attach amenities if provided
    amenity_ids = place_data.get('amenities', [])
    if amenity_ids is None:
        amenity_ids = []

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

    # Update basic fields with validation via Place rules
    if 'title' in place_data:
        title = place_data['title']
        if not title or not isinstance(title, str) or len(title) > 100:
            raise ValueError("Invalid title")
        place.title = title

    if 'description' in place_data:
        place.description = place_data['description']

    if 'price' in place_data:
        price = place_data['price']
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("price must be a number >= 0")
        place.price = float(price)

    if 'latitude' in place_data:
        lat = place_data['latitude']
        if lat is not None and (not isinstance(lat, (int, float)) or not (-90 <= lat <= 90)):
            raise ValueError("latitude must be between -90 and 90")
        place.latitude = lat

    if 'longitude' in place_data:
        lon = place_data['longitude']
        if lon is not None and (not isinstance(lon, (int, float)) or not (-180 <= lon <= 180)):
            raise ValueError("longitude must be between -180 and 180")
        place.longitude = lon

    # Update owner if provided
    if 'owner_id' in place_data:
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("owner not found")
        place.owner = owner

    # Update amenities list if provided (replace)
    if 'amenities' in place_data:
        new_ids = place_data['amenities'] or []
        new_amenities = []
        for amenity_id in new_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError("amenity not found")
            new_amenities.append(amenity)
        place.amenities = new_amenities

    place.save()
    return place


# -------- Review methods --------
def create_review(self, review_data):
    user_id = review_data.get('user_id')
    place_id = review_data.get('place_id')
    text = review_data.get('text')
    rating = review_data.get('rating')

    user = self.get_user(user_id)
    if not user:
        raise ValueError("user not found")

    place = self.get_place(place_id)
    if not place:
        raise ValueError("place not found")

    review = Review(place=place, user=user, text=text, rating=rating)

    # attach to place collection
    place.reviews.append(review)
    place.save()

    self.review_repo.add(review)
    return review


def get_review(self, review_id):
    return self.review_repo.get(review_id)


def get_all_reviews(self):
    return self.review_repo.get_all()


def get_reviews_by_place(self, place_id):
    place = self.get_place(place_id)
    if not place:
        return None
    return getattr(place, 'reviews', [])


def update_review(self, review_id, review_data):
    review = self.get_review(review_id)
    if not review:
        return None

    if 'text' in review_data:
        text = review_data['text']
        if not text or not isinstance(text, str):
            raise ValueError("text must be a non-empty string")
        review.text = text

    if 'rating' in review_data:
        rating = review_data['rating']
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("rating must be an integer between 1 and 5")
        review.rating = rating

    review.save()
    return review


def delete_review(self, review_id):
    review = self.get_review(review_id)
    if not review:
        return False

    # remove from its place.reviews
    place = getattr(review, 'place', None)
    if place and hasattr(place, 'reviews'):
        place.reviews = [r for r in place.reviews if r.id != review_id]
        place.save()

    self.review_repo.delete(review_id)
    return True

