$(document).ready(function() {
    ctx = $("#icists-chart").get(0).getContext("2d");
    buttonReady();
});


var colors = [
    '#a6cee3',
    '#1f78b4',
    '#b2df8a',
    '#33a02c',
    '#fb9a99',
    '#e31a1c',
    '#fdbf6f',
    '#ff7f00',
    '#cab2d6',
    '#6a3d9a',
    '#ffff99',
    '#b15928'
]
var ctx = undefined;
var chart = undefined;
var canvasData = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
        {
            label: "My First dataset",
            fillColor: "rgba(220,220,220,0.5)",
            strokeColor: "rgba(220,220,220,0.8)",
            highlightFill: "rgba(220,220,220,0.75)",
            highlightStroke: "rgba(220,220,220,1)",
            data: [65, 59, 80, 81, 56, 55, 40]
        },
    ]
}


var drawLine = function() {
    if (chart != undefined) {
        chart.destroy();
    }
    chart = new Chart(ctx).Line(canvasData);
}


var drawPie = function() {
    if (chart != undefined) {
        chart.destroy();
    }
    options = {
        segmentStrokeColor: "#ddd"
    }
    chart = new Chart(ctx).Pie(canvasData, options);
}


var buttonReady = function() {
    $(".dataset").on('click', function(e) {
        e.preventDefault();
        var request_url = 'error';
        if ($(this).text() === 'Application Category') {
            request_url = 'application_category';
        } else if ($(this).text() === 'Application Status') {
            request_url = 'application_status';
        } else if ($(this).text() === 'Gender') {
            request_url = 'gender';
        } else if ($(this).text() === 'Nationality') {
            request_url = 'nationality';
        } else if ($(this).text() === 'University') {
            request_url = 'university';
        } else if ($(this).text() === 'Project Topic') {
            request_url = 'project_topic';
        } else if ($(this).text() === 'Visa') {
            request_url = 'visa';
        } else if ($(this).text() === 'Group Discount') {
            request_url = 'group_discount';
        } else if ($(this).text() === 'How You Found Us') {
            request_url = 'how_you_found_us';
        } else if ($(this).text() === 'Submit Time') {
            request_url = 'submit_time';
        }

        $.getJSON('/statistics/' + request_url, function(result) {
            if (request_url !== 'submit_time') {
                var data = [];
                var idx = 0;
                $.each(result, function(i, field) {
                    data.push({
                        value: field,
                        color: colors[idx%colors.length],
                        label: i
                    });
                    idx++;
                });
                canvasData = data;
                drawPie();
            } else {
                var labels = [];
                var data = [];
                $.each(result, function(i, field) {
                    labels.push(i);
                    data.push(field);
                });
                canvasData = {
                    labels: labels,
                    datasets: [
                        {
                            label: $(this).text(),
                            fillColor: "rgba(151,187,205, 0.2)",
                            strokeColor: "rgba(151,187,205,1)",
                            pointColor: "rgba(151,187,205,1)",
                            pointStrokeColor: "#fff",
                            pointHighlightFill: "#fff",
                            pointHighlightStroke: "rgba(151,187,205,1)",
                            data: data,
                        }
                    ]
                }
                drawLine();
            }
        });
    });
}
