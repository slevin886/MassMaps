const mymap = L.map('mapid').setView([42.338032,-71.211578], 10);
//[42.360960, -71.058200], 1

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/light-v10',
    accessToken: 'pk.eyJ1Ijoic2xldmluODg2IiwiYSI6ImNrNGhtZTNneTFiZXczbW83eXgweWVrcXcifQ.vtx-bvQmfcVdM-ZEswS3Sg'
}).addTo(mymap);

function getColor(value){
    //value from 0 to 1
    let hue = ((1-value)*120).toString(10);
    return ["hsl(",hue,",100%,50%)"].join("");
}

for (let i = 0; i < avgCommutes.length; i++) {
    let locale = avgCommutes[i];
    let rank = 1 - (1 / avgCommutes.length) * i;
    let circle = L.circle(
      [locale['origin__latitude'], locale['origin__longitude']], {
          color: getColor(rank),
          opacity: 0.7,
          border: 'black',
          fill: '#f03',
          fillOpacity: 0.1,
          radius: 500,
      }
    ).addTo(mymap);
    circle.bindPopup(
      locale['origin__name']
      + '<br>' +
      'Avg. Miles/Minute: ' + Math.round(locale['average_time_dist']).toString()
      + '<br>' +
      'Avg. Minutes: ' + Math.round(locale['average_time']).toString()
    );
}


const commonLayout = {
  // 'plot_bgcolor': '#F8F8F8',
  // 'paper_bgcolor':'#F8F8F8',
  'hovermode': 'closest',
  'font': {'family': 'Helvetica Neue'},
  // 'height': 350
};

function drawTimeSeries(timeData, htmlId) {
  const data = [{
    'x': timeData.map(a => a.time),
    'y': timeData.map(a => a.avg_time),
    'type': 'scatter',
  }];
  const layout = {
    'yaxis': {'title': 'Avg. Commute Minutes',},
    'xaxis': {'title': 'Date'},
    ...commonLayout
  };
  Plotly.newPlot(htmlId, data, layout, {"displayModeBar": false});
}


function drawHorizontalBars(barData, htmlId, start=0, stop=10, reverse=true, color='green') {
  let yData = barData.slice(start, stop).map(a => a.origin__name);
  let xData = barData.slice(start, stop).map(a => a.average_time_dist);
  if (reverse){
    yData.reverse();
    xData.reverse();
  }
  const data = [{
    type: 'bar',
    orientation: 'h',
    marker: {color: color},
    x: xData,
    y: yData,
  }];
  const layout = {
    xaxis: {title: 'minutes per mile', automargin: true, range: [0, 6]},
    yaxis: {automargin: true},
    margin: {l: 120},
    ...commonLayout
  };
  Plotly.newPlot(htmlId, data, layout, {"displayModeBar": false});
}

drawTimeSeries(eveningCommutes, 'timePlot');
drawHorizontalBars(avgCommutes, 'fastest_avg');
drawHorizontalBars(avgCommutes, 'slowest_avg',
  avgCommutes.length - 10, avgCommutes.length, true, 'red');
console.log(avgCommutes);