<?php

return [
    'name' => env('APP_NAME', 'Inventory Service'),
    'env' => env('APP_ENV', 'local'),
    'debug' => (bool) env('APP_DEBUG', true),
    'url' => env('APP_URL', 'http://localhost'),
    'timezone' => 'UTC',
    'locale' => 'en',
    'fallback_locale' => 'en',
    'faker_locale' => 'en_US',
    'key' => env('APP_KEY'),
    'cipher' => 'AES-256-CBC',
    'maintenance' => [
        'driver' => 'file',
    ],
    'providers' => array_merge(
        Illuminate\Support\ServiceProvider::defaultProviders()->toArray(),
        [
            App\Providers\AppServiceProvider::class,
            App\Providers\RouteServiceProvider::class,
        ]
    ),
    'aliases' => Illuminate\Support\Facades\Facade::defaultAliases()->toArray(),
];
