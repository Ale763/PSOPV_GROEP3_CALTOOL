window.addEventListener("load", function ()
{
    var pk = new Piklor(".color-picker", [
            "#F0A3FF"
            ,"#0075DC"
            ,"#993F00"
            ,"#4C005C"
            ,"#191919"
            ,"#005C31"
            ,"#2BCE48"
            ,"#FFCC99"
            ,"#808080"
            ,"#94FFB5"
            ,"#8F7C00"
            ,"#9DCC00"
            ,"#C20088"
            ,"#003380"
            ,"#FFA405"
            ,"#FFA8BB"
            ,"#426600"
            ,"#FF0010"
            ,"#5EF1F2"
            ,"#00998F"
            ,"#E0FF66"
            ,"#740AFF"
            ,"#990000"
            ,"#FFFF80"
            ,"#FFFF00"
            ,"#FF5005"
        ], {
            open: ".picker-wrapper .btn"
        })
      , colorInput = pk.getElm("#newCalendarColor")
      , colorPicker = pk.getElm("#newCalendarColorPicker")
      , footer = pk.getElm("footer")
      ;

    pk.colorChosen(function (col)
    {
        colorPicker.style.backgroundColor = col;
        colorInput.value = col;
        // header.style.backgroundColor = col;
        // footer.style.backgroundColor = col;
    });
});
