from flask import request
from flask_restx import Namespace, Resource

from app.helpers.response import get_success_response, parse_request_body, validate_required_fields
from app.helpers.decorators import login_required
from common.services.person import PersonService
from common.app_config import config

# Create the organization blueprint
person_api = Namespace('person', description="Person-related APIs")


@person_api.route('/me')
class Me(Resource):
    
    @login_required()
    def get(self, person):
        return get_success_response(person=person)

    @login_required()
    @person_api.expect(
        {'type': 'object', 'properties': {
            'first_name': {'type': 'string'},
            'last_name': {'type': 'string'},
        }}
    )
    def patch(self, person):
        parsed_body = parse_request_body(request, ['first_name', 'last_name'])
        validate_required_fields(parsed_body)

        person_service = PersonService(config)
        person_obj = person_service.update_person_name(
            person,
            parsed_body['first_name'],
            parsed_body['last_name']
        )

        return get_success_response(
            message="Profile updated successfully.", 
            person=person_obj.as_dict()
        )