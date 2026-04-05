<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Services\AccountingService;
use Illuminate\Http\Request;
use Carbon\Carbon;

class AccountingController extends Controller
{
    protected $accountingService;

    public function __construct(AccountingService $accountingService)
    {
        $this->accountingService = $accountingService;
    }

    /**
     * Get profit and loss statement.
     */
    public function profitLoss(Request $request)
    {
        $startDate = $request->get('start_date') ? Carbon::parse($request->start_date) : null;
        $endDate = $request->get('end_date') ? Carbon::parse($request->end_date) : null;
        $userId = $request->get('user_id');

        $profitLoss = $this->accountingService->generateProfitLossStatement($startDate, $endDate, $userId);

        return response()->json($profitLoss);
    }

    /**
     * Get financial summary.
     */
    public function summary(Request $request)
    {
        $userId = $request->get('user_id');

        $summary = $this->accountingService->getFinancialSummary($userId);

        return response()->json($summary);
    }

    /**
     * Get top selling products.
     */
    public function topProducts(Request $request)
    {
        $limit = $request->get('limit', 10);
        $userId = $request->get('user_id');

        $topProducts = $this->accountingService->getTopSellingProducts($limit, $userId);

        return response()->json([
            'top_products' => $topProducts
        ]);
    }
}
