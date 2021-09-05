var cleanupdata = [
  {
    x: ['03/09/2021', '04/09/2021', '05/09/2021','06/09/2021', '07/09/2021', '08/09/2021','09/09/2021'],
    y: [20, 14, 23,29, 85, 15,34],
    type: 'bar',
    marker: {color: 'rgb(26, 118, 255)'}
  }
];

var cleanupdata_layout = {

  xaxis: {tickfont: {
      size: 14,
      color: 'rgb(107, 107, 107)'
    }},
  yaxis: {
    tickfont: {
      size: 14,
      color: 'rgb(107, 107, 107)'
    }
  },
  legend: {
    x: 0,
    y: 1.0,
    bgcolor: 'rgba(255, 255, 255, 0)',
    bordercolor: 'rgba(255, 255, 255, 0)'
  }
};

Plotly.newPlot('cleanupdatabarchart', cleanupdata,cleanupdata_layout);


var critical_app_data= [
  {
    x: ['T1', 'T2', 'T3','T4','T5','T6','T7','T8','T9','T10',
        'T11','T12', 'T13','T14','T15','T16','T17','T18','T19','T20',
        'T21','T22','T23','T24'],
    y: [20,14,23,29,85,15,34,14,23,29,
        22,17,28,22,65,32,38,24,29,39,
        43,67,32,56],
    type: 'bar',
    marker: {color: 'rgb(13,248,246)'} 
  }
];

var critical_app_data_layout = {

  xaxis: {tickfont: {
      size: 14,
      color: 'rgb(107, 107, 107)'
    }},
  yaxis: {
    tickfont: {
      size: 14,
      color: 'rgb(107, 107, 107)'
    }
  },
  legend: {
    x: 0,
    y: 1.0,
    bgcolor: 'rgba(255, 255, 255, 0)',
    bordercolor: 'rgba(255, 255, 255, 0)'
  }
};

Plotly.newPlot('critical_app_data_barchart', critical_app_data,critical_app_data_layout);

// var layout = {
// width: 500,
// height: 200,
// margin: {"t": 0, "b": 0, "l": 0, "r": 0}
// };

// Plotly.newPlot('barchartdbtrend', data, layout);


/////////////////////////////////////////////////////////////////////////////////

// var data = [
// 	{
// 		domain: { x: [0, 1], y: [0, 1] },
// 		value: 2280,
// 		title: { text: "P1" },
// 		type: "indicator",
// 		mode: "gauge+number",
//     margin: {"t": 0, "b": 20, "l": 0, "r": 0}
// 	}
// ];
// var data1 = [
// 	{
// 		domain: { x: [0, 1], y: [0, 1] },
// 		value: 2180,
// 		title: { text: "P2" },
// 		type: "indicator",
// 		mode: "gauge+number"
// 	}
// ];
// var layoutgauge = {
//   width: 250, height:140,
//   margin: {"t": 30, "b": 0, "l": 30, "r": 50},
//   font: {
//     family: 'Courier New, monospace',
//     color: '#FFFFFF'
//   },
// };

// var data2 = [
// 	{
// 		domain: { x: [0, 1], y: [0, 1] },
// 		value: 2300,
// 		title: { text: "P3" },
// 		type: "indicator",
// 		mode: "gauge+number",
//     margin: {"t": 0, "b": 0, "l": 0, "r": 0}
// 	}
// ];
// var data3 = [
// 	{
// 		domain: { x: [0, 1], y: [0, 1] },
// 		value: 2000,
// 		title: { text: "P4" },
// 		type: "indicator",
// 		mode: "gauge+number",
//     margin: {"t": 0, "b": 0, "l": 0, "r": 0}
// 	}
// ];


// var layout = { width: 400, height:250};
// Plotly.newPlot('gauge', data, layoutgauge);
// Plotly.newPlot('gauge1', data1, layoutgauge);
// Plotly.newPlot('gauge2', data2, layoutgauge);
// Plotly.newPlot('gauge3', data3, layoutgauge);
// Plotly.newPlot('gauge2', data2, layout);
// Plotly.newPlot('gauge3', data3, layout);


/////////////////////////////////////////////////////////////////////////////

var piedata = [{
  type: "pie",
  values: [100,50],
  title: { text: "P1" },
  labels: ["Total", "Remaining"],
  textinfo: "label+percent",
  textposition: "outside",
  margin: {"t": 0, "b": 0, "l": 0, "r": 0}
}]
var piedata1 = [{
  type: "pie",
  values: [100,30],
  title: { text: "P2" },
  labels: ["Total", "Remaining"],
  textinfo: "label+percent",
  textposition: "outside",
  margin: {"t": 0, "b": 0, "l": 0, "r": 0}
}]
var piedata2 = [{
  type: "pie",
  values: [100,60],
  title: { text: "P3" },
  labels: ["Total", "Remaining"],
  textinfo: "label+percent",
  textposition: "outside",
  margin: {"t": 0, "b": 0, "l": 0, "r": 0}
}]
var piedata3 = [{
  type: "pie",
  values: [100,45],
  title: { text: "P4" },
  labels: ["Total", "Remaining"],
  textinfo: "label+percent",
  textposition: "outside",
  margin: {"t": 0, "b": 0, "l": 0, "r": 0}
}]

var layoutpie = {
  width: 300, height:140,
  margin: {"t": 0, "b": 0, "l": 0, "r": 0},
  font: {
    family: 'Courier New, monospace',
    color: '#FFFFFF'
  },
  showlegend:false
};

var pielayout = {
  height: 300,
  width: 300,
  showlegend: false
  }

Plotly.newPlot('piechart', piedata, layoutpie)
Plotly.newPlot('piechart1', piedata1, layoutpie)
Plotly.newPlot('piechart2', piedata2, layoutpie)
Plotly.newPlot('piechart3', piedata3, layoutpie)

