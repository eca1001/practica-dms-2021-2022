""" TeacherEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template, request
from werkzeug.wrappers import Response
from dms2122common.data import Role
from dms2122frontend.data.rest.authservice import AuthService
from .webauth import WebAuth
#from .webquestion import WebQuestion


class TeacherEndpoints():
    """ Monostate class responsible of handing the teacher web endpoint requests.
    """
    @staticmethod
    def get_teacher(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the teacher root endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        return render_template('teacher.html', name=name, roles=session['roles'])

    
    @staticmethod
    def get_teacher_questions(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the questions administration endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']

        #test values until backfront is completed
        questions=[ {"title" : "Pregunta de prueba 1", "body" : "cuerpo pregunta 1",
                        "option1" : "A", "option2" : "B", "option3" : "C", 
                        "correct_answer": 1, "punctuation": 1.5, "penalty": 0.5},
                    {"title" : "Pregunta de prueba 2", "body" : "cuerpo pregunta 2",
                        "option1" : "A", "option2" : "B", "option3" : "C", 
                        "correct_answer": 3, "punctuation": 1, "penalty": 0.2}
                   ]     

        return render_template('teacher/questions.html', name=name, roles=session['roles'], 
                                    questions=questions)
    
    @staticmethod
    def get_teacher_students(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the student progress endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        return render_template('teacher/students.html', name=name, roles=session['roles'])

    
    @staticmethod
    def get_teacher_questions_new(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the question creation endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        redirect_to = request.args.get('redirect_to', default='/teacher/questions')
        return render_template('teacher/questions/new.html', name=name, 
                                roles=session['roles'], redirect_to=redirect_to)

    @staticmethod
    def post_teacher_questions_new(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the POST requests to the question creation endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))

        redirect_to = request.args.get('redirect_to', default='/teacher/questions')        
        return redirect(redirect_to)
    
    @staticmethod
    def get_teacher_questions_edit(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the question editing endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        title: str = str(request.args.get('questiontitle'))
        redirect_to = request.args.get('redirect_to', default='/teacher/questions')
        return render_template('teacher/questions/edit.html', name=name, roles=session['roles'], 
            redirect_to=redirect_to, title=title, body="(aqui ira el cuerpo cuando tengamos el backend)", 
            option1="(lo mismo)", option2="(lo mismo 2)", option3="(lo mismo 3)",correct_answer=3, 
            punctuation=1.5, penalty=0.5)

    @staticmethod
    def post_teacher_questions_edit(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the POST requests to the question editing endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))

        redirect_to = request.args.get('redirect_to', default='/teacher/questions')        
        return redirect(redirect_to)
    
    @staticmethod
    def get_teacher_questions_preview(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the question preview endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        title: str = str(request.args.get('questiontitle'))
        redirect_to = request.args.get('redirect_to', default='/teacher/questions')  
        return render_template('teacher/questions/preview.html', name=name, roles=session['roles'],
                                redirect_to=redirect_to, title=title)
    
    @staticmethod
    def get_teacher_questions_stats(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the question statistics endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        return render_template('teacher/questions/stats.html', name=name, roles=session['roles'])