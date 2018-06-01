class NewCalendar
{
    constructor()
    {
        this.m_sources = [];
        this.m_sourcesCount = -1;
        this.m_filterWidgets = [];
    }

    getFilter(id){
        return this.m_filterWidgets[id];
    }

    getSource(id) { return this.m_sources[id] }

    saveAllFilters(p_melding){
        let i = 0;
        for(i = 0; i<=this.m_sourcesCount; ++i) {
            this.m_filterWidgets[i].saveFilter(p_melding);
        }
    }

    saveUrl(id){
        let source = $("#urlInput"+id.toString()).val();
        $.ajax({
            url: '/ajax/add_source/',
            data: {
                'id': id,
                'source':source,
                'type': 'url'
            },
            type: "post",
            dataType: 'json',
            success: function (result) {}
        });
    }

    saveFile(id){
        let source = $("#fileInput"+id.toString()).val();
        $.ajax({
            url: '/ajax/add_source/',
            data: {
                'id': id,
                'source':source,
                'type': 'file'
            },
            type: "post",
            dataType: 'json',
            success: function (result) {}
        });
    }

    saveCourse(id){
        let source = $("#sourceInput"+id.toString()+" option:selected").val().split(";")[0];
        $.ajax({
            url: '/ajax/add_source/',
            data: {
                'id': id,
                'source':source,
                'type': 'file'
            },
            type: "post",
            dataType: 'json',
            success: function (result) {}
        });
    }

    createNewSource()
    {
        this.m_sourcesCount++;                                      // Set new amount of sources
        let newsource = new SourceWidget(this.m_sourcesCount);      // Create new sourceWidget start params
        let newfilter = new FilterWidget(this.m_sourcesCount);

        this.m_filterWidgets[this.m_sourcesCount] = newfilter;
        this.m_sources[this.m_sourcesCount] = newsource;            // Add new widget to list
        let createdSourceWidget = newsource.createSourceWidget();   // Create the widget

        $("#generated-sources").append(createdSourceWidget);        // Add widget to html
        newsource.addTitleListener();                               // Add eventListener to newSourceWidget

        this.materialize_elements_init();                           // Add dynamic components to new widget

        $("#filterWidget").attr("id", "filterWidget"+this.m_sourcesCount.toString());
        let filterwidget = $("#filterWidget"+this.m_sourcesCount.toString()).find(".newfilter");
        filterwidget.attr("onclick", "newCalendar.getFilter("+ this.m_sourcesCount+").addFilter()");
    }

    // TODO:: Fix validation focus: https://stackoverflow.com/questions/22148080/an-invalid-form-control-with-name-is-not-focusable
    // TODO:: Adding form input control
    deleteSource(id)
    {
        let sliceLen = "#sourceWidget".length;
        let id_nr = parseInt(id.slice(sliceLen), 10);
        let i = 0;
        let id_passed = false;
        let sourceWidgets = $(".sourceWidgets");
        for(i=0; i <= this.m_sourcesCount; ++i)
        {
            if (i !== id_nr && id_passed)
            {
                // Change id of sourceWidget
                let old_id = i.toString();
                let new_id = (i-1).toString();
                let sourceWidget = $("#sourceWidget"+old_id);
                sourceWidget.attr("id", "sourceWidget"+new_id);
                let widget = this.m_sources[new_id].changeId(sourceWidget, old_id, new_id);
                this.m_sources[i-1].setId(parseInt(new_id));
            }
            else if (i === id_nr)
            {
                // Remove sourceWidget
                this.m_sources.splice(i, 1);
                sourceWidgets[i].remove();
                id_passed = true;
            }
        }

        this.deleteFilterWidget(id);

        this.m_sourcesCount--;
    }

    deleteFilterWidget(p_id){
        let sliceLen = "#sourceWidget".length;
        let id_nr = parseInt(p_id.slice(sliceLen), 10);
        let i = id_nr + 1;
        for(i; i <= this.m_sourcesCount; ++i)
        {
            let filterwidget = $("#filterWidget"+(i-1).toString()).find(".newfilter");
            filterwidget.attr("onclick", "newCalendar.getFilter("+ (i-1)+").addFilter()");
            this.m_filterWidgets[i].changeAllFiltersId(i-1);
            this.m_filterWidgets[i].setId(i-1);
            $("#filterWidget"+i.toString()).attr("id", "filterWidget"+(i-1).toString());
        }
        this.m_filterWidgets.splice(id_nr, 1);
    }

    materialize_elements_init()
    {
        let sourceWidgetId = "#sourceWidget"+this.m_sourcesCount.toString();
        let collapsible = $(sourceWidgetId +".collapsible");
        let select = $(sourceWidgetId+" select");

        collapsible.collapsible();  // Collapsible dynamic functionality
        // $(".collapsible-header").addClass("active");
        // $(".collapsible").collapsible({accordion: false});
        select.material_select();   // Select dynamic functionality
    }
}

