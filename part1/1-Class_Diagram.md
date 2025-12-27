# 1. Detailed Class Diagram - Business Logic Layer

## Entities
- User
- Place
- Review
- Amenity

```mermaid
classDiagram
direction LR

class User {
  +string id
  +string first_name
  +string last_name
  +string email
  +string password
  +bool is_admin
  +datetime created_at
  +datetime updated_at

  +register()
  +update_profile()
  +delete()
}

class Place {
  +string id
  +string title
  +string description
  +float price
  +float latitude
  +float longitude
  +string owner_id
  +datetime created_at
  +datetime updated_at

  +create()
  +update()
  +delete()
}

class Review {
  +string id
  +int rating
  +string comment
  +string user_id
  +string place_id
  +datetime created_at
  +datetime updated_at

  +create()
  +update()
  +delete()
}

class Amenity {
  +string id
  +string name
  +string description
  +datetime created_at
  +datetime updated_at

  +create()
  +update()
  +delete()
}

%% Relationships
User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : has
Place "0..*" -- "0..*" Amenity : includes
