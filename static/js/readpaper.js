window.onload = function() {

    $("#submit_comment").click(function() {
        var paperid = $("#paperid").text();
        var comment = $("#write_comment").val();
        var date = new Date();

        data = {
            "paperid": paperid,
            "content": comment,
            "time": date.getTime()
        };

        $.ajax({
            type: "POST",
            url: "/comment/add",
            data: JSON.stringify(data, null, '\t'),
            contentType: "application/json;charset=UTF-8",
            success: function(result) {
                result = JSON.parse(result)
                commentid = result["commentid"];
                username = result["username"];
                time = result["time"]
                html = "<div class=\"existed_comment\" id="+commentid.toString()+" >"
                    +"<div class=\"comment_header\">"
                    +"<span class=\"comment_author\">"+username+"    "+"</span>"
                    +"<span class=\"comment_time\">"+time+"</span></div>"
                    +"<div class=\"comment_content\">"+comment+"</div></div>";
                $(".existed_comments").append(html);
                $("#write_comment").val("");
            } 
        })
    });

}