var app = angular.module('myApp', []);
app.controller('myCtrl',function ($scope, $http, $interval) {
    $scope.config = '';
    $scope.overlay = '';
    $scope.fileLocation = '';
    $scope.get_item_list = function () {
        var url = "get_item_list";
        $http.get(url).success(function (result) {
            $scope.item_list = result;
            $scope.selectedItemList = result[0];
        }).error(function () {
            toastr.error("failed");
        });
        console.log(document.location.toString());
    };

    $scope.go_config = function(){
        var url = 'go_config?spectrum='+$scope.selectedItemList+'&file_location='+$scope.fileLocation
        window.open(url)
    };

    $scope.get_item_list();
});