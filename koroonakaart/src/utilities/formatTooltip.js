import { formatDate, capitalise } from "./helper";
import { formatNumberByLocale } from "./formatNumberByLocale";


export function formatTooltip(context, series, locale, precision, showMarker) {
  // Identify which position in the series and date we are dealing with
  var index = context.chart.hoverPoint.index;
  var hoverpoint = context.chart.hoverPoint;
  var x = context.chart.hoverPoint.x;
  var y = context.chart.hoverPoint.y;
  var category = context.chart.hoverPoint.category;
  var dataGroupingUnitName;
  if (context.chart.hoverPoint.series.currentDataGrouping !== undefined ) {
    dataGroupingUnitName = context.chart.hoverPoint.series.currentDataGrouping.unitName
  }

  // // Debug
  // console.log('context');
  // console.log(context);
  // console.log('series');
  // console.log(series);
  // console.log('hoverpoint');
  // console.log(hoverpoint);
  // console.log('index');
  // console.log(index);
  // console.log('x');
  // console.log(x);
  // console.log('y');
  // console.log(y);
  // console.log('category');
  // console.log(category);
  // console.log('dataGroupingUnitName');
  // console.log(dataGroupingUnitName);

  // Get data for the individual tooltip entries
  var tooltipEntries = [];
  var n_series = series.length;
  // console.log('n_series: ' + n_series);
  for (var i = 0; i < n_series; i++) {
    if (context.chart.series[i].visible && series[i].data[index] !== undefined) {
      tooltipEntries.push({
        name: series[i].name,
        value: formatNumberByLocale(series[i].data[index], locale, precision),
        color: series[i].color
      });
    }
  }

  // Calculate tooltip title
  var tooltipTitle;
  if (isNaN(category)) {
    // Label name
    tooltipTitle = category;
  } else {
    // Localised date
    var dateOptions = {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    };
    tooltipTitle = capitalise(formatDate(x, locale, dateOptions));
  }

  // Compose tooltip
  var tooltip = tooltipTitle + "<br>";
  if (tooltipEntries.length > 0) {
    tooltip += "<table>";
    for (const tooltipEntry of tooltipEntries) {
      tooltip += "<tr>";
      tooltip += "<td>";
      if (showMarker) {
        tooltip += '<span style="color:' + tooltipEntry.color + '">●</span> ';
      }
      tooltip += tooltipEntry.name + "&nbsp;</td>";
      tooltip += '<td style="text-align: right"><b>' + tooltipEntry.value + "</b></td>";
      tooltip += "</tr>";
    }
    tooltip += "</table>";
  }

  return tooltip;
}
