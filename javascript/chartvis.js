

/**

Div names for now:
<div id="case_graph" style="width:1200px;height:600px;"></div>
<div id="pie_graph" style="width:1200px;height:600px;"></div>
<div id="cases_day_graph" style="width:1200px;height:600px;"></div>
<div id="region_graph" style="width:1200px; height:600px"></div>
 */


/**
 * Colors for charts
 */
const orange = "#FF7F0E";   // Active
const blue = "#1F77B4";     // Region charts color
const red = "#D62728";      // Confirmed
const green = "#2CA02C";    // Recovered
const grey = "#7F7F7F";     // Dead
const gridColor =  "#E6E6E6"; // Color of grid lines
const tickFontColor = "#444";    // Tick font color

const legendFontColor = "#444";
const legendFontSize = 14;

const tickDateFormat = '%d. %b <br>%Y';



/**
 * Plot configuration
 */
/**
 * Modebar buttons. Interactivity options to be removed.
 * -'2D', zoom2d, pan2d, select2d, lasso2d, zoomIn2d, zoomOut2d, autoScale2d, resetScale2d
 *   -'Geo', zoomInGeo, zoomOutGeo, resetGeo, hoverClosestGeo
 *   -'Other', hoverClosestGl2d, hoverClosestPie, toggleHover, resetViews, toImage, sendDataToCloud, toggleSpikelines, resetViewMapbox
 */

/**
 * Localization: EN, RU, ET
 */
const currentLocale = "et" // ru, or undefined? if not using


 const plotConfig = {
    modeBarButtonsToRemove: ['lasso2d', "sendDataToCloud",
            "toggleSpikelines", "zoomInGeo", "zoomOutGeo", "resetGeo", "select2d",
            "hoverClosestPie", "zoom2d", "zoomIn2d", "zoomOut2d", "hoverClosestGeo", "hoverClosestGl2d",
            "zoom2d", "pan2d", "toggleHover", "autoScale2d", "resetViewMapbox", "resetAxes", "hoverClosestCartesian",
            "hoverCompareCartesian"
        ],
    displaylogo: false,
    locale: currentLocale,
    responsive: true
}

const plotConfigRegionChart = {
    modeBarButtonsToRemove: ['lasso2d', "sendDataToCloud",
            "toggleSpikelines", "zoomInGeo", "zoomOutGeo", "resetGeo", "select2d",
            "hoverClosestPie", "zoom2d", "zoomIn2d", "zoomOut2d", "hoverClosestGeo", "hoverClosestGl2d",
            "zoom2d", "pan2d", "toggleHover", "autoScale2d", "resetViewMapbox", "resetAxes", "hoverClosestCartesian",
            "hoverCompareCartesian"
        ],
    displaylogo: false,
    locale: currentLocale

}



// Change margins of plots

/**
 * Region margins
 */
const marginBarChart = {
    l: 125,
    r: 0,
    b: 50,
    t: 0,
    pad: 5
}


/**
 * Progression margins
 */
const marginLineChart = {
    l: 60,
    r: 0,
    b: 60,
    t: 10,
    pad: 0

}
/**
 * Daily cases margins
 */
const marginDailyCases = {
    l: 60,
    r: 0,
    b: 60,
    t: 10,
    pad: 0
}


/**
 * Smoothing factor for curves. TODO: Doesn't seem to work at this moment?
 */

const smoothingConst = 1.3;

/**
 * DATA SETUP
 */

/**
 * Dates for plots
 */
const x_dates = ['2020-02-26','2020-02-27', '2020-02-28', '2020-02-29',
                '2020-03-01', '2020-03-02', '2020-03-03',
                '2020-03-04','2020-03-05', '2020-03-06', '2020-03-07',
                '2020-03-08','2020-03-09', '2020-03-10', '2020-03-11',
                '2020-03-12','2020-03-13', '2020-03-14', '2020-03-15', '2020-03-16'
            ];
/**
 * Total cumulative counts (running sum)
 */
const cumulative_confirmed_cases = [0,1,1,1,1,1,2,2,5,10,10,10,10,13,17,41,109,135,171,205];
const cumulative_recovered_cases = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1];
const cumulative_active_cases = [0,1,1,1,1,1,2,2,5,10,10,10,10,13,17,41,109,134,170,204];
const cumulative_death_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];

/**
 * Daily counts
 */
const daily_confirmed_cases = [0,1,0,0,0,0,1,0,3,5,0,0,0,3,4,24,68,26,36,34];
const daily_recovered_cases = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0];
const daily_death = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];

/**
 * tests done
 */
const cumulative_tests_done = [6,17,29,38,53,74,100,143,184,242,293,311,350,419,464,584,843,971,1133,1387]
const daily_tests_done = [6,11, 12, 9, 15, 21, 26, 43, 41, 58, 51, 18, 39, 69, 45, 120, 259, 128, 162, 254]



/**
 * Region confirmed cases
 */

