angular.module("evcconfigurations.services", ["ngResource"]).
    factory('Configuration', function ($resource) {
        var Configuration = $resource('/api/v1/evcconfigurations/:configurationId', {configurationId: '@id'});
        Configuration.prototype.isNew = function(){
            return (typeof(this.id) === 'undefined');
        }
        return Configuration;
    });

angular.module("evcconfigurations", ["evcconfigurations.services"]).
    config(function ($routeProvider) {
        $routeProvider
            .when('/', {templateUrl: '/static/views/configurations/list.html', controller: ConfigurationListController})
            .when('/configurations/new', {templateUrl: '/static/views/configurations/create.html', controller: ConfigurationCreateController})
            .when('/configurations/:configurationId', {templateUrl: '/static/views/configurations/detail.html', controller: ConfigurationDetailController});
    });

function ConfigurationListController($scope, Configuration) {
    $scope.configurations = Configuration.query();
    
}

function ConfigurationCreateController($scope, $routeParams, $location, Configuration) {

    $scope.configuration = new Configuration();

    $scope.save = function () {
    	$scope.configuration.$save(function (configuration, headers) {
    		toastr.success("Submitted New Configuration");
            $location.path('/');
        });
    };
}


function ConfigurationDetailController($scope, $routeParams, $location, Configuration) {
    var configurationId = $routeParams.configurationId;
    
    $scope.configuration = Configuration.get({configurationId: configurationId});

}
