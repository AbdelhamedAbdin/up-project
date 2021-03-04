$(document).ready(function() {
    // Add active on category
    let access_url = window.location,
        target_url = $("nav .taping a").toArray(),
        i;
    for (i = 0; i < target_url.length; i++) {
        let target = target_url[i];
        if (access_url.pathname == target.pathname) {
            $(target).addClass("active").siblings().removeClass("active");
        } else {
            $(target).removeClass("active");
        }
    }

    // Add classes on login form
    $('.login input[type="text"]').attr({"placeholder": "Email", 'class': 'form-control'});
    $('.login input[type="password"]').attr({"placeholder": "Password", 'class': 'form-control', 'id': 'password-field'});

    // search and filter

});