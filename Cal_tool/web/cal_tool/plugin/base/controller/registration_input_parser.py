from django.shortcuts import redirect
from cal_tool.models import Users
import re
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher, make_password


class BaseRegistrationInputParser:
    def __init__(self):
        self.context = {}


    def parse_input(self, request):
        """
        Parses request information about registration into a tuple containing
            1. The validity of the params (True/False)
            2. The parsed params into a dictionary with their post value as main key
                and value and status as subkeys
        :param request:
        :return:        Returns True, self.context on success,
                        Returns False, self.context on failure
        """
        required_params_valid = self.check_and_parse_required_params_valid(request)
        remaining_params_valid = self.check_and_parse_remaining_params_valid(request)
        if required_params_valid and remaining_params_valid:
            uid = Users.generate_new_id()
            uname = self.context["uname"]["value"]
            password = self.context["password1"]["value"]
            password = make_password(password )
            email = self.context["email"]["value"]
            role = Users.USER
            domain = Users.BASE
            new_user = Users(unique_id=uid,
                             username=uname,
                             password=password,
                             mail=email, role=role,
                             domain=domain)
            new_user.save()
            return True, self.context
        return False, self.context

    # ------------------------------------------------------------------------------------------------------------------
    # Main check and set functions of required and unrequired params

    def check_and_parse_required_params_valid(self, request):
        """
        Checks required params and parses them into self.context for each parameter from post.
        Each param from POST and/or GET will be parsed with 2 additional params
            1. value:   Containing the original value
            2. status:  Containg the status of the parameter (VALID/INVALID)
        :param request: Uwsgi-request object containing POST and GET params
        :return:        Returns True if all required params are valid,
                        Returns False otherwise
        """
        uname = request.POST.get("uname")
        uname_status = "VALID"
        password1 = request.POST.get("password1")
        password1_status = "VALID"
        password2 = request.POST.get("password2")
        password2_status = "VALID"

        data_valid = True
        if uname is None or not self.check_uname_available(uname):
            data_valid = False
            uname_status = "INVALID"
        if password1 is None:
            data_valid = False
            password1_status = "INVALID"
        if password2 is None:
            data_valid = False
            password2_status = "INVALID"
        if password1 is not None and password2 is not None:
            if password1 != password2 or len(password1) < 8 or len(password2) < 8:
                data_valid = False
                password1_status = "INVALID"
                password2_status = "INVALID"

        self.context["uname"] = { "value": uname, "status": uname_status }
        self.context["password1"] = { "value": password1, "status": password1_status }
        self.context["password2"] = { "value": password2, "status": password2_status }

        return data_valid

    def check_and_parse_remaining_params_valid(self, request):
        """
        Checks required params and parses them into self.context for each parameter from post.
        Each param from POST and/or GET will be parsed with 2 additional params
            1. value:   Containing the original value
            2. status:  Containg the status of the parameter (VALID/INVALID)
        :param request: Uwsgi-request object containing POST and GET params
        :return:        Returns True if all required params are valid,
                        Returns False otherwise
        """
        email = request.POST.get("email")
        if email == "":
            email = None
        email_status = "VALID"

        data_valid = True
        if not  self.check_mail_valid(email):
            data_valid = False
            email_status = "INVALID"

        self.context["domain"] = {"value": int(request.POST.get("domain")), "status": "VALID"}

        self.context["email"] = {"value": email, "status": email_status}
        return data_valid

    @staticmethod
    def check_login_status(request):
        """
        Checks if user is logged in
        :param request: Uwsgi request containing page information
        :return:        Returns True if user is logged in,
                        Returns False otherwise
        """
        try:
            user = request.session['user_id']
            if Users.objects.filter(unique_id=user).count()==1:
                return True
            else:
                return False
        except Exception:
            return False


    # ------------------------------------------------------------------------------------------------------------------
    # Helper functions

    @staticmethod
    def check_mail_valid(p_email):
        if p_email == "" or p_email is None:
            return True
        mail_taken = Users.objects.filter(mail=p_email).count() > 0
        if not mail_taken and re.match("^.+@([?)[a-zA-Z0-9-.])+\.([a-zA-Z]{2,3}|[0-9]{1,3})$", p_email) is not None:
            return True
        return False

    @staticmethod
    def check_uname_available(p_uname):
        users = Users.objects.filter(username=p_uname)
        if users.count() > 0:
            return False
        return True