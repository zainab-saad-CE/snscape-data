$.getJSON("/hashtagsframework", function (data) {
    reader(data);
  });
  function reader(data) {
    Highcharts.chart("container-word", {
      accessibility: {
        screenReaderSection: {
          beforeChartFormat:
            "<h5>{chartTitle}</h5>" +
            "<div>{chartSubtitle}</div>" +
            "<div>{chartLongdesc}</div>" +
            "<div>{viewTableButton}</div>",
        },
      },
      series: [
        {
          type: "wordcloud",
          data,
          name: "Occurrences",
        },
      ],
      title: {
        text: "Hashtags",
      },
      tooltip: {
        headerFormat:
          '<span style="font-size: 16px"><b>{point.key}</b></span><br>',
      },
    });
  }

  let out = [];

  $.getJSON("/verification", function (data3) {
    for (var i = 0; i < data3.length; i++) {
      out[i] = [data3[i]["verification"], data3[i]["number"]];
    }
    readinginfo(out);
  });
  function readinginfo(out) {
    Highcharts.chart("container-3D", {
      chart: {
        type: "pie",
        options3d: {
          enabled: true,
          alpha: 45,
        },
      },
      title: {
        text: "Verified and unverified users",
      },
      
      plotOptions: {
        pie: {
          innerSize: 100,
          depth: 45,
         
        },
      },
      series: [
        {
          name: "verification",
          data: out,
        },
      ],
    });
  }

  let age = [];
  let count = [];
  $.getJSON("/UserAgePercentage", function (data1) {
    for (var i = 0; i < data1.length; i++) {
      age[i] = data1[i]["age"];
      count[i] = data1[i]["count"];
    }
    reading(age, count);
  });
  function reading(age, count) {
    Highcharts.chart("container-age", {
      title: {
        text: "Number of years since the user joined the Twitter account",
      },
      colors:["#038878"],
      xAxis: {
        categories: age,
      },
      series: [
        {
          type: "column",
          name: "count",
          colorByPoint: false,
          data: count,
          showInLegend: false,
        },
      ],
    });
  }

  let output = [];
  $.getJSON("/topinfluncerhashtags", function (data2) {
    for (var i = 0; i < data2.length; i++) {
      output[i] = [data2[i]["name"], data2[i]["hashtags"], data2[i]["count"]];
    }
    readerinfo(output);
  });
  function readerinfo(output) {
    Highcharts.chart("container-relation", {
      title: {
        text: "This charts is showing  the top-influncer with their top hashtags ",
      },
      accessibility: {
        point: {
          valueDescriptionFormat:
            "{index}. {point.from} to {point.to}, {point.weight}.",
        },
      },
      series: [
        {
          keys: ["from", "to", "weight"],
          data: output,
          type: "sankey",
          name: "Sankey demo series",
        },
      ],
    });
  }

 

  $.getJSON("/topinfluncer", function (getresult) {
    getdata(getresult);
  });
  function getdata(getresult) {
    am5.ready(function () {
      // Create root element
      // https://www.amcharts.com/docs/v5/getting-started/#Root_element
      var root = am5.Root.new("chartdiv");

      // Set themes
      // https://www.amcharts.com/docs/v5/concepts/themes/
      root.setThemes([am5themes_Animated.new(root)]);

      // Create chart
      // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/
      var chart = root.container.children.push(
        am5percent.PieChart.new(root, {
          radius: am5.percent(90),
          innerRadius: am5.percent(50),
          layout: root.horizontalLayout,
        })
      );

      // Create series
      // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Series
      var series = chart.series.push(
        am5percent.PieSeries.new(root, {
          name: "Series",
          valueField: "count",
          categoryField: "name",
        })
      );

      // Set data
      // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Setting_data
      series.data.setAll(getresult);

      // Disabling labels and ticks
      series.labels.template.set("visible", false);
      series.ticks.template.set("visible", false);

      // Adding gradients
      series.slices.template.set("strokeOpacity", 0);
      series.slices.template.set(
        "fillGradient",
        am5.RadialGradient.new(root, {
          stops: [
            {
              brighten: -0.8,
            },
            {
              brighten: -0.8,
            },
            {
              brighten: -0.5,
            },
            {
              brighten: 0,
            },
            {
              brighten: -0.5,
            },
          ],
        })
      );

      // Create legend
      // https://www.amcharts.com/docs/v5/charts/percent-charts/legend-percent-series/
      var legend = chart.children.push(
        am5.Legend.new(root, {
          centerY: am5.percent(50),
          y: am5.percent(50),
          layout: root.verticalLayout,
        })
      );
      // set value labels align to right
      legend.valueLabels.template.setAll({ textAlign: "right" });
      // set width and max width of labels
      legend.labels.template.setAll({
        maxWidth: 140,
        width: 140,
        oversizedBehavior: "wrap",
      });

      legend.data.setAll(series.dataItems);

      // Play initial series animation
      // https://www.amcharts.com/docs/v5/concepts/animations/#Animation_of_series
      series.appear(1000, 100);
    });
  }

  let outdata = [];

  $.getJSON("/toptweet", function (data4) {
    for (var i = 0; i < data4.length; i++) {
      outdata[i] = [data4[i]["name"], data4[i]["sum"]];
    }
    readingdata(outdata);
  });

  function readingdata(outdata) {
    // Set up the chart
    Highcharts.chart("container-funnel", {
      chart: {
        type: "funnel3d",
        options3d: {
          enabled: true,
          alpha: 10,
          depth: 50,
          viewDistance: 50,
        },
      },
      title: {
        text: "Name of influncers how shared the top tweets",
      },
      accessibility: {
        screenReaderSection: {
          beforeChartFormat:
            "<{headingTagName}>{chartTitle}</{headingTagName}><div>{typeDescription}</div><div>{chartSubtitle}</div><div>{chartLongdesc}</div>",
        },
      },
      plotOptions: {
        series: {
          dataLabels: {
            enabled: true,
            format: "<b>{point.name}</b> ",
            allowOverlap: true,
            y: 10,
          },
          neckWidth: "30%",
          neckHeight: "25%",
          width: "80%",
          height: "80%",
        },
      },
      series: [
        {
          name: "Unique users",
          data: outdata,
        },
      ],
    });
  }

  let cnt = [];
  let year = [];

  $.getJSON("/CaseSearch", function (data5) {
    for (var i = 0; i < data5.length; i++) {
      year[i] = data5[i]["year"];
      cnt[i] = data5[i]["count"];
    }
    readingCaseSearch(year, cnt);
  });
  
  function readingCaseSearch(year, cnt) {
    // Set up the chart
    Highcharts.chart("container-year", {
      chart: {
        zoomType: "xy",
      },
      title: {
        text: "Number of shared tweet as time increase",
        align: "left",
      },
      xAxis: [
        {
          categories: year,
          crosshair: true,
        },
      ],
      yAxis: [
        {
          // Primary yAxis
          labels: {
            format: "{value} tweets",
            style: {
              color: Highcharts.getOptions().colors[1],
            },
          },
          title: {
            text: "Tweet count",
            style: {
              color: Highcharts.getOptions().colors[1],
            },
          },
        },
      ],
      tooltip: {
        shared: true,
      },
      legend: {
        align: "left",
        x: 80,
        verticalAlign: "top",
        y: 80,
        floating: true,
        backgroundColor:
          Highcharts.defaultOptions.legend.backgroundColor || // theme
          "rgba(255,255,255,0.25)",
      },
      series: [
        {
          name: "Tweet count",
          type: "spline",
          data: cnt,
          tooltip: {
            valueSuffix: "tweet",
          },
        },
      ],
    });
  }  

  $.getJSON("/sentiment", function (dataget) {
    readsentiment(dataget);

  });  

