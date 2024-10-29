window.dash_clientside = Object.assign({}, window.dash_clientside, {
    echartsScoreDiff: {
        ScoreDiff: function(appData) {
            var chartDom = document.getElementById('echarts_area_score_diff');
            var myChart = echarts.init(chartDom);

            // Parse les données JSON
            const data = JSON.parse(appData);
            const timeData = data.map(d => d.TOTAL_MINUTES);
            const scoreDiffData = data.map(d => d.SCORE_DIFF);

            // Préparer deux séries : une pour les valeurs positives et une pour les valeurs négatives
            const positiveData = scoreDiffData.map(value => (value >= 0 ? value : null));
            const negativeData = scoreDiffData.map(value => (value < 0 ? value : null));

            var option = {
                tooltip: {
                    trigger: 'axis',
                    formatter: function (params) {
                        return params[0].axisValue + '<br/>' + 
                                'Écart de Score: ' + params[0].data;
                    }
                },
                xAxis: {
                    type: 'category',
                    data: timeData,
                    name: 'Temps écoulé (mm:ss)',
                    nameLocation: 'middle',
                    nameGap: 30
                },
                yAxis: {
                    type: 'value',
                    name: 'Écart de Score',
                    nameLocation: 'middle',
                    nameGap: 50
                },
                series: [
                    // Série pour les valeurs positives
                    {
                        name: 'Écart positif',
                        data: positiveData,
                        type: 'line',
                        areaStyle: { color: 'rgba(82, 114, 242, 0.5)' },  // Bleu clair pour les valeurs positives
                        lineStyle: { color: 'rgba(82, 114, 242, 1)' },
                        smooth: true
                    },
                    // Série pour les valeurs négatives
                    {
                        name: 'Écart négatif',
                        data: negativeData,
                        type: 'line',
                        areaStyle: { color: 'rgba(242, 114, 82, 0.5)' },  // Rouge clair pour les valeurs négatives
                        lineStyle: { color: 'rgba(242, 114, 82, 1)' },
                        smooth: true
                    }
                ],
                grid: {
                    left: '0%', right: '0%', top: '0%', bottom: '0%', containLabel: true
                }
            };

            // Appliquer l'option et activer le redimensionnement automatique
            myChart.setOption(option);
            window.addEventListener('resize', () => myChart.resize());
        }
    }
});
            