class SourceWidget
{
    constructor(p_id)
    {
        this.m_id = p_id;
    }

    getId() {return this.m_id;}

    setId(id) {this.m_id = id;}

    addTitleListener()
    {
        let id = "#sourceWidget"+this.m_id.toString();
        let sourceWidgetName =  $(id+" .source_name");
        let sourceWidgetTitle = $(id+" .source_title");

        // Change title based on calendar_source name
        sourceWidgetName.keyup(function()
        {
            let defaultvalue = "New source";
            let input = sourceWidgetName.val();
            if(input !== "")
            {
                sourceWidgetTitle.text(input);
            }
            else
            {
                sourceWidgetTitle.text(defaultvalue);
            }
        });
    }

    sourceTypeSwitcher()
    {
        let id = this.m_id.toString();
        let sourceWidgetId = "#sourceWidget"+id;

        let selected_val = $(sourceWidgetId+" .selector input").prop("value");  // Get select value

        // Change source input type based on chosen type in select
        if(selected_val === "Bestand")
        {
            $(sourceWidgetId+" .File").show();
            $(sourceWidgetId+" .File input").prop("required", true);

            $(sourceWidgetId+" .URL input").prop("required", false);
            $(sourceWidgetId+" .URL").hide();

            $(sourceWidgetId+" .Source").hide();
            $(sourceWidgetId+" .Source input").prop("required", false);

        }
        else if(selected_val === "URL")
        {
            $(sourceWidgetId+" .File input").prop("required", false);
            $(sourceWidgetId+" .File").hide();

            $(sourceWidgetId+" .URL").show();
            $(sourceWidgetId+" .URL input").prop("required", true);

            $(sourceWidgetId+" .Source").hide();
            $(sourceWidgetId+" .Source input").prop("required", false);
        }
        else {
            $(sourceWidgetId+" .File input").prop("required", false);
            $(sourceWidgetId+" .File").hide();

            $(sourceWidgetId+" .URL").hide();
            $(sourceWidgetId+" .URL input").prop("required", false);

            $(sourceWidgetId+" .Source").show();
            $(sourceWidgetId+" .Source input").prop("required", true);
        }


    }

    createSourceWidget()
    {

        let new_id = this.m_id.toString();
        let sourceWidget = $("#sourceWidget").clone();  // Clone sourcewidget html
        let t = this.changeId(sourceWidget, "", new_id);// Change id of new widget
        t.find(" .File");                       // Show file input source
        t.find(" .File").show();
        t.find(" .URL");
        t.find(" .URL").hide();
        t.find(" .Source");
        t.find(" .Source").hide();                         // Hide url input source
        return t;
    }

