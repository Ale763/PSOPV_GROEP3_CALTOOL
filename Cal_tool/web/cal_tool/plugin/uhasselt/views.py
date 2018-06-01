import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator

from cal_tool.models import Filters
from cal_tool.plugin.base.views import ViewPlugin
from cal_tool.filter.FilterUHasselt import FilterUHasselt, FilterAttributes
from cal_tool.plugin.uhasselt.filter_attributes import filter_attributes_uhasselt

class UHasseltViewPlugin(ViewPlugin):
    def __init__(self, p_logo):
        super(UHasseltViewPlugin,self).__init__(p_template_path="uhasselt/template.html", p_logo=p_logo)
        self.setFilterAttributes(filter_attributes_uhasselt)

    # --------------------------------------------------------------------------------------------------------------------
    # Views

    @method_decorator(login_required)
    def newcalendar(self,request):
        context = {}
        context["filter_attributes"] = self.getFilterAttributes()
        return render(request, 'uhasselt/newcalendar.html', context)





    def save_filter(self, request):
        data = json.loads(request.POST.get('data', None))
        id = request.POST.get('id', None)

        request.session["filter" + str(id)] = None
        request.session["filteredsource" + str(id)] = None

        filter_list = []

        for filter in data:
            new_id = Filters.generate_new_id()
            new_filter = FilterUHasselt(new_id, filter[0])
            for filterAttribute in filter[1]:
                value = new_filter.string_to_datetime(filterAttribute["TYPE"], filterAttribute["VALUE"])
                new_filter.add_attribute(filterAttribute["TYPE"], filterAttribute["MODE"], filterAttribute["NOT"], value)
            filter_list.append(new_filter)


        request.session["filter"+str(id)] = filter_list

        if "source"+str(id) in request.session and request.session.get("source"+str(id), None) is not None:
            self.filter_source(request)

        return self.load_events(request, int(id))