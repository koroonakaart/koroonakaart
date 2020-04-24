export function positiveSign(number) {
  if (number > 0) {
    return "↑ +" + number;
  } else {
    return "↓ " + number.toString();
  }
}
