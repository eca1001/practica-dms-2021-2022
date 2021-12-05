""" StudentEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template, request
from werkzeug.wrappers import Response
from dms2122common.data import Role
from dms2122frontend.data.rest.authservice import AuthService
from .webauth import WebAuth
from .webquestion import WebQuestion
from .webanswer import WebAnswer


class StudentEndpoints():
    """ Monostate class responsible of handling the student web endpoint requests.
    """
    @staticmethod
    def get_student(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the student root endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Student.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        return render_template('student.html', name=name, roles=session['roles'])

    @staticmethod
    def get_student_questions(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the questions menu endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Student.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        return render_template('student/questions.html', name=name, roles=session['roles'])
    
    @staticmethod
    def get_student_progress(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the student progress endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Student.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        return render_template('student/progress.html', name=name, roles=session['roles'])

    @staticmethod
    def get_student_questions_answered(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the student's answered questions endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Student.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']

        #test values until backfront is completed
        answers=[ {"title" : "Pregunta de prueba 3", "score" : "1"}]
        return render_template('student/questions/answered.html', name=name, roles=session['roles'],
                                answers=answers)

    @staticmethod
    def get_student_questions_answered_view(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the student's answered questions viewing endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Student.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        title: str = str(request.args.get('questiontitle'))
        redirect_to = request.args.get('redirect_to', default='/student/questions/answered')
        return render_template('student/questions/answered/view.html', name=name, 
                                roles=session['roles'], redirect_to=redirect_to, title=title)

    @staticmethod
    def get_student_questions_pending(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the student's pending questions endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Student.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']

        #test values until backfront is completed
        questions=[ {"title" : "Pregunta de prueba 1", "body" : "cuerpo pregunta 1",
                        "option1" : "A", "option2" : "B", "option3" : "C", 
                        "correct_answer": 1},
                    {"title" : "Pregunta de prueba 2", "body" : "cuerpo pregunta 2",
                        "option1" : "A", "option2" : "B", "option3" : "C", 
                        "correct_answer": 3}
                   ] 
        redirect_to = request.args.get('redirect_to', default='/student/questions/pending')
        return render_template('student/questions/pending.html', name=name, roles=session['roles'],
                            questions=questions)

    @staticmethod
    def get_student_questions_pending_answer(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the question answering endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Student.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        title: str = str(request.args.get('questiontitle'))
        redirect_to = request.args.get('redirect_to', default='/student/questions/pending')
        return render_template('student/questions/pending/answer.html', name=name, 
                                roles=session['roles'], redirect_to=redirect_to, title=title)

    @staticmethod
    def post_student_questions_pending_answer(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the question answering endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Student.name not in session['roles']:
            return redirect(url_for('get_home'))
        
        redirect_to = request.args.get('redirect_to', default='/student/questions/pending')
        return redirect(redirect_to)