const sorted_region_data = [
  ["Info puudulik", 4],
  ["Elukoht teadmata", 4],
    ["Lääne-Virumaa", 0],
    ["Läänemaa", 0],
    ["Valgamaa", 1],
    ["Jõgevamaa", 1],
    ["Järvamaa", 1],
    ["Hiiumaa", 1],
    ["Viljandimaa", 2],
    ["Raplamaa", 2],
    ["Põlvamaa", 3],
    ["Ida-Virumaa", 4],
    ["Tartumaa", 12],
    ["Pärnumaa", 15],
    ["Võrumaa", 25],
    ["Saaremaa", 57],
    ["Harjumaa", 73],
]


/**
 * Plots tests done line chart.
 */
function testsDoneCumulativeChart() {
    var cumulative_tests = {
        x: x_dates,
        y: cumulative_tests_done,
        type: "scatter",
        mode: 'lines',
        //name: 'Teste tehtud',
        marker: {
            color: blue,
            line: {
                color: blue,
                width: 1,
                shape: 'spline',
                smoothing: smoothingConst
            },
        }
    };

    var data = [ cumulative_tests ];

    var layout = {

        xaxis: {
            tickfont: {
                size: 14,
                color: tickFontColor
            },
            gridcolor: gridColor,
            ticks: 'outside',
            zeroline: true,
            tickformat: tickDateFormat,

            },
        yaxis: {
            title: 'Testide arv',
            titlefont: {
                size: 16,
                color: tickFontColor
            },
            tickfont: {
                size: 14,
                color: tickFontColor
            },
            showline: false,
            gridcolor:gridColor,
            rangemode: "tozero",
        },
        margin: marginLineChart
    };

    Plotly.newPlot('tests_graph', data, layout, plotConfig);

};


function testsDoneDailyChart() {

    var daily_tests = {
        x: x_dates,
        y: daily_tests_done,
        type: "bar",
        //mode: 'lines',
        //name: 'Teste tehtud',
        marker: {
            color: blue
        }
    };
    var data = [ daily_tests ];

    var layout = {

        xaxis: {
            tickfont: {
                size: 14,
                color: tickFontColor
            },
            gridcolor: gridColor,
            ticks: 'outside',
            zeroline: true,
            tickformat: tickDateFormat,

            },
        yaxis: {
            title: 'Testide arv',
            titlefont: {
                size: 16,
                color: tickFontColor
            },
            tickfont: {
                size: 14,
                color: tickFontColor
            },
            showline: false,
            gridcolor:gridColor,
            rangemode: "tozero",
        },
        margin: marginLineChart
    };

    Plotly.newPlot('daily_tests_graph', data, layout, plotConfig);
}

/**
 * Plots the progression as a line chart.
 */
function progressionChart() {


    /**
     * Add buttons for log linear
     */
    const updatemenus=[
        {
            buttons: [
                {
                    args: [{
                        yaxis: {
                            type: "linear",
                            autorange: true,
                            rangemode: 'nonnegative',
                        }},

                    ],
                    label: 'Lineaarne',
                    method: 'relayout'
                },
                {
                    args: [{
                        yaxis: {
                            type: 'log',
                            rangemode: 'nonnegative',
                            autorange: true,
                        }},
                    ],
                    label:'Logaritmiline',
                    method:'relayout'
                }
            ],
            direction: 'left',
            showactive: true,
            type: 'buttons',
            x: 0.1,
            xanchor: 'left',
            y: 1.1,
            yanchor: 'top'
        }
    ]
        /*
        list([
        dict(active=1,
             buttons=list([
                dict(label='Log Scale',
                     method='update',
                     args=[{'visible': [True, True]},
                           {'title': 'Log scale',
                            'yaxis': {'type': 'log'}}]),
                dict(label='Linear Scale',
                     method='update',
                     args=[{'visible': [True, False]},
                           {'title': 'Linear scale',
                            'yaxis': {'type': 'linear'}}])
                ]),
            )
        ])
        */



    var confirmed = {
        x: x_dates,
        y: cumulative_confirmed_cases,
        type: "scatter",
        mode: 'lines',
        name: 'Kinnitatud haigusjuhud',
        marker: {
        //    color: 'rgb(164, 194, 244)',
        //    size: 12,
            color: red,
            line: {
                color: red,
                width: 1,
                shape: 'spline',
                smoothing: smoothingConst
            }
        }
    };

    var recovered = {
        x: x_dates,
        y: cumulative_recovered_cases,
        type: "scatter",
        mode: 'lines',
        name: 'Tervenenud',
        marker: {
            //    color: 'rgb(164, 194, 244)',
            //    size: 12,
                color: green,
                line: {
                    color: green,
                    width: 1,
                    shape: 'spline',
                    smoothing: smoothingConst
                }
            },
    }

    var active = {
        x: x_dates,
        y: cumulative_active_cases,
        type: "scatter",
        mode: 'lines',
        name: 'Aktiivsed',
        marker: {
                color: orange,
                line: {
                    color: orange,
                    width: 1,
                    shape: 'spline',
                    smoothing: smoothingConst
                }
            },
    };

    var death = {
        x: x_dates,
        y: cumulative_death_counts,
        type: "scatter",
        mode: 'lines',
        name: 'Hukkunud',
        marker: {
                color: grey,
                line: {
                    color: grey,
                    width: 1,
                    shape: 'spline',
                    smoothing: smoothingConst
                }
            },
    };


    var data = [ confirmed, recovered, active, death ];

    var layout = {
        updatemenus: updatemenus,
        xaxis: {
            tickfont: {
                size: 14,
                color: tickFontColor
            },
            gridcolor: gridColor,
            ticks: 'outside',
            zeroline: true,
            tickformat: tickDateFormat,

            },
        yaxis: {
            title: 'Juhtumite arv',
            titlefont: {
                size: 16,
                color: tickFontColor
            },
            tickfont: {
                size: 14,
                color: tickFontColor
            },
            showline: false,
            gridcolor:gridColor,
            rangemode: "tozero",
        },

        legend: {
            x: 0.01,
            y: 0.99,
            bgcolor: '#FFF',
            opacity: 0.7,
            bordercolor: '#000',
            borderwidth: 1,
            font: {
                size: legendFontSize,
                color: legendFontColor,
              },
        },
        margin: marginLineChart
    };

    Plotly.newPlot('case_graph', data, layout, plotConfig);

};


