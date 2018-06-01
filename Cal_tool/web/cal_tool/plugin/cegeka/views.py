from cal_tool.plugin.base.views import *

class CegekaViewPlugin(ViewPlugin):
    def __init__(self, p_logo):
        super(CegekaViewPlugin,self).__init__(p_template_path="cegeka/template.html", p_logo=p_logo)

    # --------------------------------------------------------------------------------------------------------------------
    # Views


    @method_decorator(login_required)
    def redirect_mycalendars(self, request,context = None):
        return render(request, 'cegeka/mycalendars.html', {'context': context})
    

