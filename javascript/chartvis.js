

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

/**
 * Modebar buttons. Interactivity options to be removed.
 * -'2D', zoom2d, pan2d, select2d, lasso2d, zoomIn2d, zoomOut2d, autoScale2d, resetScale2d
 *   -'Geo', zoomInGeo, zoomOutGeo, resetGeo, hoverClosestGeo
 *   -'Other', hoverClosestGl2d, hoverClosestPie, toggleHover, resetViews, toImage, sendDataToCloud, toggleSpikelines, resetViewMapbox
 */
const plotConfig = {
    modeBarButtonsToRemove: ['lasso2d', "sendDataToCloud", "toggleSpikelines"],
    displaylogo: false
}


// Change margins of plots

/**
 * Region margins
 */
const marginBarChart = {
    l: 160,
    r: 0,
    b: 50,
    t: 0,
    pad: 10
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
                '2020-03-12','2020-03-13', '2020-03-14'
            ];
/**
 * Total cumulative counts (running sum)
 */
const cumulative_confirmed_cases = [0,1,1,1,1,1,2,2,5,10,10,10,10,13,17,41,109,115];
const cumulative_recovered_cases = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1];
const cumulative_active_cases = [0,1,1,1,1,1,2,2,5,10,10,10,10,13,17,41,109,114];
const cumulative_death_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];

/**
 * Daily counts
 */
const daily_confirmed_cases = [0,1,0,0,0,0,1,0,3,5,0,0,0,3,4,24,68,6];
const daily_recovered_cases = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1];
const daily_death = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];

/**
 * Region confirmed cases
 */

const sorted_region_data = [
    ["Jõhvi", 0],
    ["Virumaa", 3],
    ["Tartu", 6],
    ["Võru", 9],
    ["Pärnu", 12],
    ["Saaremaa", 31],
    ["Tallinn/Harjumaa", 54],
]

/**
 * Plots the progression as a line chart.
 */
function progressionChart() {
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
        
        xaxis: {
            tickfont: {
                size: 14,
                color: tickFontColor
            },
            gridcolor: gridColor,
            ticks: 'outside',
            zeroline: true,
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
            x: 0.0,
            y: 1.0,
            bgcolor: 'rgba(255, 255, 255, 0)',
            bordercolor: 'rgba(255, 255, 255, 0)',
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
        name: 'Hukkumine',
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
          x: 0.0,
          y: 1.0,
          bgcolor: 'rgba(255, 255, 255, 0)',
          bordercolor: 'rgba(255, 255, 255, 0)',
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
 * Plot for municipalities
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
        marker: {
            color: blue,
            opacity: 0.9
        }
      }];

    var layout = {
        xaxis: {
            title: 'Juhtumite arv',
            gridcolor: gridColor,
            tickfont: {
                color: tickFontColor
            }
        },
        yaxis: {
            tickfont: {
                color: tickFontColor,
                size: 14
            }
        },
        margin: marginBarChart
    };
      
    Plotly.newPlot('region_graph', data, layout, plotConfig);
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