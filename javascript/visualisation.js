// Set dimensions
var width = 600,
    height = 500,
    active = d3.select(null);

// Projection
var projection = d3.geoMercator()
    // .fitExtent([ [0, 0], [800, 600] ], counties);
    .center([25.0136, 58.5953])
    .scale([5000])
    .translate([width / 2, height / 2]);

// Path
var path = d3.geoPath()
    .projection(projection);


function drawCounties() {
    // Colour
    var population_domain = [0, 1, 5, 10, 25, 50, 100, 250];
    // var population_domain = [0, 50, 250, 500, 1000, 5000];
    var population_colour = d3.scaleThreshold()
        .domain(population_domain)
        .range(d3.schemeBlues[9]);

    // Population data
    var prevalence_data = d3.map();

    var svg = d3.select("svg#map_prevalence");

    svg.append("rect")
        .attr("width", width)
        .attr("height", height);
    // svg.append("rect")
    //     .attr("width", width)
    //     .attr("height", height)
    //     .on("click", clicked);

    var g = svg.append("g");
    // Load TopoJSON maps and data asynchronously.
    d3.queue()
        .defer(d3.json, "/data/topojson/counties.json")
        .defer(d3.csv, "/data/counties.csv", function (d) {
            // Debug
            console.log(d);
            prevalence_data.set(d.id, +d['confirmed']);
        })
        .await(ready);

    // Define legend settings
    var legendText = ["0", "1", "5", "10", "25", "50", "100", "250"];
    // var legendColors = ["#C6DBEF","#9ecae1", "#63afd7", "#2171b5", "#08519c", "#08306b"];
    var legendColors = ["#9ecae1", "#63afd7", "#4ea2d9", "#4292c6", "#2171b5", "#08519c", "#1f4884", "#08306b"];

    function ready(error, data) {
        if (error) throw error;

        // Debug
        console.log('');
        console.log('data:');
        console.log(data);
        console.log('prevalence_data:');
        console.log(prevalence_data);
        console.log('');

        // Load population data
        var counties = topojson.feature(data, {
            type: "GeometryCollection",
            geometries: data.objects.maakond.geometries  // counties
            // geometries: data.objects.omavalitsus.geometries // municipalities
            // geometries: data.objects.asustusyksus.geometries // settlements
        });

        // Draw the map
        g.append("g")
            .attr("id", "counties")
            .selectAll("path")
            .data(counties.features)
            .enter()
            .append("path")
            .attr("d", path)
            .attr("fill", function(d) {
                return population_colour(d.population = prevalence_data.get(d.properties.MKOOD));
            });
        g.append("g")
            .attr("id", "counties")
            .selectAll("path")
            .data(counties.features)
            .enter()
            .append("path")
            .attr("d", path)
            .attr("fill", function(d) {
                return population_colour(d.population = prevalence_data.get(d.properties.MKOOD));
            })
            .on("click", clicked);

        g.append("path")
            .datum(topojson.mesh(data, data.objects.maakond, function(a, b) { return a !== b; }))
            .attr("id", "county_borders")
            .attr("d", path);

        // var legend = svg.append("g")
        var legend = d3.select("svg#legend")
            .attr("id", "legend");

        var legenditem = legend.selectAll(".legenditem")
            .data(d3.range(8))
            .enter()
            .append("g")
            .attr("class", "legenditem")
            .attr("transform", function(d, i) { return "translate(" + i * 42 + ",0)"; });

        legenditem.append("rect")
            .attr("x", width - 600)
            .attr("y", 0)
            .attr("width", 120)
            .attr("height", 10)
            .attr("class", "rect")
            .style("fill", function(d, i) { return legendColors[i]; });

        legenditem.append("text")
            .attr("x", width - 600)
            .attr("y", 20)
            .style("text-anchor", "right")
            .text(function(d, i) { return legendText[i]; });
    }

    function clicked(d) {
        // Debug
        console.log(d)
        console.log(d.population);
        console.log("Map was clicked.");
        if (typeof d !== 'undefined') {
            console.log(d.properties.MNIMI);
            vue_app.current_place_name = d.properties.MNIMI;
            vue_app.current_place_confirmed = parseInt(d.population,10).toLocaleString('et');

        };

        if (active.node() === this) return reset();
        active.classed("active", false);
        active = d3.select(this).classed("active", true);

        var bounds = path.bounds(d),
            dx = bounds[1][0] - bounds[0][0],
            dy = bounds[1][1] - bounds[0][1],
            x = (bounds[0][0] + bounds[1][0]) / 2,
            y = (bounds[0][1] + bounds[1][1]) / 2,
            scale = .9 / Math.max(dx / width, dy / height),
            translate = [width / 2 - scale * x, height / 2 - scale * y];

        g.transition()
            .duration(750)
            .style("stroke-width", 1.5 / scale + "px")
            .attr("transform", "translate(" + translate + ")scale(" + scale + ")");
    }

    function reset() {
        active.classed("active", false);
        active = d3.select(null);

        g.transition()
            .duration(500)
            .style("stroke-width", "1.5px")
            .attr("transform", "");

        // Reset data values to country level
        // TODO: Don't hard-code any values here.
        vue_app.current_place_name = 'Eesti';
        vue_app.current_place_confirmed = parseInt('225').toLocaleString('et');
    }
}


