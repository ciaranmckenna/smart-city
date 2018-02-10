#!/usr/bin/env python
# -*- coding: utf-8 -*-

# These two lines ensure the JSON data will print to our webpage.
print ("Content-type: text/html")
print 

import json

# This variable stores the actual data necessary to draw the zones on the map.
geo = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "zone" : "1"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -5.955104827880859,
              54.59578750570867
            ],
            [
              -5.928325653076172,
              54.58300611240568
            ],
            [
              -5.905237197875977,
              54.59727923575245
            ],
            [
              -5.930213928222656,
              54.610801761273855
            ],
            [
              -5.955104827880859,
              54.59578750570867
            ]
          ]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "zone" : "3"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -5.953559875488281,
              54.59524052433466
            ],
            [
              -6.000251770019531,
              54.56549357068548
            ],
            [
              -5.9839439392089835,
              54.557431292707555
            ],
            [
              -5.936565399169922,
              54.58678624168226
            ],
            [
              -5.953559875488281,
              54.59524052433466
            ]
          ]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "zone" : "2"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -5.924034118652344,
              54.651590680027134
            ],
            [
              -5.927467346191406,
              54.609857319005776
            ],
            [
              -5.911674499511719,
              54.60071000748458
            ],
            [
              -5.9058380126953125,
              54.65139205120125
            ],
            [
              -5.924034118652344,
              54.651590680027134
            ]
          ]
        ]
      }
    }
  ]
}

# This ensures the data printed to the webpage is in fact json data.
print (json.dumps(geo))