$(document).ready(function(){
    // Ajax code to like a category
    $('#likes').click(function(){
        var catid;
        catid = $(this).attr("data-catid");
        $.get('/rango/like_category', {category_id: catid},
        function(data){
            $('#like_count').html(data);
            $('#likes').hide();
        });
    });
    $('#dislikes').click(function(){
        var catid;
        catid = $(this).attr("data-catid");
        $.get('/rango/dislike_category', {category_id: catid}, function(data){
            $('#like_count').html(data);
            $('#dislikes').hide()
        });
    });

    // To update the category list according to input
    $('#suggestion').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/rango/suggest_category/', {suggestion: query},
        function(data){
            $('#cats').html(data);
        });
    });
});