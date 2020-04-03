# Koroonakaart

Repo now being developed within Open Knowledge Estonia: [https://github.com/okestonia/koroonakaart](https://github.com/okestonia/koroonakaart). Data is updated every day around 12 (depends on TEHIK data update). Live version is available at [koroonakaart.ee](http://koroonakaart.ee/).

Url to load localized version follows the format of **https://koroonakaart.ee/language** (eg https://koroonakaart.ee/en). Valid language identifiers currently are **et** (Estonian), **en** (English) and **ru** (Russian).


This project is co-developed by a team of researchers and open government data activists from Open Knowledge Estonia, Tallinn University of Technology (Keegan McBride, Project Manager, @keeganmcbride), University of Tartu (Joonas Puura, @PuuraJ), and other civic activists (Harry Sild, @Kypsis; Chris Thompson @neuroactive) who took part in the Garage 48 Hack The Crisis Hackathon.

For more information please contact:  

Keegan McBride (PO of koroonakaart.ee) ⁠— keegan.mcbride@taltech.ee

Maarja-Leena Saar (board member of Open Knowledge Estonia) ⁠— maarjaleena@okee.ee 

## To embed any of the charts

You can use the export menu on the charts (hamburger) and copy and paste from the modal or directly link to the chart. Eg *https://www.koroonakaart.ee/en/chart?chart=TestsPopRatioChart&height=700&width=1000* Accepts height and width currently as props through query string.

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```
### Get data from TEHIK API
```
pip3 install -r requirements.txt
python3 main.py
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


# Who we are?
## How team formed @ [Hack the Crisis](https://www.facebook.com/events/204692110602347/) and current maintenance
This is a work in progress and was built in ~24 hours as part of the Hack the Crisis hackathon put on by Garage 48 in Estonia. It is developed by Harry Sild (@Kypsis), Chris Thompson (@neuroactive), Joonas Puura (@PuuraJ), Keegan McBride (@Keeganmcbride). Hanna Maria Mägi came up with the initial design, Maarja Leena Saar and Sven Illing have also contributed. 

Please feel free to fork and/or PR. We hope to keep this up-to-date and improve over time. All suggestions and ideas are welcome. 

# How to contribute?
It is all voluntary work and has no funding.

You have a proposal what to do or you can help to develop a solution? Take a look here > https://github.com/okestonia/koroonakaart/issues

Open Knowledge Estonia [https://www.facebook.com/okestonia/](https://www.facebook.com/okestonia/) opened separate bank account to receive support for infrastructure and core maintance. We will publish all supporters and keep costs transparent.

MTÜ Open Knowledge Estonia EE607700771004696794 

