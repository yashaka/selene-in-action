import pydantic


class User(pydantic.BaseModel):
    """
    User model, that can be used to validate response from API,
    or to model in UI tests,
    the info of whom should be easier reused in different places.

    Example:
        >>> import requests
        >>> from selene_in_action.model.data.user import User
        >>> response = requests.get('https://reqres.in/api/users/2')
        >>> user = User(**response.json().get('data'))
    """

    id: int
    email: str
    firstName: str
    lastName: str
    avatar: str
