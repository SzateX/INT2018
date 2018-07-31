$(document).ready(
    function()
    {
        $("tr").click(function(event){
            if(!$(event.target).hasClass("no-click"))
            {
                if($(event.target).parent()[0].hasAttribute("href"))
                {
                    location.href = $(event.target).parent().attr("href");
                }
            }
        });

        $('select').formSelect();

        $('.datepicker').datepicker({format:'yyyy-mm-dd'});
        $('.timepicker').timepicker({twelveHour:false, format: "HH:ii:SS"});

        $('.timepicker').on('change', function() {
            receivedVal = $(this).val();
        $(this).val(receivedVal + ":00");
    });

        $('.sidenav').sidenav();
    }
);