// Updated on Navbar
const updatedOn = "24/03/2020, 18:30";

// Statsbar
const confirmedCasesNumber = "369";
const activeCasesNumber = "362";
const hospitalisedNumber = "17";
const deceasedNumber = "0";
const recoveredNumber = "7";
const testsAdministeredNumber = "4041";

// Map components
const dataInfectionsByCounty = [
  ["Harjumaa", 133],
  ["Hiiumaa", 2],
  ["Ida-Virumaa", 6],
  ["Jõgevamaa", 1],
  ["Järvamaa", 1],
  ["Läänemaa", 2],
  ["Lääne-Virumaa", 1],
  ["Põlvamaa", 3],
  ["Pärnumaa", 22],
  ["Raplamaa", 2],
  ["Saaremaa", 114],
  ["Tartumaa", 23],
  ["Valgamaa", 1],
  ["Viljandimaa", 3],
  ["Võrumaa", 43]
];

const dataInfectionsByCounty10000 = [
  ["Harjumaa", 2.22], // Harjumaa
  ["Hiiumaa", 2.13], // Hiiumaa
  ["Ida-Virumaa", 0.44], // Ida-Virumaa
  ["Jõgevamaa", 0.35], // Jõgevamaa
  ["Järvamaa", 0.33], // Järvamaa
  ["Läänemaa", 0.98], // Läänemaa
  ["Lääne-Virumaa", 0.17], // Lääne-Virumaa
  ["Põlvamaa", 1.2], // Põlvamaa
  ["Pärnumaa", 2.56], // Pärnumaa
  ["Raplamaa", 0.6], // Raplamaa
  ["Saaremaa", 34.43], // Saaremaa
  ["Tartumaa", 1.50], // Tartumaa
  ["Valgamaa", 0.35], // Valgamaa
  ["Viljandimaa", 0.65], // Viljandimaa
  ["Võrumaa", 12.02] // Võrumaa
];

const countyByDay = {
  harjumaa: [73,	87,	101,	104,	108,	114,	123,	128,133],
  hiuumaa: [1,	1,	1,	1,	2,	2,	2,	2,2],
  idavirumaa: [4,	5,	5,	5,	6,	6,	6,	6,6],
  jogevamaa: [1,	1,	1,	1,	1,	1,	1,	1,1],
  jarvemaa: [1,	1,	1,	1,	1,	1,	1,	1,1],
  laanevirumaa: [0,	0,	1,	1,	1,	1,	1,	1,1],
  laanemaa: [0,	0,	0,	0,	2,	2,	2,	2,2],
  polvamaa: [3,	3,	3,3,	3,	3,	3,	3,3],
  parnumaa: [15,	19,	21,	22,	22,	22,	22,	22,22],
  raplamaa: [2,	2,	2,	2,	2,	2,	2,	2,2],
  saaremaa: [57,	57,	70,	71,	77,	92,	94,	110,114],
  tartumaa: [12,	12,	13,	14,	15,	17,	21,	22,23],
  valgamaa: [1,	1,	1,	1,	1,	1,	1,	1,1],
  viljandimaa: [2,	2,	2,	2, 2,	2,	2,	2,3],
  vorumaa: [25,	26,	26,	29,	30,	30,	34,	38,43],
  dates: ["2020-03-16",
    "2020-03-17",
    "2020-03-18",
    "2020-03-19",
    "2020-03-20",
    "2020-03-21",
    "2020-03-22",
    "2020-03-23",
  "2020-03-24"]

};

// Positive tests per 10k chart
const dataTestsPopRatio = [
  2.22, // Harjumaa
  2.13, // Hiiumaa
  0.44, // Ida-Virumaa
  0.35, // Jõgevamaa
  0.33, // Järvamaa
  0.98, // Läänemaa
  0.17, // Lääne-Virumaa
  1.2, // Põlvamaa
  2.56, // Pärnumaa
  0.6, // Raplamaa
  34.43, // Saaremaa
  1.50, // Tartumaa
  0.35, // Valgamaa
  0.65, // Viljandimaa
  12.02 // Võrumaa
];

