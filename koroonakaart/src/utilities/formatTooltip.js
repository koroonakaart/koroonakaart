import { formatDate, capitalise } from "./helper";
import { formatNumberByLocale } from "./formatNumberByLocale";

export function formatTooltip(context, series, locale, precision, showMarker) {
  // Identify which position in the series and date we are dealing with
  var index = context.chart.hoverPoint.index;
  var x = context.chart.hoverPoint.x;
  var category = context.chart.hoverPoint.category;

  // Get data for the individual tooltip entries
  var tooltipEntries = [];
  var n_series = series.length;
  for (var i = 0; i < n_series; i++) {
    if (
      context.chart.series[i].visible &&
      series[i].data[index] !== undefined
    ) {
      tooltipEntries.push({
        name: series[i].name,
        value: formatNumberByLocale(series[i].data[index], locale, precision),
        color: series[i].color,
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
      tooltip +=
        '<td style="text-align: right"><b>' + tooltipEntry.value + "</b></td>";
      tooltip += "</tr>";
    }
    tooltip += "</table>";
  }

  return tooltip;
}
