var mainApp = angular.module('mainApp', ['Services', 'Controllers', 'ngResource', 'ngRoute'], function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
}).config(function($resourceProvider, $httpProvider, $routeProvider) {
    $resourceProvider.defaults.stripTrailingSlashes = false;
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $routeProvider.
        when('/', {
            templateUrl: '/static/partials/home.html',
            controller: 'MainController'
        })
      .otherwise({
        redirectTo: '/'
      });
});