// Confirmed cases by counties chart
const dataConfirmedCasesByCounties = [
  133, // Harjumaa
  2, // Hiiumaa
  6, // Ida-Virumaa
  1, // Jõgevamaa
  1, // Järvamaa,
  2, // Läänemaa
  1, // Lääne-Virumaa
  3, // Põlvamaa
  22, // Pärnumaa
  2, // Raplamaa
  114, // Saaremaa
  23, // Tartumaa
  1, // Valgamaa
  3, // Viljandimaa
  43, // Võrumaa
  12 // Insufficient data
];

// Cumulative cases chart
const dataCumulativeCasesChart = {
  date: [
    "2020-02-26",
    "2020-02-27",
    "2020-02-28",
    "2020-02-29",
    "2020-03-01",
    "2020-03-02",
    "2020-03-03",
    "2020-03-04",
    "2020-03-05",
    "2020-03-06",
    "2020-03-07",
    "2020-03-08",
    "2020-03-09",
    "2020-03-10",
    "2020-03-11",
    "2020-03-12",
    "2020-03-13",
    "2020-03-14",
    "2020-03-15",
    "2020-03-16",
    "2020-03-17",
    "2020-03-18",
    "2020-03-19",
    "2020-03-20",
    "2020-03-21",
    "2020-03-22",
    "2020-03-23",
    "2020-03-24"
  ],
  cases: [
    0,
    1,
    1,
    1,
    1,
    1,
    2,
    2,
    5,
    10,
    10,
    10,
    10,
    13,
    17,
    41,
    109,
    135,
    171,
    205,
    225,
    258,
    267,
    283,
    306,
    326,
    352,
    369
  ],
  recovered: [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    1,
    1,
    1,
    1,
    1,
    2,
    2,
    4,
    7,
    7
  ],
  active: [
    0,
    1,
    1,
    1,
    1,
    1,
    2,
    2,
    5,
    10,
    10,
    10,
    10,
    13,
    17,
    41,
    109,
    134,
    170,
    204,
    224,
    257,
    266,
    281,
    304,
    322,
    345,
    362
  ],
  deceased: [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
};

// New cases per day chart
const dataNewCasesPerDayChart = {
  date: [
    "2020-02-26",
    "2020-02-27",
    "2020-02-28",
    "2020-02-29",
    "2020-03-01",
    "2020-03-02",
    "2020-03-03",
    "2020-03-04",
    "2020-03-05",
    "2020-03-06",
    "2020-03-07",
    "2020-03-08",
    "2020-03-09",
    "2020-03-10",
    "2020-03-11",
    "2020-03-12",
    "2020-03-13",
    "2020-03-14",
    "2020-03-15",
    "2020-03-16",
    "2020-03-17",
    "2020-03-18",
    "2020-03-19",
    "2020-03-20",
    "2020-03-21",
    "2020-03-22",
    "2020-03-23",
    "2020-03-24"
  ],
  confirmedCases: [
    0,
    1,
    0,
    0,
    0,
    0,
    1,
    0,
    3,
    5,
    0,
    0,
    0,
    3,
    4,
    24,
    68,
    26,
    36,
    34,
    20,
    33,
    9,
    16,
    23,
    20,
    26,
    17
  ],
  recovered: [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    0,
    0,
    0,
    0,
    1,
    0,
    2,
    3,
    0
  ],
  deceased: [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
};

// Cumulative tests chart
const dataCumulativeTestsChart = {
  date: [
    "2020-02-26",
    "2020-02-27",
    "2020-02-28",
    "2020-02-29",
    "2020-03-01",
    "2020-03-02",
    "2020-03-03",
    "2020-03-04",
    "2020-03-05",
    "2020-03-06",
    "2020-03-07",
    "2020-03-08",
    "2020-03-09",
    "2020-03-10",
    "2020-03-11",
    "2020-03-12",
    "2020-03-13",
    "2020-03-14",
    "2020-03-15",
    "2020-03-16",
    "2020-03-17",
    "2020-03-18",
    "2020-03-19",
    "2020-03-20",
    "2020-03-21",
    "2020-03-22",
    "2020-03-23",
    "2020-03-24"
  ],
  testsAdministered: [
    6,
    17,
    29,
    38,
    53,
    74,
    100,
    143,
    184,
    242,
    293,
    311,
    350,
    419,
    464,
    584,
    843,
    971,
    1133,
    1387,
    1625,
    2020,
    2259,
    2504,
    2812,
    3229,
    3724,
    4041
  ]
};

// Tests per day chart
const dataTestsPerDayChart = {
  date: [
    "2020-02-26",
    "2020-02-27",
    "2020-02-28",
    "2020-02-29",
    "2020-03-01",
    "2020-03-02",
    "2020-03-03",
    "2020-03-04",
    "2020-03-05",
    "2020-03-06",
    "2020-03-07",
    "2020-03-08",
    "2020-03-09",
    "2020-03-10",
    "2020-03-11",
    "2020-03-12",
    "2020-03-13",
    "2020-03-14",
    "2020-03-15",
    "2020-03-16",
    "2020-03-17",
    "2020-03-18",
    "2020-03-19",
    "2020-03-20",
    "2020-03-21",
    "2020-03-22",
    "2020-03-23",
    "2020-03-24"
  ],
  testsPerDay: [
    6,
    11,
    12,
    9,
    15,
    21,
    26,
    43,
    41,
    58,
    51,
    18,
    39,
    69,
    45,
    120,
    259,
    128,
    162,
    254,
    238,
    395,
    239,
    245,
    308,
    417,
    495,
    317
  ]
};

// Positive tests by age chart
const dataPositiveTestsByAgeChart = {
  // 0 - 4, 5 - 9, 10 - 14, 15 - 19, 20 - 24, 25 - 29, 30 - 34, 35 - 39, 40 - 44, 45 - 49, 50 - 54, 55 - 59, 60 - 64, 65+, unknown
  malePositive: [1, 1, 4, 1, 9, 6, 17, 19, 20, 22, 28, 17, 12, 13, 0],
  maleNegative: [58, 73, 61, 56, 84, 102, 158, 158, 134, 158, 108, 79, 75, 155, 0],


  femalePositive: [1, 0, 5, 7, 5, 10, 19, 25, 20, 27, 20, 20, 11, 27, 0],
  femaleNegative: [53, 39, 76, 70, 90, 211, 250, 254, 233, 213, 165, 131, 110, 251, 0],


  unknownPositive: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
  unknownNegative: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 59]

};
// Positive and negative tests by county chart
const dataPositiveNegativeChart = {
  negative: [
    183,
    1958,
    23,
    68,
    29,
    35,
    30,
    59,
    36,
    224,
    77,
    423,
    273,
    35,
    66,
    156
  ],
  positive: [12, 133, 2, 6, 1, 1, 2, 1, 3, 22, 2, 114, 23, 1, 3, 43]
};




module.exports = {
  updatedOn,
  confirmedCasesNumber,
  activeCasesNumber,
  hospitalisedNumber,
  deceasedNumber,
  recoveredNumber,
  testsAdministeredNumber,
  dataInfectionsByCounty,
  dataInfectionsByCounty10000,
  dataTestsPopRatio,
  dataConfirmedCasesByCounties,
  dataCumulativeCasesChart,
  dataNewCasesPerDayChart,
  dataCumulativeTestsChart,
  dataTestsPerDayChart,
  dataPositiveTestsByAgeChart,
  dataPositiveNegativeChart,
  countyByDay

};
