from flask import request
from flask_restx import Namespace, Resource

from app.helpers.response import (
    get_success_response,
    get_failure_response,
    parse_request_body,
    validate_required_fields,
)
from app.helpers.decorators import login_required
from common.services.todo import TodoService
from common.app_config import config

# Create the todo blueprint
todo_api = Namespace("todo", description="Todo-related APIs")


@todo_api.route("")
class Todos(Resource):
    @login_required()
    def get(self, person):
        """Get all todos for the current user with optional filtering."""
        filter_type = request.args.get("filter", "all")  # all, active, completed
        todo_service = TodoService(config)

        if filter_type == "completed":
            todos = todo_service.get_completed_todos(person.entity_id)
        elif filter_type == "active":
            todos = todo_service.get_active_todos(person.entity_id)
        else:
            todos = todo_service.get_todos_by_person(person.entity_id)

        return get_success_response(todos=[todo.as_dict() for todo in todos])

    @login_required()
    @todo_api.expect(
        {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
            },
        }
    )
    def post(self, person):
        """Create a new todo."""
        parsed_body = parse_request_body(request, ["title"])
        validate_required_fields({"title": parsed_body["title"]})

        todo_service = TodoService(config)
        todo = todo_service.create_todo(
            person_id=person.entity_id,
            title=parsed_body["title"],
        )
        return get_success_response(
            todo=todo.as_dict(), message="Todo created successfully."
        )

    @login_required()
    def delete(self, person):
        """Delete all completed todos."""
        todo_service = TodoService(config)
        todo_service.delete_completed_todos(person.entity_id)
        return get_success_response(message="All completed todos deleted successfully.")


@todo_api.route("/complete")
class TodoCompleteAll(Resource):
    @login_required()
    def post(self, person):
        """Mark all todos as completed."""
        todo_service = TodoService(config)
        todo_service.complete_all_todos(person.entity_id)
        return get_success_response(message="All todos marked as completed.")


@todo_api.route("/activate")
class TodoActivateAll(Resource):
    @login_required()
    def post(self, person):
        """Mark all todos as active."""
        todo_service = TodoService(config)
        todo_service.activate_all_todos(person.entity_id)
        return get_success_response(message="All todos marked as active.")


@todo_api.route("/<string:todo_id>")
class TodoItem(Resource):
    @login_required()
    def get(self, todo_id, person):
        """Get a specific todo."""
        todo_service = TodoService(config)
        todo = todo_service.get_todo_by_id(todo_id)

        if not todo or todo.person_id != person.entity_id:
            return get_failure_response("Todo not found", status_code=404)

        return get_success_response(todo=todo.as_dict())

    @login_required()
    @todo_api.expect(
        {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "is_completed": {"type": "boolean"},
            },
        }
    )
    def patch(self, todo_id, person):
        """Update a specific todo."""
        parsed_body = parse_request_body(request, ["title", "is_completed"])
        validate_required_fields({"title": parsed_body["title"]})

        todo_service = TodoService(config)
        todo = todo_service.get_todo_by_id(todo_id)

        if not todo or todo.person_id != person.entity_id:
            return get_failure_response("Todo not found", status_code=404)

        updated_todo = todo_service.update_todo_by_id(
            entity_id=todo_id,
            title=parsed_body["title"],
            is_completed=parsed_body["is_completed"],
        )
        return get_success_response(
            todo=updated_todo.as_dict(), message="Todo updated successfully."
        )
        

    @login_required()
    def delete(self, todo_id, person):
        """Delete a todo."""
        todo_service = TodoService(config)
        todo = todo_service.get_todo_by_id(todo_id)

        if not todo or todo.person_id != person.entity_id:
            return get_failure_response("Todo not found", status_code=404)

        todo_service.delete_todo_by_id(todo)
        return get_success_response(message="Todo deleted successfully.")


@todo_api.route("/<string:todo_id>/toggle")
class TodoToggle(Resource):
    @login_required()
    def put(self, todo_id, person):
        """Toggle the completion status of a todo."""
        todo_service = TodoService(config)
        todo = todo_service.get_todo_by_id(todo_id)

        if not todo or todo.person_id != person.entity_id:
            return get_failure_response("Todo not found", status_code=404)

        updated_todo = todo_service.toggle_todo_by_id(todo_id)
        return get_success_response(
            todo=updated_todo.as_dict(),
            message=f"Todo marked as {'completed' if updated_todo.is_completed else 'active'}.",
        )