    changeId(sourceWidget, old_id, new_id)
    {
        // Change ids of all important components for dynamic functionality and input
        this.m_id = parseInt(new_id);
        sourceWidget.attr("id", "sourceWidget"+new_id);

        let calendarName = sourceWidget.find("#calendarName"+old_id);
        calendarName.attr("id", "calendarName"+ new_id) ;
        calendarName.attr("name", "calendarName"+ new_id);

        let sourceType = sourceWidget.find("#sourceType"+old_id);
        sourceType.attr("id", "sourceType"+new_id);
        sourceType.attr("name","sourceType"+new_id);
        sourceType.attr("onchange", "newCalendar.getSource("+new_id+").sourceTypeSwitcher('#urlInput"+ new_id+"')") ;

        let urlInput = sourceWidget.find("#urlInput"+old_id);
        urlInput.attr("id", "urlInput"+ new_id) ;
        urlInput.attr("name", "urlInput"+ new_id)
        urlInput.attr("onchange", "newCalendar.saveUrl("+new_id+")") ;

        let sourceInput = sourceWidget.find("#sourceInput"+old_id);
        sourceInput.attr("id", "sourceInput"+ new_id) ;
        sourceInput.attr("name", "sourceInput"+ new_id);
        sourceInput.attr("onchange", "newCalendar.saveCourse("+new_id+")") ;

        let fileInput = sourceWidget.find("#fileInput"+old_id);
        fileInput.attr("id", "fileInput"+ new_id) ;
        fileInput.attr("name", "fileInput"+ new_id);
        fileInput.attr("onchange", "newCalendar.saveFile("+new_id+")") ;

        let deleteSourceFunction = sourceWidget.find("#deleteSource"+old_id);
        deleteSourceFunction.attr("id", "deleteSource"+new_id);
        deleteSourceFunction.attr("onclick", "newCalendar.deleteSource('#sourceWidget"+ new_id+"')") ;

        return sourceWidget;
    }
}

class FilterWidget
{
    constructor(id) {
        this.m_filters = [];
        this.m_filterCount = -1;
        this.m_id=id;
        this.m_activeFilter=-1;
    }

    setId(p_id){
        this.m_id=p_id;
    }

    makeFilterVisible(p_number){
        let i = 0;
        let filterWidgets = $("#filterWidget"+this.m_id.toString());
        for(i=0; i <= this.m_filterCount; ++i)
        {
            if (i === p_number){
                $("#"+this.m_id.toString()+"filter"+ i.toString()).attr("style", "display: block;");
                filterWidgets.find(".filterTab"+i.toString()).find("a").attr("class", "active link");
                filterWidgets.find(".addAttribute").attr("onclick", "newCalendar.getFilter("+ this.m_id+").addAttribute("+i+")");
            }
            else {
                $("#"+this.m_id.toString()+"filter"+ i.toString()).attr("style", "display: none;");
                filterWidgets.find(".filterTab" + i.toString()).find("a").attr("class", "link");
            }

        }
        this.m_activeFilter=p_number;
    }

    changeAllFiltersId(p_newId){
        let i = 0;
        let filterWidgets = $("#filterWidget"+this.m_id.toString());
        for(i=0; i <= this.m_filterCount; ++i) {
            filterWidgets.find("#"+this.m_id.toString()+"filter"+i.toString()).attr("id", p_newId.toString()+"filter"+i.toString());
            filterWidgets.find(".deleteFilter").attr("onclick", "newCalendar.getFilter("+p_newId+").deleteFilter()") ;
            //filterWidgets.find(".saveFilter").attr("onclick", "newCalendar.getFilter("+p_newId+").saveFilter()") ;
            filterWidgets.find(".filterTab"+i.toString()).find("a").attr("onclick", "newCalendar.getFilter("+p_newId+").makeFilterVisible("+i+")");
        }
        filterWidgets.find(".newfilter").attr("onclick", "newCalendar.getFilter("+p_newId+").addFilter()");
    }

