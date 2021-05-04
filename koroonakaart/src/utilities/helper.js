export function positiveSign(number) {
  if (number > 0) {
    return "+" + number;
  } else {
    return number.toString();
  }
}

export function capitalise(str) {
  // Capitalise the first letter of a string
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function formatDate(date, locale, dateOptions) {
  if (locale === "en") {
    // Will produce European-style dates when using English
    locale = "en-GB";
  }
  return new Date(date).toLocaleString(locale, dateOptions);
}
