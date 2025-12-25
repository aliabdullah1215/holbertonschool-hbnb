# HBnB Evolution - Technical Documentation (Part 1)

## Introduction
This document provides the technical blueprint for the HBnB Evolution application.  
It covers the overall layered architecture, the core domain model (Business Logic layer), and key API interaction flows using UML diagrams.

### Scope
The documentation includes:
- High-level package diagram (3-layer architecture + Facade communication)
- Detailed class diagram for the Business Logic layer
- Sequence diagrams for core API calls

---

## High-Level Architecture (Task 0)

### Purpose
Provide a conceptual overview of the HBnB system structure and how layers communicate using the Facade pattern.

### Diagram
```mermaid
%% classDiagram
class PresentationLayer {
    <<Layer>>
    +API Endpoints
    +Services
}

class BusinessLogicLayer {
    <<Layer>>
    +Domain Models
    +Business Rules
}

class PersistenceLayer {
    <<Layer>>
    +Database Repositories
}

PresentationLayer --> BusinessLogicLayer : Facade Access
BusinessLogicLayer --> PersistenceLayer : CRUD Operations

---

## Business Logic Layer - Class Diagram (Task 1)

### Purpose
Describe the main domain entities (User, Place, Review, Amenity), their attributes, methods, and relationships.

### Diagram
```mermaid
%% classDiagram
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

---

## API Interaction Flow - Sequence Diagrams (Task 2)

### Purpose
Illustrate how requests flow through the layered architecture for key operations, showing responsibilities and data flow.

### Diagram
```mermaid
%% ## 1. User Registration

**Overview**: Creates a new user account by validating the provided information and securely storing it in the database.

```mermaid
sequenceDiagram
    autonumber
    participant U as Client
    participant P as Presentation Layer
    participant B as Business Logic
    participant D as Database

    U->>P: POST /api/v1/users/register<br/>{first_name, last_name, email, password}
    
    Note over P: Validate request format
    P->>B: register_new_user(user_data)
    
    Note over B: Check email format<br/>Verify email uniqueness<br/>Hash password with bcrypt<br/>Generate UUID and timestamps
    B->>D: INSERT user (id, first_name, last_name, email, password_hash, is_admin, created_at, updated_at)
    
    D-->>B: User record created
    B-->>P: User object (sanitized, no password)
    P-->>U: 201 Created<br/>{user_id, email, first_name, last_name, created_at}
```

---

## 2. Place Creation

**Overview**: Enables authenticated users to list a new property with details and location information.

```mermaid
sequenceDiagram
    autonumber
    participant U as Client
    participant P as Presentation Layer
    participant B as Business Logic
    participant D as Database

    Note over U: User is authenticated
    U->>P: POST /api/v1/places<br/>{title, description, price, latitude, longitude, owner_id}
    
    P->>P: Verify authentication token
    Note over P: Extract user_id from token
    
    P->>B: create_new_place(place_data, user_id)
    
    Note over B: Validate coordinates range<br/>Check price is positive<br/>Verify required fields<br/>Generate UUID, set timestamps
    B->>D: INSERT place (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
    
    D-->>B: Place ID returned
    
    Note over B: Link amenities if provided
    loop For each amenity
        B->>D: INSERT place_amenity (place_id, amenity_id)
    end
    
    B-->>P: Place object with amenities
    P-->>U: 201 Created<br/>{place_id, title, price, owner_id, amenities[]}
```

---

## 3. Review Submission

**Overview**: Allows users to submit ratings and feedback for places they have experienced.

```mermaid
sequenceDiagram
    autonumber
    participant U as Client
    participant P as Presentation Layer
    participant B as Business Logic
    participant D as Database

    U->>P: POST /api/v1/places/{place_id}/reviews<br/>{rating, comment}
    
    P->>P: Authenticate user
    Note over P: Get user_id from session
    
    P->>B: submit_review(place_id, user_id, review_data)
    
    B->>D: SELECT place WHERE id = place_id
    D-->>B: Place details
    
    Note over B: Verify place exists<br/>Check user is not owner<br/>Validate rating (1-5)<br/>Generate UUID, timestamps
    
    B->>D: INSERT review (id, place_id, user_id, rating, comment, created_at, updated_at)
    
    D-->>B: Review created successfully
    B-->>P: Review object
    P-->>U: 201 Created<br/>{review_id, place_id, rating, comment, created_at}
```

---

## 4. Fetching a List of Places

**Overview**: Retrieves places based on search criteria, including associated amenities and owner information.

```mermaid
sequenceDiagram
    autonumber
    participant U as Client
    participant P as Presentation Layer
    participant B as Business Logic
    participant D as Database

    U->>P: GET /api/v1/places?price_min=100&price_max=500&location=nearby
    
    P->>B: get_places_list(filters)
    
    Note over B: Parse and validate filters<br/>Build query conditions
    B->>D: SELECT * FROM places WHERE price BETWEEN 100 AND 500 AND location criteria met
    
    D-->>B: List of matching places
    
    loop For each place in results
        B->>D: SELECT amenities WHERE place_id = ?
        D-->>B: Amenities list
        
        B->>D: SELECT user WHERE id = owner_id
        D-->>B: Owner info
        
        Note over B: Attach amenities and owner to place
    end
    
    B-->>P: Enriched places list
    P-->>U: 200 OK<br/>[{place_id, title, price, owner, amenities[]}, ...]
```

---

## Summary

These diagrams demonstrate the interaction patterns for core HBnB operations:

- **User Registration**: Focuses on data validation and secure password storage
- **Place Creation**: Shows authentication flow and relationship building with amenities
- **Review Submission**: Enforces business rules preventing owners from reviewing their properties
- **Fetching Places**: Demonstrates query filtering and data aggregation from multiple tables

Each operation follows the layered architecture with clear separation between presentation, business logic, and data persistence concerns.
