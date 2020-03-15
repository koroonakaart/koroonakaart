var current_place_name = 'Eesti';
var current_place_confirmed = 135;
var current_place_active = 134;
var current_place_in_treatment = 2;
var current_place_deaths = 0;
var current_place_recovered = 1;
var zoomLevel = 'county';
// TODO: Is there a way we can import this data without jQuery? Then we could drop jQuery.
var json = $.getJSON({'url': "/koroonakaart/data/topojson/population.json", 'async': false});


// Initialize Vue app
const vue_app = new Vue({
    el: '#content',
    data: {
        current_place_name: current_place_name,
        current_place_confirmed: current_place_confirmed.toLocaleString(),
        current_place_active: current_place_active.toLocaleString(),
        current_place_in_treatment: current_place_in_treatment.toLocaleString(),
        current_place_deaths: current_place_deaths.toLocaleString(),
        current_place_recovered: current_place_recovered.toLocaleString(),
        zoomLevel: zoomLevel
    },
    methods: {
        changeMap() {
            console.log(this.zoomLevel)
            var elements = document.getElementsByTagName('path');
            while (elements[0]) elements[0].parentNode.removeChild(elements[0]);
            if (this.zoomLevel === "country") {
                drawCounties();
            }
            if (this.zoomLevel === "county") {
                drawCounties();
            }
            if (this.zoomLevel === "municipality") {
                drawMunicipalities();
            }
        },
    },
    mounted: function () {
        this.$nextTick(function () {
            // console.log(json);

            console.log("In mounted hook.", this);
        });
    }
});
