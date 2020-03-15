var current_place_name = 'Eesti';
var current_place_confirmed = 135;
var zoomLevel = 'county';
// TODO: Is there a way we can import this data without jQuery? Then we could drop jQuery.
var json = $.getJSON({'url': "/koroonakaart/data/topojson/population.json", 'async': false});


// Initialize Vue app
const vue_app = new Vue({
    el: '#content',
    data: {
        current_place_name: current_place_name,
        current_place_confirmed: current_place_confirmed.toLocaleString(),
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