// Data retrieved from https://netmarketshare.com/
// Radialize the colors
function readsentiment(dataget){
am5.ready(function() {

// Create root element
// https://www.amcharts.com/docs/v5/getting-started/#Root_element
var root = am5.Root.new("chartdiv3");

// Set themes
// https://www.amcharts.com/docs/v5/concepts/themes/
root.setThemes([
  am5themes_Animated.new(root)
]);

// Create chart
// https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/
// start and end angle must be set both for chart and series
var chart = root.container.children.push(am5percent.PieChart.new(root, {
  layout: root.verticalLayout,
  innerRadius: am5.percent(40)
}));

// Create series
// https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Series
// start and end angle must be set both for chart and series
var series0 = chart.series.push(am5percent.PieSeries.new(root, {
  valueField: "count",
  categoryField: "name",
  alignLabels: false
}));

var bgColor = root.interfaceColors.get("background");

series0.ticks.template.setAll({ forceHidden: true });
series0.labels.template.setAll({ forceHidden: true });
series0.slices.template.setAll({
  stroke: bgColor,
  strokeWidth: 2,
  tooltipText:
    "{category}: {value} count"
});
series0.slices.template.states.create("hover", { scale: 0.95 });

var series1 = chart.series.push(am5percent.PieSeries.new(root, {
  valueField: "percentage",
  categoryField: "name",
  alignLabels: true
}));

series1.slices.template.setAll({
  stroke: bgColor,
  strokeWidth: 2,
  tooltipText:
    "{category}: {value} percentage"
});

var data = dataget;

// Set data
// https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Setting_data
series0.data.setAll(dataget);
series1.data.setAll(dataget);

// Play initial series animation
// https://www.amcharts.com/docs/v5/concepts/animations/#Animation_of_series
series0.appear(1000, 100);
series1.appear(1000, 100);

});
}

