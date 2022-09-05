class Page {
    static app = undefined;
    static refresh = undefined;

    static start(app) {
        /*--- Vue application (components) start. ---*/
        Page.app = app;
        Page.app.start();
        /*--- Other code blocks are started via refresh instance. ---*/
        Page.refresh = new Refresh();
        Page.refresh.start();
    }

    static fix_hatta_content_container() {
        //$("#hatta-content").html($("#hatta-content").html().replace(/(>[^<>\,\.]\s*<)/g, "><"));
        $("#hatta-content").html("X");
    }

    static get_current_url() {
        return window.location.href;
    }

    static get_query_parameter(key_name, default_value) {
        var key = "";
        var value = "";
        var query_string = window.location.search.substring(1);
        var vars = query_string.split("&");
        var pair = ["", ""];
        for (var i = 0; i < vars.length; i++) {
            pair = vars[i].split("=");
            key = decodeURIComponent(pair[0]);
            value = decodeURIComponent(pair[1]);
            if (key_name.toLowerCase() === key.toLowerCase()) {
                return value;
            }
        }
        return default_value;
    }
}
