# 2. Sequence Diagrams for API Calls

This document shows the interaction flow for four main API operations in HBnB Evolution.

---

## 1. User Registration

When a user signs up, the system validates their information and creates a new account.

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Facade
    participant UserModel
    participant Database

    Client->>API: POST /users/register
    API->>Facade: register_user(data)
    Facade->>UserModel: validate(data)
    UserModel->>Database: check_email_exists()
    Database-->>UserModel: result
    
    alt email exists
        UserModel-->>API: error
        API-->>Client: 409 Conflict
    else email available
        UserModel->>Database: save_user()
        Database-->>UserModel: success
        UserModel-->>API: user created
        API-->>Client: 201 Created
    end
```

---

## 2. Place Creation

Authenticated users can create place listings with amenities.

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Facade
    participant PlaceModel
    participant Database

    Client->>API: POST /places
    API->>API: verify_token()
    API->>Facade: create_place(data, user_id)
    Facade->>PlaceModel: validate(data)
    PlaceModel->>Database: save_place()
    Database-->>PlaceModel: place_id
    
    loop amenities
        PlaceModel->>Database: link_amenity()
    end
    
    PlaceModel-->>API: place created
    API-->>Client: 201 Created
```

---

## 3. Review Submission

Users can submit reviews for places they've visited.

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Facade
    participant ReviewModel
    participant Database

    Client->>API: POST /places/{id}/reviews
    API->>API: verify_token()
    API->>Facade: create_review(place_id, user_id, data)
    Facade->>Database: get_place(place_id)
    Database-->>Facade: place
    
    alt user is owner
        Facade-->>API: error
        API-->>Client: 403 Forbidden
    else valid
        Facade->>ReviewModel: create(data)
        ReviewModel->>Database: save_review()
        Database-->>ReviewModel: success
        ReviewModel-->>API: review created
        API-->>Client: 201 Created
    end
```

---

## 4. Fetching Places

Retrieve a list of places with optional filters.

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Facade
    participant PlaceModel
    participant Database

    Client->>API: GET /places?filters
    API->>Facade: get_places(filters)
    Facade->>PlaceModel: build_query(filters)
    PlaceModel->>Database: fetch_places()
    Database-->>PlaceModel: places[]
    
    loop each place
        PlaceModel->>Database: get_amenities()
        Database-->>PlaceModel: amenities[]
    end
    
    PlaceModel-->>API: places with details
    API-->>Client: 200 OK
```

---

## Notes

- All diagrams follow the 3-layer architecture pattern
- Authentication is handled at the API layer
- Business logic validation occurs in the Facade/Model layer
- Database operations are isolated in the Persistence layer
