var current_place_name = 'Eesti';
var current_place_confirmed = 135;
var current_place_active = 134;
var current_place_in_treatment = 2;
var current_place_deaths = 0;
var current_place_recovered = 1;
var current_place_population = 1317762;
var zoomLevel = 'county';
// TODO: Is there a way we can import this data without jQuery? Then we could drop jQuery.
var json = $.getJSON({'url': "/data/topojson/population.json", 'async': false});


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
        current_place_population: current_place_population.toLocaleString(),
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
    computed: {
        current_place_confirmed_percent() {
            const population_by_place = {
                'Eesti': 1328000,
                'Harju maakond': 163497,
                'Hiiu maakond': 9387,
                'Ida-Viru maakond': 76519,
                'Jõgeva maakond': 28734,
                'Järva maakond': 30286,
                'Lääne maakond': 20507,
                'Lääne-Viru maakond': 59325,
                'Põlva maakond': 25006,
                'Pärnu maakond': 85938,
                'Rapla maakond': 33311,
                'Saare maakond': 33108,
                'Tartu maakond': 152977,
                'Valga maakond': 2837,
                'Viljandi maakond': 46371,
                'Võru maakond': 35782
            }

            return this.current_place_confirmed / population_by_place[this.current_place_name];
        }
    },
    mounted: function () {
        this.$nextTick(function () {
            // console.log(json);

            console.log("In mounted hook.", this);
        });
    }
});
