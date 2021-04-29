import { formatDate } from "./helper";
import { formatNumberByLocale } from "./formatNumberByLocale";

export function formatTooltip(context, series, locale, precision, showMarker) {
  // Identify which position in the series and date we are dealing with
  var index = context.chart.hoverPoint.index;
  var x = context.chart.hoverPoint.x;
  var category = context.chart.hoverPoint.category;

  // Debug
  // console.log(context.chart.hoverPoint);

  // Get data for the individual tooltip entries
  var tooltipEntries = [];
  for (const series of series) {
    if (series.data[index] !== undefined) {
      tooltipEntries.push({
        name: series.name,
        value: formatNumberByLocale(series.data[index], locale, precision),
        color: series.color,
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
    tooltipTitle = formatDate(x, locale, dateOptions);
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
