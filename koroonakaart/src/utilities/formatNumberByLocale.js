export function formatNumberByLocale(num, locale) {
  if(!num || !locale) throw new Error('Number or locale is missing')
  const parsedNumber = typeof num === "string" ? parseFloat(num) : num;
  return new Intl.NumberFormat(locale).format(parsedNumber);
}