    addFilter(){
        this.m_filterCount += 1;
        let newFilter = new Filter(this.m_filterCount);
        this.m_filters[this.m_filterCount] = newFilter;

        let filtercount = this.m_filterCount;
        let filterWidget = $("#filterWidget"+this.m_id.toString());
        let filtercontent = filterWidget.find(".filterContent");
        let filterId = this.m_id;

        if (this.m_filterCount == 0) {
            filtercontent.attr('style', "display: inline;");
            $(".saveFilter").attr('style', "float: right; display: inline;")
        }

        filtercontent.append('<div class="col s12 m12 l12" id="'+this.m_id.toString()+'filter'+ filtercount.toString() +'" style="display: none;"></div>');
        filterWidget.find("#"+this.m_id.toString()+"filter"+ filtercount.toString()).load("/newcalendar/filter.html", function() {
            filterWidget.find(".addTab").append('<li class="tab filterTab'+ filtercount.toString() +'"><a onclick="newCalendar.getFilter('+ filterId.toString() +').makeFilterVisible('+ filtercount.toString() +')" class="link">Filter '+(filtercount+1).toString()+'</a></li>');
            filterWidget.find(".deleteFilter").attr("onclick", "newCalendar.getFilter("+ filterId+").deleteFilter()");
            filterWidget.find(".addAttribute").attr("onclick", "newCalendar.getFilter("+ filterId+").addAttribute("+filtercount+")");
        });
        this.makeFilterVisible(filtercount);
        $('ul.tabs').tabs();
    }

    addHTMLattribute(p_filterId, p_addedAttributeId){
        let filterAttributes = $("#"+this.m_id.toString()+"filter"+p_filterId.toString()).find(".filterAttributes");

        let filterAttributesDiv = $("#"+this.m_id.toString()+"filter"+p_filterId.toString()).find(".filterAttributesDiv");
        filterAttributesDiv.attr("style", "overflow-y: scroll; max-height: 150px; display: block;");

        let mode = $(".AttributeMode option:selected").html();
        let not = $('#AttributeNegation').is(":checked");
        let value = $("#AttributeValue").val();
        if (value == ""){
            let calwidget = $('.datepicker').pickadate();
            value = calwidget[0].value;
        }
        let type = $(".AttributeFilter option:selected").html();

        if(value == ""){
            alert("Please fill in a value");
            return;
        }

        if (!not)
            filterAttributes.append("<tr class='filterAttribute"+p_addedAttributeId+"'><td class='faAttribute'>"+type+"</td><td class='faMode'>"+mode+"</td><td class='faNot' style='visibility: hidden'>niet</td><td class='faValue'>"+value+"</td><td><i class='material-icons iconButton right sourceDelete deleteAttribute' onclick='newCalendar.getFilter("+this.m_id+").deleteAttribute("+p_filterId+", "+p_addedAttributeId+")'>delete</i></td></tr>");
        else
            filterAttributes.append("<tr class='filterAttribute"+p_addedAttributeId+"'><td class='faAttribute'>"+type+"</td><td class='faMode'>"+mode+"</td><td class='faNot'>niet</td><td class='faValue'>"+value+"</td><td><i class='material-icons iconButton right sourceDelete deleteAttribute' onclick='newCalendar.getFilter("+this.m_id+").deleteAttribute("+p_filterId+", "+p_addedAttributeId+")'>delete</i></td></tr>");

        mode = $(".AttributeMode option:selected").val();
        type = $(".AttributeFilter option:selected").val();

        this.m_filters[p_filterId].addAttributeData(p_addedAttributeId, mode, not, value, type);
    }

    addAttribute(p_id){
        let addedId = this.m_filters[p_id].getNextAttributeId();
        $(".saveFilterAttribute").attr("onclick", "newCalendar.getFilter("+this.m_id+").addHTMLattribute("+p_id+", "+addedId+")");
    }

    deleteAttribute(p_filterID, p_attributeId){
        this.m_filters[p_filterID].deleteAttribute(this.m_id, p_filterID, p_attributeId);
        newCalendar.saveAllFilters();
    }

