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

// Sales Service API Routes
Route::prefix('sales')->group(function () {
    Route::get('/', [App\Http\Controllers\Api\SalesController::class, 'index']);
    Route::post('/', [App\Http\Controllers\Api\SalesController::class, 'store']);
    Route::get('/{id}', [App\Http\Controllers\Api\SalesController::class, 'show']);
    Route::put('/{id}', [App\Http\Controllers\Api\SalesController::class, 'update']);
    Route::delete('/{id}', [App\Http\Controllers\Api\SalesController::class, 'destroy']);
    Route::get('/report/daily', [App\Http\Controllers\Api\SalesController::class, 'dailyReport']);
    Route::get('/report/monthly', [App\Http\Controllers\Api\SalesController::class, 'monthlyReport']);
});

Route::prefix('expenses')->group(function () {
    Route::get('/', [App\Http\Controllers\Api\ExpenseController::class, 'index']);
    Route::post('/', [App\Http\Controllers\Api\ExpenseController::class, 'store']);
    Route::get('/{id}', [App\Http\Controllers\Api\ExpenseController::class, 'show']);
    Route::put('/{id}', [App\Http\Controllers\Api\ExpenseController::class, 'update']);
    Route::delete('/{id}', [App\Http\Controllers\Api\ExpenseController::class, 'destroy']);
});

Route::prefix('accounting')->group(function () {
    Route::get('/profit-loss', [App\Http\Controllers\Api\AccountingController::class, 'profitLoss']);
    Route::get('/summary', [App\Http\Controllers\Api\AccountingController::class, 'summary']);
});
