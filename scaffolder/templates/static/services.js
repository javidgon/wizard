var Services = angular.module('Services', ['ngResource']);

{% for app in apps %}
// Services for {{ app.name }}
{% for model in app.models %}
Services.factory('{{ model.name }}', ['$resource',
    function($resource) {
        return $resource(
            '/api/v1/{{ app.name }}/{{ model.name | lower }}s/:{{ model.name | lower }}Id/',
            {
                {{ model.name | lower }}Id: '@{{ model.name | lower }}Id'
            },
            {
                query: {method: 'GET', isArray: true, cache: false},
                get: {method: 'GET'},
                post: {method: 'POST'},
                put: {method: 'PUT'},
                delete: {method: 'DELETE'}
            });
    }]);

{% endfor %}
{% endfor %}