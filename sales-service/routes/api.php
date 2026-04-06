<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\AccountingController;
use App\Http\Controllers\Api\ExpenseController;
use App\Http\Controllers\Api\SalesController;

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
    Route::get('/', [SalesController::class, 'index']);
    Route::post('/', [SalesController::class, 'store']);
    Route::post('/record-digit', [SalesController::class, 'storeEntry']);
    Route::get('/report/daily', [SalesController::class, 'dailyReport']);
    Route::get('/report/monthly', [SalesController::class, 'monthlyReport']);
    Route::get('/{id}', [SalesController::class, 'show']);
    Route::put('/{id}', [SalesController::class, 'update']);
    Route::delete('/{id}', [SalesController::class, 'destroy']);
});

Route::prefix('expenses')->group(function () {
    Route::get('/', [ExpenseController::class, 'index']);
    Route::get('/categories', [ExpenseController::class, 'categories']);
    Route::get('/summary', [ExpenseController::class, 'summary']);
    Route::post('/', [ExpenseController::class, 'store']);
    Route::get('/{id}', [ExpenseController::class, 'show']);
    Route::put('/{id}', [ExpenseController::class, 'update']);
    Route::delete('/{id}', [ExpenseController::class, 'destroy']);
});

Route::prefix('accounting')->group(function () {
    Route::get('/profit-loss', [AccountingController::class, 'profitLoss']);
    Route::get('/summary', [AccountingController::class, 'summary']);
    Route::get('/top-products', [AccountingController::class, 'topProducts']);
});
