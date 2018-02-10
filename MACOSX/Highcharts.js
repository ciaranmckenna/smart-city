//Highcharts  initialisation  defaults for names adnd axis
Highcharts.setOptions({
  global: {
    useUTC: false
  }
});

var pm10Chart = Highcharts.chart('container1', {
  chart: {
    zoomType: 'x'
  },
  title: {
    text: 'Particulate Matter (PM10)'
  },
  xAxis: {
    type: 'datetime'
  },
  yAxis: {
    title: {
      text: 'µg/m3'
    }

  },
  legend: {
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'middle'
  },

  //takes an array of arrays
  series: []
});

var pm25Chart = Highcharts.chart('container2', {
  chart: {
    zoomType: 'x'
  },
  title: {
    text: 'Particulate Matter (PM2.5)'
  },
  xAxis: {
    type: 'datetime'
  },
  yAxis: {
    title: {
      text: 'µg/m3'
    }
  },
  legend: {
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'middle'
  },
  //takes an array of arrays
  series: []
});