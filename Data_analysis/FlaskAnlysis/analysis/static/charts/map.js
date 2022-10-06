(async () => {
    const topology = await fetch(
        'https://code.highcharts.com/mapdata/custom/world.topo.json'
    ).then(response => response.json());


    Highcharts.getJSON('http://127.0.0.1:8080/location', function (data) {

        // Prevent logarithmic errors in color calulcation
        data.forEach(function (p) {
            p.value = (p.value < 1 ? 1 : p.value);
        });

        // Initialize the chart
        Highcharts.mapChart('containermap', {

            chart: {
                map: topology
            },

            title: {
                text: 'Number of tweet shared in each Country'
            },

            legend: {
                title: {
                    text: 'Number of tweet shared in each country',
                    style: {
                        color: ( // theme
                            Highcharts.defaultOptions &&
                            Highcharts.defaultOptions.legend &&
                            Highcharts.defaultOptions.legend.title &&
                            Highcharts.defaultOptions.legend.title.style &&
                            Highcharts.defaultOptions.legend.title.style.color
                        ) || 'black'
                    }
                }
            },

            mapNavigation: {
                enabled: true,
                buttonOptions: {
                    verticalAlign: 'bottom'
                }
            },

            tooltip: {
                backgroundColor: 'none',
                borderWidth: 0,
                shadow: false,
                useHTML: true,
                padding: 0,
                pointFormat: '<span class="f32"><span class="flag {point.properties.hc-key}">' +
                    '</span></span> {point.name}<br>' +
                    '<span style="font-size:30px">{point.value}/count</span>',
                positioner: function () {
                    return { x: 0, y: 250 };
                }
            },

            colorAxis: {
                min: 1,
                max: 10000,
                type: 'logarithmic',
                maxColor:"#026C5F"
            },

            series: [{
                data: data,
                joinBy: ['iso-a3', 'code3'],
                name: 'Crime density',
                states: {
                    hover: {
                        color: '#026C5F'
                    }
                }
            }]
        });
    });

})();


(async () => {

  const topology = await fetch(
      'https://code.highcharts.com/mapdata/custom/world.topo.json'
  ).then(response => response.json());

  Highcharts.getJSON('http://127.0.0.1:8080/influncerlocation', function (data) {

      Highcharts.mapChart('containermap1', {
          chart: {
              borderWidth: 1,
              map: topology
          },

          title: {
              text: 'Location of influncer'
          },

     

          accessibility: {
              description: 'We see how China and India by far are the countries with the largest population.'
          },

          legend: {
              enabled: true
          },

          mapNavigation: {
              enabled: true,
             
              buttonOptions: {
                  verticalAlign: 'bottom'
              }
          },

          series: [{
              name: 'Countries',
              color: '#E0E0E0',
              enableMouseTracking: false
          }, {
              type: 'mapbubble',
              name: 'number of influncer in each country',
              joinBy: ['iso-a3', 'code3'],
              data: data,
              minSize: 4,
              maxSize: '12%',
              color: "#108E7F",
              tooltip: {
                  pointFormat: "{point.properties.hc-a2}: {point.z} person's"
              }
          }]
      });
  });

})();