function drawMunicipalities() {
    // Colour
    var population_domain = [0, 1000, 5000, 10000, 20000, 50000, 100000, 500000];
    var population_colour = d3.scaleThreshold()
        .domain(population_domain)
        .range(d3.schemeBlues[9]);

    // Population data
    var prevalence_data = d3.map();

    var svg = d3.select("svg#map_prevalence");

    svg.append("rect")
        .attr("width", width)
        .attr("height", height)
        .on("click", clicked);

    var g = svg.append("g");
    // Load TopoJSON maps and data asynchronously.
    d3.queue()
        .defer(d3.json, "/data/topojson/municipalities.json")
        .defer(d3.csv, "/data/population_by_municipality.csv", function (d) {
            if (isNaN(d['pop_2018'])) {
                prevalence_data.set(d.id, 0);
            } else {
                prevalence_data.set(d.id, +d['pop_2018']);

            }
        })
        .await(ready);

    // Define legend settings
    var legendText = ["0", "1", "5", "10", "25", "50", "100", "250"];
    var legendColors = ["#9ecae1", "#63afd7", "#4ea2d9", "#4292c6", "#2171b5", "#08519c", "#1f4884", "#08306b"];

    // Callback function
    function ready(error, data) {
        if (error) throw error;

        // Debug
        console.log(data);

        // Load population data
        var municipalities = topojson.feature(data, {
            type: "GeometryCollection",
            //geometries: data.objects.maakond.geometries  // counties
            geometries: data.objects.omavalitsus.geometries // municipalities
            // geometries: data.objects.asustusyksus.geometries // settlements
        });

        // Draw the map
        g.append("g")
            .attr("id", "municipalities")
            .selectAll("path")
            .data(municipalities.features)
            .enter()
            .append("path")
            .attr("d", path)
            .attr("fill", function(d) {
                return population_colour(d.population = prevalence_data.get(d.properties.OKOOD));
            })
            .on("click", clicked);

        g.append("path")
            .datum(topojson.mesh(data, data.objects.maakond, function(a, b) { return a !== b; }))
            .attr("id", "municipality_borders")
            .attr("d", path);

        // var legend = svg.append("g")
        var legend = d3.select("svg#legend")
            .attr("id", "legend");

        var legenditem = legend.selectAll(".legenditem")
            .data(d3.range(8))
            .enter()
            .append("g")
            .attr("class", "legenditem")
            .attr("transform", function(d, i) { return "translate(" + i * 31 + ",0)"; });

        legenditem.append("rect")
            .attr("x", width - 550)
            .attr("y", 30)
            .attr("width", 30)
            .attr("height", 6)
            .attr("class", "rect")
            .style("fill", function(d, i) { return legendColors[i]; });

        legenditem.append("text")
            .attr("x", width - 550)
            .attr("y", 20)
            .style("text-anchor", "middle")
            .text(function(d, i) { return legendText[i]; });
    }

    function clicked(d) {
        // Debug
        console.log("Map was clicked.");
        if (typeof d !== 'undefined') {
            console.log(d.properties.MNIMI);
            vue_app.current_place_name = d.properties.ONIMI;
            vue_app.current_place_confirmed = parseInt(d.population,10).toLocaleString('et');
        };

        if (active.node() === this) return reset();
        active.classed("active", false);
        active = d3.select(this).classed("active", true);

        var bounds = path.bounds(d),
            dx = bounds[1][0] - bounds[0][0],
            dy = bounds[1][1] - bounds[0][1],
            x = (bounds[0][0] + bounds[1][0]) / 2,
            y = (bounds[0][1] + bounds[1][1]) / 2,
            scale = .9 / Math.max(dx / width, dy / height),
            translate = [width / 2 - scale * x, height / 2 - scale * y];

        g.transition()
            .duration(750)
            .style("stroke-width", 1.5 / scale + "px")
            .attr("transform", "translate(" + translate + ")scale(" + scale + ")");
    }

    function reset() {
        active.classed("active", false);
        active = d3.select(null);

        g.transition()
            .duration(500)
            .style("stroke-width", "1.5px")
            .attr("transform", "");

        // Reset data values to country level
        // TODO: Don't hard-code any values here.
        vue_app.current_place_name = 'Eesti';
        vue_app.current_place_confirmed = parseInt('225').toLocaleString();
    }
}


drawCounties();
