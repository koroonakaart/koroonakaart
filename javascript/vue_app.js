var current_year = 2018;
var current_place_name = 'Estonia';
var current_place_population = 1317762;
var zoomLevel = 'county';
var json = $.getJSON({'url': "/statistics-explorer/data/json/population.json", 'async': false});


// Initialize Vue app
const vue_app = new Vue({
    el: '#content',
    data: {
        current_year: current_year,
        current_place_name: current_place_name,
        current_place_population: current_place_population.toLocaleString(),
        zoomLevel: zoomLevel
    },
    methods: {
        updatePopulation() {
            updatePopulationByYear(this.current_year);
        },

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

        changePyramid() {
            document.getElementById("pyramid").innerHTML = "";
            pyramidBuilder(json.responseJSON[this.current_year], '#pyramid', {height: 400, width: 500});
        }
    },
    mounted: function () {
        this.$nextTick(function () {
            console.log(json);
            pyramidBuilder(json.responseJSON["2018"], '#pyramid', {height: 400, width: 500});
            console.log("In mounted hook.", this);
        });
    }
});