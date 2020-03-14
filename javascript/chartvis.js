


/**

Div names for now:
<div id="case_graph" style="width:1200px;height:600px;"></div>
<div id="pie_graph" style="width:1200px;height:600px;"></div>
<div id="cases_day_graph" style="width:1200px;height:600px;"></div>
<div id="region_chart" style="width:1200px; height:600px"></div>
 */


/**
 * Plots the progression as a line chart.
 */
function progressionChart() {

    const x_dates = ['2020-02-26','2020-02-27', '2020-02-28', 
            '2020-02-29','2020-03-01', '2020-03-02', '2020-03-03', 
            '2020-03-04','2020-03-05', '2020-03-06', '2020-03-07',
            '2020-03-08','2020-03-09', '2020-03-10', '2020-03-11',
            '2020-03-12','2020-03-13', '2020-03-14'];

    var confirmed = {
        x: x_dates,
        y: [0,1,1,1,1,1,2,2,5,10,10,10,10,13,17,41,109,115],
        mode: 'lines',
        name: 'Kinnitatud juhud',
        marker: {
        //    color: 'rgb(164, 194, 244)',
        //    size: 12,
            color: 'red',
            line: {
            color: 'red',
            width: 1
            }
        }
    };
    
    var recovered = {
        x: x_dates,
        y: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        mode: 'lines',
        name: 'Taastunud',
        marker: {
            //    color: 'rgb(164, 194, 244)',
            //    size: 12,
                color: 'RGBA(0, 100, 0, 1)',
                line: {
                color: 'orange',
                width: 1
                }
            },
    }

    var active = {
        x: x_dates,
        y: [0,1,1,1,1,1,2,2,5,10,10,10,10,13,17,41,109,114],
        mode: 'lines',
        name: 'Aktiivsed',
        marker: {
            //    color: 'rgb(164, 194, 244)',
            //    size: 12,
                color: 'orange',
                line: {
                color: 'orange',
                width: 1
                }
            },
    };

    var death = {
        x: ['2020-02-26','2020-02-27', '2020-02-28', 
            '2020-02-29','2020-03-01', '2020-03-02', '2020-03-03', 
            '2020-03-04','2020-03-05', '2020-03-06', '2020-03-07',
            '2020-03-08','2020-03-09', '2020-03-10', '2020-03-11',
            '2020-03-12','2020-03-13', '2020-03-14'],
        y: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        mode: 'lines',
        name: 'Hukkunud',
        marker: {
            //    color: 'rgb(164, 194, 244)',
            //    size: 12,
                color: 'RGBA(169, 169, 169, 1)',
                line: {
                color: 'red',
                width: 1
                }
            },
    };

    
    var data = [ confirmed, recovered, active, death ];
    
    var layout = {
        // title:'COVID-19 progressioon'
    };
    
    Plotly.newPlot('case_graph', data, layout);

};



/**
 * Chars for plotting cases per day
 * Based on: https://plot.ly/javascript/bar-charts/
 */
function casesPerDay() {

    const x_dates = ['2020-02-26','2020-02-27', '2020-02-28', 
            '2020-02-29','2020-03-01', '2020-03-02', '2020-03-03', 
            '2020-03-04','2020-03-05', '2020-03-06', '2020-03-07',
            '2020-03-08','2020-03-09', '2020-03-10', '2020-03-11',
            '2020-03-12','2020-03-13', '2020-03-14'];
            
    var confirmed = {
        x: x_dates,
        y: [0,1,0,0,0,0,1,0,3,5,0,0,0,3,4,24,68,6],
        name: 'Kinnitatud haigusjuhtumid',
        marker: {color: 'red'},
        type: 'bar'
      };
      
      var recovered = {
        x: x_dates,
        y: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        name: 'Taastumised',
        marker: {color: 'RGBA(0, 100, 0, 1)'},
        type: 'bar'
      };
      
      var death = {
        x: x_dates,
        y: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        name: 'Hukkumine',
        marker: {color: 'RGBA(169, 169, 169, 1)'},
        type: 'bar'
      };
      
      var data = [confirmed, recovered, death];
      
      var layout = {
        title: 'Juhtumid',
        xaxis: {tickfont: {
            size: 14,
            color: 'rgb(107, 107, 107)'
          }},
        yaxis: {
          title: 'Juhtumite arv',
          titlefont: {
            size: 16,
            color: 'rgb(107, 107, 107)'
          },
          tickfont: {
            size: 14,
            color: 'rgb(107, 107, 107)'
          }
        },
        legend: {
          x: 0,
          y: 1.0,
          bgcolor: 'rgba(255, 255, 255, 0)',
          bordercolor: 'rgba(255, 255, 255, 0)'
        },
        barmode: 'group',
        bargap: 0.15,
        bargroupgap: 0.2
      };
      
      Plotly.newPlot('cases_day_graph', data, layout);
}


/**
 * Plots the pie chart of active counts, deaths and recovered.
 */
function pieChart() {
    var data = [{
        values: [115, 1, 0],
        labels: ['Aktiivsed', 'Tervenenud', 'Hukkunud'],
        type: 'pie'
      }];
      
      var layout = {
      //    title: 'Show Edit in Chart Studio Button'
      };
      
      Plotly.newPlot('pie_graph', data, layout);
};

/**
 * Plot for municipalities
 */
function regionChart() {

    const y = ["Tallinn/Harjumaa", "Tartu", "Võru", "Saaremaa", "Virumaa", "Pärnu", "Jõhvi", "Teadmata"]
    const x = [54,6,9,31,3,12,0]
    
    let new_arr = []
    // Sort array
    for (let i=0; i<x.length; i++) {
        new_arr.push([x[i], y[i]])
    }
    // Sort by first key.
    new_arr = new_arr.sort((a,b) => a[0] > b[0]);

    // reextract x and y
    const new_x = new_arr.map(a => a[0]);
    const new_y = new_arr.map(a => a[1]);
    /// const max_val = max(...x); // Gradient for olor
    
    var data = [{
        type: 'bar',
        x: new_x,
        y: new_y,
        orientation: 'h',
      }];

      var layout = {
        xaxis: {
            title: 'Juhtumite arv'
            }
        };
      
      Plotly.newPlot('region_chart', data, layout);
}



progressionChart();
pieChart();
casesPerDay();
regionChart();