<script type="text/javascript">
Highcharts.setOptions({global:{useUTC:false}});
function loadGraph() {
    $('#graph-container').highcharts({
        chart: {
            type: 'area'
        },
        title: {
            text: '{{chart['title']}}'
        },
        subtitle: {
            text: '{{chart['subtitle']}}'
        },
        xAxis: {
            tickInterval: 1000 * 60 * 60,
        type: 'datetime',
        labels: {
            formatter: function() {
                var monthStr = Highcharts.dateFormat('%Y-%m-%d %H:%M', this.value);
                return monthStr
            },
        },
        },
        yAxis: {
            title: {
                text: '{{chart['ytitle']}}'
            },
            labels:{
                formatter: function(){
                    return this.value + ' {{unit}}'
                }
            }
        },
        plotOptions: {
            area: {
                marker: {
                    enabled: false,
                    symbol: 'circle',
                    radius: 2,
                    states: {
                        hover: {
                            enabled: true
                        }
                    }
                }
            },
            // 在这里，可以修改点击事件。
            series: { 
                cursor: 'pointer', 
                point: {
                    events: {
                        click: function() {
                            alert('abc');
                            // var query = {
                            //     dtype:this.series.name,
                            //     service:document.getElementById('service').value,
                            //     time:Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x)
                            // };
                            // var obj = this;
                            // $.get('time-detail', query, function(res){
                            //     var res = eval('('+res+')');
                            //     var thead = '<thead><tr>';
                            //     for (i=0;i<res[0].length;i++) {
                            //         thead = thead + '<th>' + res[0][i] + '</th>';
                            //     }
                            //     thead = thead + '</tr></thead>';
                            //     var tbody = '<tbody>';
                            //     for (i=1;i<res.length;i++) {
                            //         tbody = tbody + '<tr>';
                            //         for (j=0;j<res[i].length;j++) {
                            //             tbody = tbody + '<td>' + res[i][j] + '</td>';
                            //         }
                            //         tbody = tbody + '</tr>';
                            //     }
                            //     tbody = tbody + '</tbody>';
                            //     var table = '<div><a href="time-detail?host=' + query['host'] +
                            //         '&dtype=' + query['dtype'] + '&service=' + query['service'] +
                            //         '&time=' + query['time'] + '&html=1" target="_blank">Open in New Window</a></div>' +
                            //         '<table class="table table-striped table-hover">' + thead + tbody + '</table>';
                            //     hs.htmlExpand(null, {
                            //         headingText: obj.series.name,
                            //         maincontentText: table,
                            //         width: 1500
                            //     });
                            // });
                        }
                    }
                },
                marker: {
                    lineWidth: 1
                }
            }
        },
        tooltip: {
            formatter: function(){
                var start = Highcharts.dateFormat('[%H:%M -', this.x);
                var end = Highcharts.dateFormat(' %H:%M]', this.x+600*1000);
                return '<b>'+this.series.name+'</b><br>' + start + end + ' : ' +this.y + '{{unit}}'; 
            }
        },
        series: [
            {% for series in dataset %}
                {
                    name: "{{series['name']}}",
                    color: "{{series['color']}}",
                    data: [
                        {% for row in series['stats'] %}
                            {% set time, value =row['time'], row['value'] %}
                            [{{time}}, {{value}}],
                        {% endfor %}
                    ]
                },
            {% endfor %}
        ]
    });
}
$(document).ready(function(){
    loadGraph();
})
</script>