/**
 * Chars for plotting cases per day
 * Based on: https://plot.ly/javascript/bar-charts/
 */
function casesPerDay() {

    var confirmed = {
        x: x_dates,
        y: daily_confirmed_cases,
        name: 'Kinnitatud haigusjuhud',
        marker: {color: red},
        type: 'bar'
      };

      var recovered = {
        x: x_dates,
        y: daily_recovered_cases,
        name: 'Tervenenud',
        marker: {color: green},
        type: 'bar'
      };

      var death = {
        x: x_dates,
        y: daily_death,
        name: 'Hukkunud',
        marker: {color: grey},
        type: 'bar'
      };


      var data = [confirmed, recovered, death];

      var layout = {

        xaxis: {
            tickfont: {
                size: 14,
                color: tickFontColor,
            },
            gridcolor: gridColor,
            ticks: 'outside',
            tickformat: tickDateFormat,
        },

        yaxis: {
          title: 'Juhtumite arv',
          titlefont: {
            size: 16,
            color: tickFontColor
          },
          tickfont: {
            size: 14,
            color: tickFontColor
          },
          gridcolor: gridColor,
        },

        legend: {
            x: 0.01,
            y: 0.99,
            bgcolor: '#FFF',
            opacity: 0.7,
            bordercolor: '#000',
            borderwidth: 1,
            font: {
               size: legendFontSize,
               color: legendFontColor,
            }

        },
        barmode: 'group',
        bargap: 0.15,
        bargroupgap: 0.2,
        margin: marginDailyCases

      };

      Plotly.newPlot('cases_day_graph', data, layout, plotConfig);
}


/**
 * Horizontal bar plot for cases by county
 */
function regionChart(srt_region) {

    // Sort by second key
    //const new_arr = region_confirmed_cases.sort((a,b) => a[1] > b[1]);
    //console.log(new_arr);
    // reextract x and y
    let new_x = [];
    let new_y = [];
    for (let i = 0; i < srt_region.length; i++) {
        new_x.push(srt_region[i][1]);
        new_y.push(srt_region[i][0]);
    }


    var data = [{
        type: 'bar',
        x: new_x,
        y: new_y,
        orientation: 'h',
        text: new_x,
        textposition: 'auto',
        marker: {
            color: blue,
            opacity: 0.9
        },
        hoverinfo: 'none'
      }];

    var layout = {
        xaxis: {
            title: 'Juhtumite arv',
            gridcolor: gridColor,
            tickfont: {
                color: tickFontColor
            },
            fixedrange: true,
        },
        yaxis: {
            tickfont: {
                color: tickFontColor,
                size: 14
            },
            fixedrange: true,
        },
        margin: marginBarChart
    };

    Plotly.newPlot('region_graph', data, layout, plotConfigRegionChart);
}



/**
 * Plots the pie chart of active counts, deaths and recovered.
 */
/*
function pieChart() {
    var data = [{
        values: [115, 1, 0],
        labels: ['Aktiivsed', 'Tervenenud', 'Hukkunud'],
        marker: {
            colors:  [orange, green, grey],
        },
        type: 'pie'
      }];


      var layout = {
      //    title: 'Show Edit in Chart Studio Button'
      };

      Plotly.newPlot('pie_graph', data, layout);
};
*/

progressionChart();
//pieChart();
casesPerDay();
regionChart(sorted_region_data);
testsDoneCumulativeChart();
testsDoneDailyChart();
