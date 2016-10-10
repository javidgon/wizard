var Controllers = angular.module('Controllers', ['Services']);

Controllers.controller('MainController', function MainController($scope) {
  /* Feel free to replace this placeholder content! */
  $scope.entries = [
    {
      name: 'Nexus S',
    }, {
      name: 'Motorola XOOM with Wi-Fi',
    }, {
      name: 'MOTOROLA XOOM',
    }
  ];
});
/* If you need Controllers for your Resources, you can uncomment them out.

{% for app in apps %}{% for model in app.models %}
Controllers.controller('{{ model.name }}Controller', function {{ model.name }}Controller($scope, {{ model.name }}) {

  // Generic GET (list)
  {{ model.name }}.query().$promise.then(function (data) {
    console.log('{{ model.name }}: ' + data)
  });
  // Generic GET (detail)
  {{ model.name }}.get({'{{ model.name | lower}}Id': 1}).$promise.then(function (data) {
    console.log('{{ model.name }}: ' + data)
  });
  // Generic POST
  {{ model.name }}.post({'{{ model.name | lower}}Id': 1}, {}).$promise.then(function (data) {
    console.log('{{ model.name }}: ' + data)
  });
  // Generic PUT
  {{ model.name }}.put({'{{ model.name | lower}}Id': 1}, {}).$promise.then(function (data) {
    console.log('{{ model.name }}: ' + data)
  });
  // Generic DELETE
  {{ model.name }}.delete({'{{ model.name | lower}}Id': 1}).$promise.then(function (data) {
    console.log('{{ model.name }}: ' + data)
  });

});{% endfor %}
{% endfor %}*/