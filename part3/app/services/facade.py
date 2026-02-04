from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        # تم استبدال InMemoryRepository بالمستودعات المبنية على SQLAlchemy
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
        # تشفير كلمة المرور إذا كانت ضمن البيانات المراد تحديثها
        if "password" in data:
            temp_user = User()
            temp_user.hash_password(data["password"])
            data["password"] = temp_user.password
        return self.user_repo.update(user_id, data)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

   # -------- create place --------\

def create_place(self, data):
        # 1. التأكد من وجود المالك
        owner = self.get_user(data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        # 2. سحب المرافق قبل إنشاء كائن Place
        amenities_ids = data.pop('amenities', [])

        # 3. إنشاء كائن المكان
        place = Place(**data)
        
        # 4. ربط المرافق (هنا قد يحدث الخطأ إذا لم يكن الاسم مطابقاً في الموديل)
        for amenity_id in amenities_ids:
            amenity = self.get_amenity(amenity_id)
            if amenity:
                # تأكد أن اسم الحقل في موديل Place هو amenities
                place.amenities.append(amenity)

        self.place_repo.add(place)
        return place


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
    def create_amenity(self, amenity_data):
        """Create a new amenity from dictionary data"""
        # إذا كانت البيانات قادمة كقاموس من الـ API
        if isinstance(amenity_data, dict):
            amenity = Amenity(**amenity_data)
        else:
            # لدعم الاستدعاء المباشر بالنص إذا لزم الأمر
            amenity = Amenity(name=amenity_data)
            
        self.amenity_repo.add(amenity)
        return amenity
