🏨 HBnB Evolution — Part 1
Technical Documentation & UML Architecture

Project: HBnB Evolution – UML
Team: Ali Abdullah Summan • Ali Hassan Almaghrabi • Omar Hail Alanzi
School: Holberton School
Date: December 2025

📌 Overview

This repository contains the technical documentation and UML design for Part 1 of the HBnB Evolution application — a simplified AirBnB-style platform.

The goal of this phase is to provide a complete architectural blueprint before implementation begins, ensuring clarity, maintainability, and clean separation of responsibilities across system layers.

This documentation will guide the development work in later project stages, including persistence, REST APIs, deployment, and user-facing features.

🧱 System Architecture Summary

HBnB Evolution is designed following a 3-layer architecture:

Layer	Responsibilities
Presentation Layer	API endpoints, service handlers, request validation
Business Logic Layer	Core models, business rules, facade pattern
Persistence Layer	Repositories / data access, storage communication

The Facade Pattern is central to the design — it exposes a unified entry point for business logic, ensuring loose coupling between layers.

📂 Repository Structure
part1/
├── README.md                  # This file
├── diagrams/
│   ├── high_level_architecture.md
│   ├── class_diagram.md
│   ├── sequence_user_registration.md
│   └── sequence_list_places.md


💡 Keeping diagrams modular makes iteration easier during development.

🧭 Deliverables Included
Requirement	Status	Description
High-Level Package Diagram	✔️ Completed	Architecture using 3-layer model + facade
Business Logic Class Diagram	✔️ Completed	Entities: User, Place, Review, Amenity
API Sequence Diagrams	✔️ Completed	Registration, place creation, review submission, list places
Documentation Compilation	✔️ Completed	Unified technical document


🧩 Diagrams Summary

🔷 High-Level Package Diagram

✔ Demonstrates layered architecture
✔ Shows facade interaction between Presentation & Business Logic

🏗️ Class Diagram (Business Logic)

✔ Models include required attributes & methods
✔ UUID, timestamps, entity relationships, many-to-many places ↔ amenities

🔁 Sequence Diagrams
Use Case	Highlights
User Registration	Creates user through facade + repository
Place Creation	User-owned entity creation, mapping to DB
Review Submission	Connects user ↔ place ↔ review
List Places	Fetches filtered place data


📝 Design Principles Applied

Separation of Concerns

Single Responsibility Principle

Facade Pattern

Encapsulation of Business Rules

Consistent Entity Auditing (timestamps, UUIDs)


📌 Why This Design?

✔ Supports scalability and modularity
✔ Keeps API logic independent from data storage
✔ Allows persistence layer changes without affecting business logic
✔ Clear entry point for business operations via Facade

This ensures future tasks — database implementation, API development, UI rendering — can be built on a stable and well-structured foundation.


🤝 Authors
Name	Role
Ali Abdullah Summan	Business  / Package diagram
Ali Hassan Almaghrabi / Class diagram
Omar Hail Alanzi	 / Sequence diagrams



“A solid architecture is the first step toward a successful system.”
— Holberton Method