    deleteFilter(){
        let id = this.m_activeFilter;
        let i = 0;
        let id_passed = false;
        for(i=0; i <= this.m_filterCount; ++i)
        {
            if (i !== id && id_passed)
            {
                // Change id of filterWidget
                let old_id = i.toString();
                let new_id = (i-1).toString();
                let filterWidget = $("#"+this.m_id.toString()+"filter"+old_id);
                let filterTab = $(".filterTab"+old_id);
                filterWidget.find(".addAttribute").attr("onclick", "newCalendar.getFilter("+ this.m_id+").addAttribute("+new_id+")");
                filterTab.html('<a  class="link" onclick="newCalendar.getFilter('+ this.m_id.toString() +').makeFilterVisible('+new_id+')">Filter '+ i.toString() +'</a>');
                filterTab.attr("class", "filterTab"+new_id+" tab");
                this.m_filters[new_id].changeId(filterWidget, old_id, new_id, this.m_id);
                this.m_filters[i-1].setId(parseInt(new_id));
            }
            else if (i === id)
            {
                $( ".filterTab"+ id.toString()).remove();
                $( "#"+this.m_id.toString()+"filter"+ id.toString()).remove();
                id_passed = true;
            }
        }
        if(this.m_activeFilter == this.m_filterCount)
            this.makeFilterVisible(id-1);
        else
            this.makeFilterVisible(id);

        this.m_filterCount--;

        newCalendar.saveAllFilters();

        if (this.m_filterCount == -1){
            $(".filterContent").attr('style', "display: none;");
            $(".saveFilter").attr('style', "float: right; display: none;");
            let div = $("#sourceWidget"+this.m_id.toString()).find("#filterResultsDiv");
            div.attr("style", "display: none; overflow-y: scroll; max-height: 200px;");
        }
    }

    saveFilter(p_meding){
        let i = 0;
        let id = this.m_id.toString();
        var list = [];
        for(i=0; i<=this.m_filterCount;++i){
            let filter = [];
            let filterdata = $("#"+this.m_id.toString()+"filter"+i.toString());
            let filterName = filterdata.find(".filterName").val();
            let attributeList = this.m_filters[i].saveAttributes();

            if(filterName == "" && p_meding){
                alert("Please enter a name for filter"+(i+1).toString());
                return false;
            }
            if(attributeList.length === 0 && p_meding){
                alert("Please add an attribute for filter "+(i+1).toString());
                return false;
            }

            filter[0] = filterName;
            filter[1] = attributeList;
            list[i] = filter;
        }
        $.ajax({
            url: '/ajax/save_filter/',
            type: 'post',
            data: {
                'data': JSON.stringify(list),
                'id': this.m_id
            },
            dataType: 'json',
            success: function (result) {
                let table = $("#sourceWidget"+id).find("#filterResults");
                let div = $("#sourceWidget"+id).find("#filterResultsDiv");
                table.html("");
                if(result.length > 0)
                    div.attr("style", "display: block; overflow-y: scroll; max-height: 200px;");
                else {
                    div.attr("style", "display: none; overflow-y: scroll; max-height: 200px;");
                    return;
                }

                let i = 0;
                for (i = 0; i<result.length; ++i) {
                    let event = result[i];
                    let html = "<tr><td>"+event['summary']+"</td><td>"+event['start']+"</td><td>"+event['end']+"</td></tr>";
                    table.append(html);
                }
            }
        });
        return true;
    }
}

class Filter
{
    constructor(p_id)
    {
        // this.m_source_id = p_source_id;
        this.m_id=p_id;
        this.m_attributes = [];
        this.m_attributesCount = -1;
    }

    getFilterAttribute(p_id){
        return this.m_attributes[p_id];
    }

    setId(p_id){
        this.m_id=p_id;
    }

    getNextAttributeId(){
        return this.m_attributesCount+1;
    }

    addAttributeData(p_id, p_mode, p_not, p_value, p_type){
        this.addAttribute();
        this.m_attributes[p_id].loadData(p_mode, p_not, p_value, p_type);
    }

