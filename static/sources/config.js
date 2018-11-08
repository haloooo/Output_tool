var app = angular.module('myConfig', []);
app.controller('myCtrl',function ($scope, $http, $interval) {
    $scope.spectrum = $('#spectrum').val();
    $scope.file_location = $('#file_location').val();
    $scope.getCSV = function () {
        var url = 'getCSV';
        $http.get(url,{
            params:{
                'spectrum':$scope.spectrum,
                'file_location':$scope.file_location
            }
        }).success(function (result) {
            $scope.csv_list = result;
        }).error(function () {
            alert('error')
        })
    };
    $scope.make_chart = function(){
        var url = 'make_chart';
        if($scope.csv_list.length == 0){
            toastr.error('Please upload file first');
            return
        }
        //显示
        $("#loadingModal").modal('show');
        $("#downloadBtn").attr('disabled',true);
        $http.get(url,{
            params:{
                'spectrum':$scope.spectrum,
                'data':JSON.stringify($scope.csv_list)
            }
        }).success(function (result) {
            if(result['state'] == 'success'){
                //隐藏
                $("#loadingModal").modal('hide');
                $("#downloadBtn").attr('disabled',false);
                window.open("download/" + result["png_zip"])
            }else if(result['state'] == 'error'){
                //隐藏
                $("#loadingModal").modal('hide');
                $("#downloadBtn").attr('disabled',false);
                toastr.error('Download zip file failed');
            }

            // var categories = [];
            // var series = [];
            // var name = '';
            // for(var i = 0; i < result.length; i++){
            //     for(var j = 0; j < result[i].length; j++){
            //         if(j == 8){
            //             name = result[i][j]['name'];
            //             categories = result[i][j]['x'];
            //             series = result[i][j]['data'];
            //             console.log(series);
            //             $scope.createChart(name,categories,series);
            //         }
            //     }
            // }
        }).error(function () {
            //隐藏
            $("#downloadBtn").attr('disabled',false);
            $("#loadingModal").modal('hide');
        })
    };
    $scope.createChart = function(name, categories, series){
        var title = {
            text: name
        };
        var subtitle = {
            text: 'Config,Overlay'
        };
        var xAxis = {
            title: {
                text: 'Frequency(Hz)'
            },
            categories: categories
        };
        var yAxis = {
            title: {
                text: 'Magnitude(deg.)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        };
        var tooltip = {
            valueSuffix: '\xB0C'
        };
        var legend = {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        };
        var exporting =  {
            // enabled : true,
            // buttons : {
            //     exportButton : {
            //         menuItems: [{
            //             text: '导出PNG图片(宽度为250px)',
            //             onclick:function() {
            //                 this.exportChart({
            //                     width:200 //导出报表的宽度  
            //                 });
            //             }
            //         }, {
            //             text: '导出PNG图片(宽度为800px)',
            //             onclick:function() {
            //                 this.exportChart();// 800px by default  
            //             }
            //         },
            //             null,
            //             null
            //         ]
            //     },
            //     printButton: {
            //         enabled : false
            //     }
            // },
            // filename : '停车场停车曲线图'
            url: '//export.highcharts.com.cn'
        };
        var series =  series;
        // var series =  [{
        //     name:"GH98377102AKPK61A+ZPYCAD",
        //     data:["1","2","3","3","3","3","3","3", "3"]
        // }];
        var json = {};
        json.title = title;
        json.subtitle = subtitle;
        json.xAxis = xAxis;
        json.yAxis = yAxis;
        json.tooltip = tooltip;
        json.legend = legend;
        json.exporting = exporting;
        json.series = series;
        var chart = $('#container').highcharts(json);

    };
    $scope.export = function(){
        for(var i = 0; i < Highcharts.charts.length; i++){
            if(Highcharts.charts[i] != undefined){
                Highcharts.charts[i].exportChartLocal()
            }
        }
        console.log(Highcharts.charts);
    };
    $scope.deleteFile = function(file_name){
        var url = "deleteFile";
        $http.get(url,{
            params:{
                'file_name':file_name
            }
        }).success(function (result) {
            if(result['state'] == 'success'){
                location.reload()
            }else if(result['state'] == 'error'){
                toastr.error('Delete file failed');
            }
        }).error(function () {
            toastr.error('error')
        })
    };
    $scope.getCSV();
    // $scope.createChart();
});