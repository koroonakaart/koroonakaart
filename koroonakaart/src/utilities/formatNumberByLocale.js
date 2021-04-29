export function formatNumberByLocale(num, locale, precision = 0) {
  if (num === undefined || locale === undefined) throw new Error('Number or locale is missing.')
  const parsedNumber = Number(typeof num === "string" ? parseFloat(num) : num).toFixed(precision);
  return new Intl.NumberFormat(locale, { minimumFractionDigits: precision }).format(parsedNumber);
}
