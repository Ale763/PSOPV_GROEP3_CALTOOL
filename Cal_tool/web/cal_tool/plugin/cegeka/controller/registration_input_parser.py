from cal_tool.plugin.base.controller.registration_input_parser import *


class CegekaRegistrationInputParser(BaseRegistrationInputParser):
    def __init__(self):
        super().__init__()

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
            domain = Users.CEGEKA
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

        self.context["email"] = {"value": email, "status": email_status}
        return data_valid

    # ------------------------------------------------------------------------------------------------------------------
    # Helper functions

    @staticmethod
    def check_mail_valid(p_email):
        if p_email == "" or p_email is None:
            return True
        mail_taken = Users.objects.filter(mail=p_email).count() > 0
        # Add this to make uhasselt plugin only to UHasselt students: and re.match("^.+@([?)[a-zA-Z0-9-.])*\.?cegeka\.be$", p_email) is not None
        if not mail_taken :
            return True
        return False
