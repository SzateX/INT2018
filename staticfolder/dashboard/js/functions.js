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
    }
);