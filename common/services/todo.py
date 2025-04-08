from uuid import UUID
from common.repositories.factory import RepositoryFactory, RepoType
from common.models.todo import Todo
from app.helpers.exceptions import InputValidationError


class TodoService:
    """Service class for managing Todo operations."""

    def __init__(self, config):
        self.config = config
        self.repository_factory = RepositoryFactory(config)
        self.todo_repo = self.repository_factory.get_repository(RepoType.TODO)

    def create_todo(self, person_id: str, title: str) -> Todo:
        """
        Create a new todo item.

        :param person_id: ID of the person creating the todo
        :param title: Title of the todo
        :return: Created Todo object
        """
        todo = Todo(person_id=person_id, title=title)
        todo.prepare_for_save(changed_by_id=person_id)
        return self.todo_repo.save(todo)

    def get_todo_by_id(self, entity_id: str) -> Todo:
        """
        Get a todo by its ID.

        :param entity_id: ID of the todo
        :return: Todo object if found, None otherwise
        """
        return self.todo_repo.get_one({"entity_id": entity_id})

    def toggle_todo_by_id(self, entity_id: str) -> Todo:
        """
        Toggle the completion status of a todo.

        :param entity_id: ID of the todo
        :return: Updated Todo object
        """
        todo = self.get_todo_by_id(entity_id)
        if not todo:
            raise InputValidationError("Todo not found")
        if todo:
            todo.is_completed = not todo.is_completed
            self.todo_repo.save(todo)
        return todo

    def update_todo_by_id(self, entity_id: str, title: str, is_completed: bool) -> Todo:
        """
        Update a todo item.

        :param entity_id: ID of the todo
        :param title: New title for the todo
        :param is_completed: New completion status for the todo
        :return: Updated Todo object
        """
        todo = self.get_todo_by_id(entity_id)
        if not todo:
            raise InputValidationError("Todo not found")
        todo.title = title
        todo.is_completed = is_completed
        self.todo_repo.save(todo)
        return todo

    def delete_todo_by_id(self, entity_id: str) -> None:
        self.todo_repo.delete(entity_id)

    def get_todos_by_person(self, person_id: str) -> list[Todo]:
        """
        Get all todos for a person.

        :param person_id: ID of the person
        :return: List of Todo objects
        """
        return self.todo_repo.get_many({"person_id": person_id})

    def get_completed_todos(self, person_id: str = None) -> list[Todo]:
        """
        Get all completed todos, optionally filtered by person.

        :param person_id: Optional ID of the person to filter by
        :return: List of completed Todo objects
        """
        filters = {"is_completed": True, "active": True}
        if person_id:
            filters["person_id"] = person_id
        return self.todo_repo.get_many(filters)

    def get_active_todos(self, person_id: str = None) -> list[Todo]:
        """
        Get all active (not completed) todos, optionally filtered by person.

        :param person_id: Optional ID of the person to filter by
        :return: List of active Todo objects
        """
        filters = {"is_completed": False, "active": True}
        if person_id:
            filters["person_id"] = person_id
        return self.todo_repo.get_many(filters)

    def delete_completed_todos(self, person_id: str) -> None:
        """
        Delete all completed todos for a person.

        :param person_id: ID of the person
        """
        completed_todos = self.get_completed_todos(person_id)
        for todo in completed_todos:
            self.todo_repo.delete(todo)


    def complete_all_todos(self, person_id: str) -> None:
        """
        Mark all todos as completed for a person.

        :param person_id: ID of the person
        """
        active_todos = self.get_active_todos(person_id)
        for todo in active_todos:
            todo.is_completed = True
            self.todo_repo.save(todo)

    def activate_all_todos(self, person_id: str) -> None:
        """
        Mark all todos as active for a person.

        :param person_id: ID of the person
        """
        completed_todos = self.get_completed_todos(person_id)
        for todo in completed_todos:
            todo.is_completed = False
            self.todo_repo.save(todo)