class Refresh {
    constructor() {
        this.refresh = parseInt(Hatta.get_query_parameter("refresh", "60"));
    }

    start() {
        console.log(new Datetime().datetime_as_ISO_string + " start (refresh=" + this.refresh + ")!");
        this.timeout = window.setTimeout(function() {window.location.reload()}, (this.refresh * 60) * 1000, this);
    }
}
