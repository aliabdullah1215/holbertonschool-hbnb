from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        # Repositories
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

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

    # -------- Place methods --------
    def create_place(self, data):
        """
        data must contain:
        title, description, price, latitude, longitude, owner_id
        """
        owner = self.get_user(data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=data['title'],
            owner=owner,
            description=data.get('description', ''),
            price=data.get('price', 0),
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        return self.place_repo.update(place_id, data)

