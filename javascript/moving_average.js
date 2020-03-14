// https://stackoverflow.com/questions/40057020/calculating-exponential-moving-average-ema-using-javascript

var getEMA = (a,r) => a.reduce((p,n,i) => i ? p.concat(2*n/(r+1) + p[p.length-1]*(r-1)/(r+1)) : p, [a[0]]),
    // data = [15, 18, 12, 14, 16, 11, 6, 18, 15, 16],
    data = [-1, -2, 3, 4, 5],
    range = 3;

console.log(getEMA(data,range));