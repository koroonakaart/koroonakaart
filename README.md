# Koroonakaart

Koroonakaart is a project which aims to give accurate and up-to-date information about the Covid-19 epidemic in Estonia.

The project is currently managed by Open Knowledge Estonia. GitHub repository: [https://github.com/okestonia/koroonakaart](https://github.com/okestonia/koroonakaart). The live version is available at [koroonakaart.ee](https://koroonakaart.ee/). The data is updated every day around 11:00 Estonian time, depending on the TEHIK data update. The app is published in three language versions: Estonian, English, and Russian.

For more information please contact:

Maarja-Leena Saar (board member of Open Knowledge Estonia) ⁠— maarjaleena@okee.ee

## Data

All data used by our application can be accessed directly at the following link: https://www.koroonakaart.ee/data.json

## Project setup

### Install prerequisites

Install `poetry` to manage Python dependencies: [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)

### Get/update data from TEHIK API

After cloning the repository, you will need to download the latest Estonian COVID-19 data from TEHIK in order for the app to compile.

```bash
cd TEHIK_Open_Data_Loading_Scripts/
poetry install
poetry run python update_data.py
```

Note: At present, the update process won't work if carried out between midnight and the time that TEHIK updates their data, which is typically sometime between 11am and noon Estonian time. We realise this isn't ideal and are working to improve the process.

### Install front-end dependencies

To Customize Vue.js configuration see [Configuration Reference](https://cli.vuejs.org/config/).

```bash
cd koroonakaart/
npm install
```

### Compiles and hot-reloads for development

```bash
npm run serve
```

### Compiles and minifies for production

```bash
npm run build
```

### Lints and fixes files

```bash
npm run lint
```

# How to contribute?

If you have a suggestion about something that could be improved or wish to help with the technical development, please take a look here: https://github.com/okestonia/koroonakaart/issues

All suggestions and ideas are welcome. Please feel free to fork the project, raise new issues, or make pull requests.

The project is primarily voluntary and has received no funding other than from members of the community. Open Knowledge Estonia [https://www.facebook.com/okestonia/](https://www.facebook.com/okestonia/) has opened a separate bank account to receive support for infrastructure and core maintance:

MTÜ Open Knowledge Estonia EE607700771004696794

We will publish the amount of all support received and keep costs transparent.

# History

## How the team formed at [Hack the Crisis](https://www.facebook.com/events/204692110602347/)

The app was originally built in around 24 hours as part of the Hack the Crisis hackathon put on by Garage48 in Estonia. It was developed by Harry Sild (@Kypsis), Chris Thompson (@neuroactive), Joonas Puura (@PuuraJ), and Keegan McBride (@Keeganmcbride). Hanna Maria Mägi came up with the initial design. Maarja Leena Saar and Sven Illing have also contributed.

# License and data information

This repository is maintained as an open source project and released under an [MIT license](LICENSE).

⚠️ The Highcharts component of this project is licensed under a more restrictive license: [CC-BY-NC](https://creativecommons.org/licenses/by-nc/4.0/), which prevents you from using that component for commercial purposes. Before using the Highcharts dependency, please ensure that your use case is compliant with this licence.

The regional and settlement data is from Maa-amet version 20200601 and demographic data is provided by Statistikaamet.

The COVID-19 related data has been optained from TEHIK via https://www.terviseamet.ee/et/koroonaviirus/avaandmed and is available under [CC0](LICENSE-data).