    changeId(p_filter, p_old_id, p_new_id, p_filterId){
        // Change ids of all important components for dynamic functionality and input
        this.m_id = parseInt(p_new_id);
        p_filter.attr("id", p_filterId+"filter"+p_new_id);

        let filterName = p_filter.find("#filterName"+p_old_id);
        filterName.attr("id", "filterName"+ p_new_id) ;
        filterName.attr("name", "filterName"+ p_new_id);
    }
    addAttribute()
    {
        this.m_attributesCount +=1;
        let newAttribute = new FilterAttribute(this.m_attributesCount);
        this.m_attributes[this.m_attributesCount] = newAttribute;
        return this.m_attributesCount;
    }

    deleteAttribute(p_filterWidgetId, p_filterId, p_id){
        let i = p_id;
        let id_passed = false;
        for(i=p_id; i <= this.m_attributesCount; ++i)
        {
            let filterAttribute = $("#"+p_filterWidgetId.toString()+"filter"+p_filterId.toString()).find(".filterAttribute"+i.toString());
            if (i !== p_id && id_passed)
            {
                let new_id = (i-1);
                filterAttribute.find(".deleteAttribute").attr("onclick", "newCalendar.getFilter("+p_filterWidgetId+").deleteAttribute("+p_filterId+", "+new_id+")");
                filterAttribute.attr("class", "filterAttribute"+new_id.toString());
                this.m_attributes[i].setId(new_id);
                this.m_attributes[i-1]=this.m_attributes[i];
            }
            else if (i === p_id)
            {
                id_passed=true;
                filterAttribute.remove();
            }
        }

        let filterAttributeDiv = $("#"+p_filterWidgetId.toString()+"filter"+p_filterId.toString()).find(".filterAttributesDiv");
        if(this.m_attributesCount == 0)
            filterAttributeDiv.attr("style", "overflow-y: scroll; max-height: 150px; display: none");

        this.m_attributesCount--;
    }

    saveAttributes(){
        let i = 0;
        let attributeList = [];
        for(i = 0;i<=this.m_attributesCount; ++i){
            attributeList[i] = this.m_attributes[i].getData();
        }
        return attributeList;
    }
}

class FilterAttribute
{
    constructor(p_id){
        this.m_id = p_id;
        this.m_mode = "";
        this.m_type = "";
        this.m_value = "";
        this.m_not = false;
    }

    setId(p_id){
        this.m_id=p_id;
    }

    loadData(p_mode, p_not, p_value, p_type){
        var isTrueSet = p_not;
        this.m_mode = p_mode;
        this.m_not = isTrueSet;
        this.m_value = p_value;
        this.m_type = p_type;
    }

    getData(){
        let attribute = {};
        attribute["MODE"] = this.m_mode.toString().toUpperCase();
        attribute["NOT"] = this.m_not;
        attribute["VALUE"] = this.m_value;
        attribute["TYPE"] = this.m_type.toString().toUpperCase();
        return attribute;
    }
}

function changeDatePicker() {
    let type = $(".AttributeFilter option:selected").html();
    if (type.indexOf("datum")>=0){
        $("#calendarDate").attr("style", "display: inline-block");
        $("#valuePicker").attr("style", "display: none");
    }
    else {
        $("#calendarDate").attr("style", "display: none");
        $("#valuePicker").attr("style", "display: inline-block");
    }
}

$('#newCalendarForm').submit(function(evt)
{
    let submitButtonContainer = $("#SubmitButton").parent();
    let preloader = $(".resources .preloader-wrapper").clone();
    preloader.addClass("right" );
    submitButtonContainer.html(preloader);
    $(document.documentElement).click(function (evt) { evt.stopPropagation();});
});

$('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15, // Creates a dropdown of 15 years to control year,
    today: 'Today',
    clear: 'Clear',
    close: 'Ok',
    closeOnSelect: false, // Close upon selecting a date,
    container: undefined, // ex. 'body' will append picker to body
  });

$("#newCalendarForm").submit(function (e) {
    newCalendar.saveAllFilters(false);
});

let newCalendar = new NewCalendar();
newCalendar.createNewSource();

$("#header").addClass("active");
$("#header").collapsible({accordion: false});



