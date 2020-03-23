// Updated on Navbar
const updatedOn = "23/03/2020, 18:30";

// Statsbar
const confirmedCasesNumber = "352";
const activeCasesNumber = "348";
const hospitalisedNumber = "17";
const deceasedNumber = "0";
const recoveredNumber = "4";
const testsAdministeredNumber = "3724";

// Map components
const dataInfectionsByCounty = [
  ["Harjumaa", 128],
  ["Hiiumaa", 2],
  ["Ida-Virumaa", 6],
  ["Jõgevamaa", 1],
  ["Järvamaa", 1],
  ["Läänemaa", 2],
  ["Lääne-Virumaa", 1],
  ["Põlvamaa", 3],
  ["Pärnumaa", 22],
  ["Raplamaa", 2],
  ["Saaremaa", 110],
  ["Tartumaa", 22],
  ["Valgamaa", 1],
  ["Viljandimaa", 2],
  ["Võrumaa", 38]
];

const dataInfectionsByCounty10000 = [
  ["Harjumaa", 2.14], // Harjumaa
  ["Hiiumaa", 2.13], // Hiiumaa
  ["Ida-Virumaa", 0.44], // Ida-Virumaa
  ["Jõgevamaa", 0.35], // Jõgevamaa
  ["Järvamaa", 0.33], // Järvamaa
  ["Läänemaa", 0.98], // Läänemaa
  ["Lääne-Virumaa", 0.17], // Lääne-Virumaa
  ["Põlvamaa", 1.2], // Põlvamaa
  ["Pärnumaa", 2.56], // Pärnumaa
  ["Raplamaa", 0.6], // Raplamaa
  ["Saaremaa", 33.22], // Saaremaa
  ["Tartumaa", 1.44], // Tartumaa
  ["Valgamaa", 0.35], // Valgamaa
  ["Viljandimaa", 0.43], // Viljandimaa
  ["Võrumaa", 10.62] // Võrumaa
];

// Positive tests per 10k chart
const dataTestsPopRatio = [
  2.14, // Harjumaa
  2.13, // Hiiumaa
  0.44, // Ida-Virumaa
  0.35, // Jõgevamaa
  0.33, // Järvamaa
  0.17, // Lääne-Virumaa
  0.98, // Läänemaa
  1.2, // Põlvamaa
  2.56, // Pärnumaa
  0.6, // Raplamaa
  33.22, // Saaremaa
  1.44, // Tartumaa
  0.35, // Valgamaa
  0.43, // Viljandimaa
  10.62 // Võrumaa
];

// Confirmed cases by counties chart
const dataConfirmedCasesByCounties = [
  128, // Harjumaa
  2, // Hiiumaa
  6, // Ida-Virumaa
  1, // Jõgevamaa
  1, // Järvamaa
  1, // Lääne-Virumaa
  2, // Läänemaa
  3, // Põlvamaa
  22, // Pärnumaa
  2, // Raplamaa
  110, // Saaremaa
  22, // Tartumaa
  1, // Valgamaa
  2, // Viljandimaa
  38, // Võrumaa
  11 // Insufficient data
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
    "2020-03-23"
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
    352
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
    4
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
    348
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
    "2020-03-23"
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
    26
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
    "2020-03-23"
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
    3724
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
    "2020-03-23"
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
    495
  ]
};

// Positive tests by age chart
const dataPositiveTestsByAgeChart = {
  // 0 - 4, 5 - 9, 10 - 14, 15 - 19, 20 - 24, 25 - 29, 30 - 34, 35 - 39, 40 - 44, 45 - 49, 50 - 54, 55 - 59, 60 - 64, 65+, unknown
  male: [1, 1, 4, 1, 9, 5, 16, 19, 19, 22, 27, 14, 12, 12, 0],
  female: [1, 0, 5, 7, 2, 10, 19, 25, 20, 27, 19, 18, 11, 25, 0],
  unknown: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
};
// Positive and negative tests by county chart
const dataPositiveNegativeChart = {
  negative: [
    173,
    1785,
    20,
    65,
    26,
    30,
    54,
    23,
    34,
    214,
    72,
    406,
    230,
    30,
    59,
    151
  ],
  positive: [11, 128, 2, 6, 1, 1, 1, 2, 3, 22, 2, 110, 22, 1, 2, 38]
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
  dataPositiveNegativeChart
};