$.getJSON("/urltopinfluncer", function (dataget1) {
  readurl(dataget1);

});  

// Data retrieved from https://netmarketshare.com/
// Radialize the colors
function readurl(dataget1){
am5.ready(function() {

// Create root element
// https://www.amcharts.com/docs/v5/getting-started/#Root_element
var root = am5.Root.new("chartdiv4");

// Set themes
// https://www.amcharts.com/docs/v5/concepts/themes/
root.setThemes([
am5themes_Animated.new(root)
]);

var data = dataget1;

// Create chart
// https://www.amcharts.com/docs/v5/charts/xy-chart/
var chart = root.container.children.push(
am5xy.XYChart.new(root, {
panX: false,
panY: false,
wheelX: "none",
wheelY: "none",
paddingLeft: 50,
paddingRight: 40
})
);

// Create axes
// https://www.amcharts.com/docs/v5/charts/xy-chart/axes/

var yRenderer = am5xy.AxisRendererY.new(root, {});
yRenderer.grid.template.set("visible", false);

var yAxis = chart.yAxes.push(
am5xy.CategoryAxis.new(root, {
categoryField: "name",
renderer: yRenderer,
paddingRight:40
})
);

var xRenderer = am5xy.AxisRendererX.new(root, {});
xRenderer.grid.template.set("strokeDasharray", [3]);

var xAxis = chart.xAxes.push(
am5xy.ValueAxis.new(root, {
min: 0,
renderer: xRenderer
})
);

// Add series
// https://www.amcharts.com/docs/v5/charts/xy-chart/series/
var series = chart.series.push(
am5xy.ColumnSeries.new(root, {
name: "Income",
xAxis: xAxis,
yAxis: yAxis,
valueXField: "steps",
categoryYField: "name",
sequencedInterpolation: true,
calculateAggregates: true,
maskBullets: false,
tooltip: am5.Tooltip.new(root, {
dy: -30,
pointerOrientation: "vertical",
labelText: "{valueX}"
})
})
);

series.columns.template.setAll({
strokeOpacity: 0,
cornerRadiusBR: 10,
cornerRadiusTR: 10,
cornerRadiusBL: 10,
cornerRadiusTL: 10,
maxHeight: 50,
fillOpacity: 0.8
});

var currentlyHovered;

series.columns.template.events.on("pointerover", function(e) {
handleHover(e.target.dataItem);
});

series.columns.template.events.on("pointerout", function(e) {
handleOut();
});

function handleHover(dataItem) {
if (dataItem && currentlyHovered != dataItem) {
handleOut();
currentlyHovered = dataItem;
var bullet = dataItem.bullets[0];
bullet.animate({
key: "locationX",
to: 1,
duration: 600,
easing: am5.ease.out(am5.ease.cubic)
});
}
}

function handleOut() {
if (currentlyHovered) {
var bullet = currentlyHovered.bullets[0];
bullet.animate({
key: "locationX",
to: 0,
duration: 600,
easing: am5.ease.out(am5.ease.cubic)
});
}
}


var circleTemplate = am5.Template.new({});

series.bullets.push(function(root, series, dataItem) {
var bulletContainer = am5.Container.new(root, {});
var circle = bulletContainer.children.push(
am5.Circle.new(
root,
{
  radius: 34
},
circleTemplate
)
);

var maskCircle = bulletContainer.children.push(
am5.Circle.new(root, { radius: 27 })
);

// only containers can be masked, so we add image to another container
var imageContainer = bulletContainer.children.push(
am5.Container.new(root, {
mask: maskCircle
})
);

// not working
var image = imageContainer.children.push(
am5.Picture.new(root, {
templateField: "pictureSettings",
centerX: am5.p50,
centerY: am5.p50,
width: 60,
height: 60
})
);

return am5.Bullet.new(root, {
locationX: 0,
sprite: bulletContainer
});
});

// heatrule
series.set("heatRules", [
{
dataField: "valueX",
min: am5.color(0xe5dc36),
max: am5.color(0x5faa46),
target: series.columns.template,
key: "fill"
},
{
dataField: "valueX",
min: am5.color(0xe5dc36),
max: am5.color(0x5faa46),
target: circleTemplate,
key: "fill"
}
]);

series.data.setAll(data);
yAxis.data.setAll(data);

var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {}));
cursor.lineX.set("visible", false);
cursor.lineY.set("visible", false);

cursor.events.on("cursormoved", function() {
var dataItem = series.get("tooltip").dataItem;
if (dataItem) {
handleHover(dataItem)
}
else {
handleOut();
}
})

// Make stuff animate on load
// https://www.amcharts.com/docs/v5/concepts/animations/
series.appear();
chart.appear(1000, 100);

});
}

