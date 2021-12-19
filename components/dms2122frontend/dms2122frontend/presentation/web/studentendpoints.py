""" StudentEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template, request, flash
from werkzeug.wrappers import Response
from dms2122common.data import Role
from dms2122frontend.data.rest.authservice import AuthService
from dms2122frontend.data.rest.backendservice import BackendService
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
    def get_student_progress(auth_service: AuthService, backend_service: BackendService) -> Union[Response, Text]:
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
    def get_student_questions_answered(auth_service: AuthService, backend_service: BackendService) -> Union[Response, Text]:
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

        return render_template('student/questions/answered.html', name=name, roles=session['roles'],
                                questions=WebQuestion.list_answered_for_user(backend_service, name))

    @staticmethod
    def get_student_questions_answered_view(auth_service: AuthService, backend_service: BackendService) -> Union[Response, Text]:
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
        id: int = int(str(request.args.get('questionid')))
        redirect_to = request.args.get('redirect_to', default='/student/questions/answered')

        return render_template('student/questions/answered/view.html', name=name, 
                                roles=session['roles'], redirect_to=redirect_to, 
                                question = WebQuestion.get_question(backend_service ,id),
                                answer=WebAnswer.get_answer(backend_service, name, id) 
                                )

    @staticmethod
    def get_student_questions_pending(auth_service: AuthService, backend_service: BackendService) -> Union[Response, Text]:
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

        return render_template('student/questions/pending.html', name=name, roles=session['roles'],
                            questions=WebQuestion.list_pending_for_user(backend_service,name))

    @staticmethod
    def get_student_questions_pending_answer(auth_service: AuthService, backend_service: BackendService) -> Union[Response, Text]:
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
        id: int = int(str(request.args.get('questionid')))
        redirect_to = request.args.get('redirect_to', default='/student/questions/pending')
        return render_template('student/questions/pending/answer.html', name=name, 
            roles=session['roles'], redirect_to=redirect_to, question = WebQuestion.get_question(backend_service ,id))

    @staticmethod
    def post_student_questions_pending_answer(auth_service: AuthService, backend_service: BackendService) -> Union[Response, Text]:
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

        selected = str(request.form['option'])
        number_selected = 0
        if selected == 'option1':
            number_selected = 1
        elif selected == 'option2':
            number_selected = 2
        elif selected == 'option3':
            number_selected = 3

        new_answer = WebAnswer.answer_question(backend_service,
                                                int(request.form['id']),
                                                number_selected,
                                                str(name))

        if not new_answer:
            return redirect(url_for('get_student_questions_pending'))
        redirect_to = request.form['redirect_to']
        if not redirect_to:
            redirect_to = url_for('get_student_questions_pending')
        return redirect(redirect_to)