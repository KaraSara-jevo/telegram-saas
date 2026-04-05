<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

// User Service API Routes
Route::prefix('users')->group(function () {
    Route::get('/', [App\Http\Controllers\Api\UserController::class, 'index']);
    Route::post('/', [App\Http\Controllers\Api\UserController::class, 'store']);
    Route::get('/{id}', [App\Http\Controllers\Api\UserController::class, 'show']);
    Route::put('/{id}', [App\Http\Controllers\Api\UserController::class, 'update']);
    Route::delete('/{id}', [App\Http\Controllers\Api\UserController::class, 'destroy']);
});

Route::prefix('subscriptions')->group(function () {
    Route::get('/', [App\Http\Controllers\Api\SubscriptionController::class, 'index']);
    Route::post('/', [App\Http\Controllers\Api\SubscriptionController::class, 'store']);
    Route::get('/{id}', [App\Http\Controllers\Api\SubscriptionController::class, 'show']);
    Route::put('/{id}', [App\Http\Controllers\Api\SubscriptionController::class, 'update']);
});
