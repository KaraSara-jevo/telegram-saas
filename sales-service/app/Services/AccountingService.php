<?php

namespace App\Services;

use App\Models\Sale;
use App\Models\Expense;
use Carbon\Carbon;
use Illuminate\Support\Facades\DB;

class AccountingService
{
    /**
     * Calculate profit and loss for a given period.
     */
    public function calculateProfitLoss($startDate = null, $endDate = null, $userId = null): array
    {
        $startDate = $startDate ?: Carbon::now()->startOfMonth();
        $endDate = $endDate ?: Carbon::now()->endOfMonth();

        // Get sales data
        $salesQuery = Sale::dateRange($startDate, $endDate);
        if ($userId) {
            $salesQuery->forUser($userId);
        }
        
        $sales = $salesQuery->get();
        $totalRevenue = $sales->sum('total_amount');
        $totalProfit = $sales->sum(function ($sale) {
            return $sale->profit;
        });

        // Get expenses data
        $expensesQuery = Expense::dateRange($startDate, $endDate);
        if ($userId) {
            $expensesQuery->forUser($userId);
        }
        
        $expenses = $expensesQuery->get();
        $totalExpenses = $expenses->sum('amount');

        // Calculate profit/loss
        $netProfitLoss = $totalProfit - $totalExpenses;

        return [
            'period' => [
                'start_date' => $startDate->toDateString(),
                'end_date' => $endDate->toDateString(),
            ],
            'revenue' => [
                'total' => $totalRevenue,
                'sales_count' => $sales->count(),
                'average_sale' => $sales->count() > 0 ? $totalRevenue / $sales->count() : 0,
            ],
            'profit' => [
                'total' => $totalProfit,
                'profit_margin' => $totalRevenue > 0 ? ($totalProfit / $totalRevenue) * 100 : 0,
            ],
            'expenses' => [
                'total' => $totalExpenses,
                'expense_count' => $expenses->count(),
                'average_expense' => $expenses->count() > 0 ? $totalExpenses / $expenses->count() : 0,
                'by_category' => $expenses->groupBy('category')->map(function ($categoryExpenses) {
                    return [
                        'total' => $categoryExpenses->sum('amount'),
                        'count' => $categoryExpenses->count(),
                    ];
                }),
            ],
            'summary' => [
                'net_profit_loss' => $netProfitLoss,
                'is_profitable' => $netProfitLoss >= 0,
            ],
        ];
    }

    /**
     * Get financial summary for dashboard.
     */
    public function getFinancialSummary($userId = null): array
    {
        $today = Carbon::today();
        $thisMonth = Carbon::now()->startOfMonth();
        $lastMonth = Carbon::now()->subMonth()->startOfMonth();
        $lastMonthEnd = Carbon::now()->subMonth()->endOfMonth();

        // Today's data
        $todaySales = Sale::today();
        $todayExpenses = Expense::today();
        if ($userId) {
            $todaySales->forUser($userId);
            $todayExpenses->forUser($userId);
        }

        $todayRevenue = $todaySales->sum('total_amount');
        $todayProfit = $todaySales->get()->sum(function ($sale) {
            return $sale->profit;
        });
        $todayExpenseTotal = $todayExpenses->sum('amount');

        // This month data
        $thisMonthSales = Sale::thisMonth();
        $thisMonthExpenses = Expense::thisMonth();
        if ($userId) {
            $thisMonthSales->forUser($userId);
            $thisMonthExpenses->forUser($userId);
        }

        $thisMonthRevenue = $thisMonthSales->sum('total_amount');
        $thisMonthProfit = $thisMonthSales->get()->sum(function ($sale) {
            return $sale->profit;
        });
        $thisMonthExpenseTotal = $thisMonthExpenses->sum('amount');

        // Last month data for comparison
        $lastMonthSales = Sale::dateRange($lastMonth, $lastMonthEnd);
        $lastMonthExpenses = Expense::dateRange($lastMonth, $lastMonthEnd);
        if ($userId) {
            $lastMonthSales->forUser($userId);
            $lastMonthExpenses->forUser($userId);
        }

        $lastMonthRevenue = $lastMonthSales->sum('total_amount');
        $lastMonthProfit = $lastMonthSales->get()->sum(function ($sale) {
            return $sale->profit;
        });
        $lastMonthExpenseTotal = $lastMonthExpenses->sum('amount');

        return [
            'today' => [
                'revenue' => $todayRevenue,
                'profit' => $todayProfit,
                'expenses' => $todayExpenseTotal,
                'net' => $todayProfit - $todayExpenseTotal,
                'sales_count' => $todaySales->count(),
                'expense_count' => $todayExpenses->count(),
            ],
            'this_month' => [
                'revenue' => $thisMonthRevenue,
                'profit' => $thisMonthProfit,
                'expenses' => $thisMonthExpenseTotal,
                'net' => $thisMonthProfit - $thisMonthExpenseTotal,
                'sales_count' => $thisMonthSales->count(),
                'expense_count' => $thisMonthExpenses->count(),
            ],
            'comparison' => [
                'revenue_change' => $this->calculatePercentageChange($lastMonthRevenue, $thisMonthRevenue),
                'profit_change' => $this->calculatePercentageChange($lastMonthProfit, $thisMonthProfit),
                'expenses_change' => $this->calculatePercentageChange($lastMonthExpenseTotal, $thisMonthExpenseTotal),
            ],
        ];
    }

    /**
     * Get top selling products.
     */
    public function getTopSellingProducts($limit = 10, $userId = null): array
    {
        $query = Sale::select(
                'product_id',
                DB::raw('COUNT(*) as sales_count'),
                DB::raw('SUM(quantity) as total_quantity'),
                DB::raw('SUM(total_amount) as total_revenue')
            )
            ->groupBy('product_id')
            ->orderBy('total_revenue', 'desc')
            ->limit($limit);

        if ($userId) {
            $query->forUser($userId);
        }

        return $query->get()->toArray();
    }

    /**
     * Calculate percentage change between two values.
     */
    private function calculatePercentageChange($oldValue, $newValue): float
    {
        if ($oldValue == 0) {
            return $newValue > 0 ? 100 : 0;
        }

        return (($newValue - $oldValue) / $oldValue) * 100;
    }

    /**
     * Generate profit and loss statement.
     */
    public function generateProfitLossStatement($startDate = null, $endDate = null, $userId = null): array
    {
        $data = $this->calculateProfitLoss($startDate, $endDate, $userId);
        
        return [
            'title' => 'Profit & Loss Statement',
            'period' => $data['period'],
            'income' => [
                'total_revenue' => $data['revenue']['total'],
                'cost_of_goods_sold' => $data['revenue']['total'] - $data['profit']['total'],
                'gross_profit' => $data['profit']['total'],
                'gross_profit_margin' => $data['profit']['profit_margin'],
            ],
            'expenses' => $data['expenses'],
            'net_result' => [
                'net_profit' => $data['summary']['net_profit_loss'],
                'is_profitable' => $data['summary']['is_profitable'],
            ],
        ];
    }
}
