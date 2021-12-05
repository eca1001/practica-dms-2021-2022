""" BackendService class module.
"""

from typing import Optional
import requests
from dms2122common.data import Role
from dms2122common.data.rest import ResponseData


class BackendService():
    """ REST client to connect to the backend service.
    """

    def __init__(self,
        host: str, port: int,
        api_base_path: str = '/api/v1',
        apikey_header: str = 'X-ApiKey-Backend',
        apikey_secret: str = ''
        ):
        """ Constructor method.

        Initializes the client.

        Args:
            - host (str): The backend service host string.
            - port (int): The backend service port number.
            - api_base_path (str): The base path that is prepended to every request's path.
            - apikey_header (str): Name of the header with the API key that identifies this client.
            - apikey_secret (str): The API key that identifies this client.
        """
        self.__host: str = host
        self.__port: int = port
        self.__api_base_path: str = api_base_path
        self.__apikey_header: str = apikey_header
        self.__apikey_secret: str = apikey_secret

    def __base_url(self) -> str:
        """ Constructs the base URL for the requests.

        Returns:
            - str: The base URL.
        """
        return f'http://{self.__host}:{self.__port}{self.__api_base_path}'

    def list_questions(self, token: Optional[str]) -> ResponseData:
        """ Requests a list of created questions.

        Args:
            token (Optional[str]): The user session token.

        Returns:
            - ResponseData: If successful, the contents hold a list of question data dictionaries.
              Otherwise, the contents will be an empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + '/questions',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def create_question(self, token: Optional[str], title: str,  body: str, option1: str, option2: str, option3: str,
             correct_answer: int, punctuation: float, penalty: float) -> ResponseData:
        """ Requests a question creation.

        Args:
            - token (Optional[str]): The user session token.
            - username (str): The new user's name.
            - password (str): The new user's password.

        Returns:
            - ResponseData: If successful, the contents hold the new question's data.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + '/question/new',
            json={
                'title': title,
                'body': body,
                'option1': option1,
                'option2': option2,
                'option3': option3,
                'correct_answer': correct_answer,
                'punctuation': punctuation,
                'penalty': penalty
            },
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def get_question(self, token: Optional[str], id: int) -> ResponseData:
        """ Requests a specific question.

        Args:
            token (Optional[str]): The user session token.

        Returns:
            - ResponseData: If successful, the contents hold the requested question data.
              Otherwise, the contents will be an empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/question/{id}',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data


    def question_has_answers(self, token: Optional[str], id: str) -> ResponseData:
        """ Checks if a question has been answered by anyone.

        Args:
            - token (Optional[str]): The user session token.
            - username (str): The name of the queried user.

        Returns:
            - ResponseData: If successful, the contents hold a value of true. Otherwise an
              empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/question/{id}/answers/',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data
    
    def answer_question(self, token: Optional[str], id: int, number: int, username: str) -> ResponseData:
        """ Requests a question creation.

        Args:
            - token (Optional[str]): The user session token.
            - username (str): The new user's name.
            - password (str): The new user's password.

        Returns:
            - ResponseData: If successful, the contents hold the new question's data.
        """

        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f'/question/{id}/answer{username}',
            json={
                'username': username,
                'number': number,
                'id': id
            },
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def list_all_for_question(self, token: Optional[str], id: int) -> ResponseData:
        """ Requests a list of answers for a certain question.

        Args:
            token (Optional[str]): The user session token.

        Returns:
            - ResponseData: If successful, the contents hold a list of question data dictionaries.
              Otherwise, the contents will be an empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/answers/{id}',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def list_all_for_user(self, token: Optional[str], username: str) -> ResponseData:
        """ Requests a list of answers for a certain user.

        Args:
            token (Optional[str]): The user session token.

        Returns:
            - ResponseData: If successful, the contents hold a list of question data dictionaries.
              Otherwise, the contents will be an empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/answers/{username}',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data