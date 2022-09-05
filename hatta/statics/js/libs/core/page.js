class Page {
    constructor() {
        $("#hatta-content").html($("#hatta-content").html().replace(/(>[^<>\,\.]\s*<)/g, "><"));
    }
    
    start() {
    
    }
    
    fix_hatta_content_container() {
        $("#hatta-content").html($("#hatta-content").html().replace(/(>[^<>\,\.]\s*<)/g, "><"));
    }
}

$('#body').ready(function() {
    var page = new Page();
    page.start();
});

