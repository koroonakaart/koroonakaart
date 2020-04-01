export const collateDates = array =>
  array.reduce((accumulator, { ResultTime, n }) => {
    let temp = accumulator.find(o => o.ResultTime === ResultTime);
    if (temp) {
      temp.n += n;
    } else {
      accumulator.push({ ResultTime, n });
    }
    return accumulator;
  }, []);

export const accumulatedTests = array => {
  let tempArray = [];
  let accumulated = 0;

  for (let i = 0; i < array.length; i++) {
    accumulated = accumulated + array[i].n;
    tempArray.push({ ...array[i], n: accumulated });
  }
  return tempArray;
};
