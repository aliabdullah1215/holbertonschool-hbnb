#!/usr/bin/env python3
from flask_restx import Namespace, Resource, fields
from business_logic.facade import facade

api = Namespace("places", description="Place operations")

place_input = api.model("PlaceInput", {
    "name": fields.String(required=True),
    "owner_id": fields.String(required=True),
    "description": fields.String(required=False),
    "price": fields.Float(required=False),
    "latitude": fields.Float(required=False),
    "longitude": fields.Float(required=False),
    "amenity_ids": fields.List(fields.String, required=False)
})

review_small = api.model("ReviewSmall", {
    "id": fields.String,
    "text": fields.String,
    "user_id": fields.String,
    "place_id": fields.String
})

place_output = api.model("PlaceOutput", {
    "id": fields.String,
    "name": fields.String,
    "owner_id": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "amenity_ids": fields.List(fields.String),
    "reviews": fields.List(fields.Nested(review_small))
})

def serialize_review_small(r):
    return {
        "id": r.id,
        "text": r.text,
        "user_id": r.user_id,
        "place_id": r.place_id
    }

def serialize_place(place):
    try:
        reviews = facade.list_reviews_by_place(place.id)
    except ValueError:
        reviews = []

    return {
        "id": place.id,
        "name": place.name,
        "owner_id": place.owner_id,
        "description": getattr(place, "description", ""),
        "price": getattr(place, "price", 0.0),
        "latitude": getattr(place, "latitude", None),
        "longitude": getattr(place, "longitude", None),
        "amenity_ids": getattr(place, "amenity_ids", []),
        "reviews": [serialize_review_small(r) for r in reviews]
    }

@api.route("/")
class PlaceList(Resource):
    @api.expect(place_input)
    @api.marshal_with(place_output, code=201)
    def post(self):
        data = api.payload
        if "price" in data and data["price"] < 0:
            api.abort(400, "Price cannot be negative")
        try:
            place = facade.create_place(
                name=data.get("name"),
                owner_id=data.get("owner_id"),
                description=data.get("description", ""),
                price=data.get("price", 0.0),
                latitude=data.get("latitude"),
                longitude=data.get("longitude"),
                amenity_ids=data.get("amenity_ids", [])
            )
        except ValueError as e:
            api.abort(404, str(e))
        return serialize_place(place), 201

    @api.marshal_list_with(place_output)
    def get(self):
        return [serialize_place(p) for p in facade.list_places()]

@api.route("/<string:place_id>")
class PlaceItem(Resource):
    @api.marshal_with(place_output)
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return serialize_place(place)

    @api.expect(place_input)
    @api.marshal_with(place_output)
    def put(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        data = api.payload
        if "price" in data and data["price"] < 0:
            api.abort(400, "Price cannot be negative")
        updated = facade.update_place(place_id, **data)
        return serialize_place(updated)
