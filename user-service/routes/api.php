<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;

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

// Public authentication routes
Route::prefix('auth')->group(function () {
    Route::post('/login', [AuthController::class, 'login']);
    Route::post('/register', [AuthController::class, 'register']);
    Route::post('/verify-code', [AuthController::class, 'verifySubscriptionCode']);
    Route::post('/telegram', [AuthController::class, 'telegramAuth']);
});

// Protected routes
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/user', function (Request $request) {
        return $request->user();
    });
    
    Route::prefix('auth')->group(function () {
        Route::get('/profile', [AuthController::class, 'profile']);
        Route::put('/profile', [AuthController::class, 'updateProfile']);
        Route::post('/logout', [AuthController::class, 'logout']);
    });
    
    // User Service API Routes
    Route::prefix('users')->group(function () {
        Route::get('/', [App\Http\Controllers\Api\UserController::class, 'index']);
        Route::post('/', [App\Http\Controllers\Api\UserController::class, 'store']);
        Route::get('/{id}', [App\Http\Controllers\Api\UserController::class, 'show']);
        Route::put('/{id}', [App\Http\Controllers\Api\UserController::class, 'update']);
        Route::delete('/{id}', [App\Http\Controllers\Api\UserController::class, 'destroy']);
        Route::get('/{id}/profile', [App\Http\Controllers\UserController::class, 'profile']);
    });

    Route::prefix('subscriptions')->group(function () {
        Route::get('/', [App\Http\Controllers\Api\SubscriptionController::class, 'index']);
        Route::post('/', [App\Http\Controllers\Api\SubscriptionController::class, 'store']);
        Route::post('/activate', [App\Http\Controllers\Api\SubscriptionController::class, 'activate']);
        Route::get('/{id}', [App\Http\Controllers\Api\SubscriptionController::class, 'show']);
        Route::put('/{id}', [App\Http\Controllers\Api\SubscriptionController::class, 'update']);
    });
});
