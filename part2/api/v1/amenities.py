#!/usr/bin/env python3
"""
Amenity endpoints for HBnB API
"""

from flask_restx import Namespace, Resource, fields
from business_logic.facade import facade  # use facade for data access

api = Namespace("amenities", description="Amenity operations")

# Swagger input model
amenity_input = api.model("AmenityInput", {
    "name": fields.String(required=True)
})

# Swagger output model
amenity_output = api.model("AmenityOutput", {
    "id": fields.String,
    "name": fields.String
})

# serialize Amenity object to dict
def serialize_amenity(amenity):
    return {"id": amenity.id, "name": amenity.name}

# Route for list of amenities and creating new amenity
@api.route("/")
class AmenityList(Resource):
    @api.expect(amenity_input)
    @api.marshal_with(amenity_output, code=201)
    def post(self):
        # Create a new amenity using facade
        data = api.payload
        amenity = facade.create_amenity(name=data.get("name"))
        return serialize_amenity(amenity), 201

    @api.marshal_list_with(amenity_output)
    def get(self):
        # Get all amenities from facade
        amenities = facade.list_amenities()
        return [serialize_amenity(a) for a in amenities]

# Route for specific amenity operations
@api.route("/<string:amenity_id>")
class AmenityItem(Resource):
    @api.marshal_with(amenity_output)
    def get(self, amenity_id):
        # Retrieve single amenity by ID
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return serialize_amenity(amenity)

    @api.expect(amenity_input)
    @api.marshal_with(amenity_output)
    def put(self, amenity_id):
        # Update an existing amenity using facade
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        updated = facade.update_amenity(amenity_id, name=api.payload.get("name"))
        return serialize_amenity(updated)
