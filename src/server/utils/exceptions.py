class ClientException(Exception):
    status_code: int

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class ResourceNotFoundException(ClientException):
    resource_id: str | int
    resource_name: str

    def __init__(self, resource_id: str | int, resource_name: str = "Resource"):
        self.status_code = 404
        self.resource_id = resource_id

        super().__init__(404, f"{resource_name} with id {resource_id} not found")


class ResourceWrongTypeError(ClientException):
    resource_id: str
    resource_type: str
    correct_type: str

    def __init__(self, resource_id: str, resource_type: str, correct_type: str):
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.correct_type = correct_type

        super().__init__(
            400,
            f"Resource with id {resource_id} is of type {resource_type}, but should be of type {correct_type}",  # noqa: E501
        )
