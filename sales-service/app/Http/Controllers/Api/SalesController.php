<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\DigitRecord;
use App\Models\Sale;
use App\Services\AccountingService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Carbon\Carbon;

class SalesController extends Controller
{
    protected $accountingService;

    public function __construct(AccountingService $accountingService)
    {
        $this->accountingService = $accountingService;
    }

    /**
     * Display a listing of sales.
     */
    public function index(Request $request)
    {
        $query = Sale::query();

        // Filter by user
        if ($request->has('user_id')) {
            $query->forUser($request->user_id);
        }

        // Filter by date range
        if ($request->has('start_date') && $request->has('end_date')) {
            $query->dateRange($request->start_date, $request->end_date);
        }

        // Filter by product
        if ($request->has('product_id')) {
            $query->where('product_id', $request->product_id);
        }

        // Filter by payment method
        if ($request->has('payment_method')) {
            $query->where('payment_method', $request->payment_method);
        }

        // Order by latest
        $query->orderBy('sale_date', 'desc');

        $sales = $query->paginate($request->get('per_page', 15));

        return response()->json($sales);
    }

    /**
     * Store a newly created sale.
     */
    public function store(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'user_id' => 'required|integer',
            'product_id' => 'required|integer',
            'quantity' => 'required|integer|min:1',
            'unit_price' => 'required|numeric|min:0',
            'payment_method' => 'required|string|max:50',
            'customer_name' => 'nullable|string|max:255',
            'customer_phone' => 'nullable|string|max:20',
            'notes' => 'nullable|string',
            'sale_date' => 'nullable|date',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $data = $request->all();
        $data['total_amount'] = $data['quantity'] * $data['unit_price'];
        $data['sale_date'] = $data['sale_date'] ?? now();

        $sale = Sale::create($data);

        return response()->json([
            'message' => 'Sale created successfully',
            'sale' => $sale
        ], 201);
    }

    /**
     * Display the specified sale.
     */
    public function show($id)
    {
        $sale = Sale::find($id);
        
        if (!$sale) {
            return response()->json(['error' => 'Sale not found'], 404);
        }

        return response()->json([
            'sale' => $sale,
            'profit' => $sale->profit,
        ]);
    }

    /**
     * Update the specified sale.
     */
    public function update(Request $request, $id)
    {
        $sale = Sale::find($id);
        
        if (!$sale) {
            return response()->json(['error' => 'Sale not found'], 404);
        }

        $validator = Validator::make($request->all(), [
            'quantity' => 'integer|min:1',
            'unit_price' => 'numeric|min:0',
            'payment_method' => 'string|max:50',
            'customer_name' => 'nullable|string|max:255',
            'customer_phone' => 'nullable|string|max:20',
            'notes' => 'nullable|string',
            'sale_date' => 'nullable|date',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $data = $request->all();
        
        // Recalculate total if quantity or unit price changed
        if (isset($data['quantity']) || isset($data['unit_price'])) {
            $data['quantity'] = $data['quantity'] ?? $sale->quantity;
            $data['unit_price'] = $data['unit_price'] ?? $sale->unit_price;
            $data['total_amount'] = $data['quantity'] * $data['unit_price'];
        }

        $sale->update($data);

        return response()->json([
            'message' => 'Sale updated successfully',
            'sale' => $sale
        ]);
    }

    /**
     * Remove the specified sale.
     */
    public function destroy($id)
    {
        $sale = Sale::find($id);
        
        if (!$sale) {
            return response()->json(['error' => 'Sale not found'], 404);
        }

        $sale->delete();

        return response()->json([
            'message' => 'Sale deleted successfully'
        ]);
    }

    /**
     * Get daily sales report.
     */
    public function dailyReport(Request $request)
    {
        $date = $request->get('date', today());
        $userId = $request->get('user_id');

        $sales = Sale::whereDate('sale_date', $date);

        if ($userId) {
            $sales->forUser($userId);
        }

        $sales = $sales->get();

        return response()->json([
            'date' => $date,
            'summary' => [
                'total_sales' => $sales->count(),
                'total_revenue' => $sales->sum('total_amount'),
                'total_profit' => $sales->sum(function ($sale) {
                    return $sale->profit;
                }),
            ],
            'sales' => $sales,
        ]);
    }

    /**
     * Get monthly sales report.
     */
    public function monthlyReport(Request $request)
    {
        $month = $request->get('month', now()->month);
        $year = $request->get('year', now()->year);
        $userId = $request->get('user_id');

        $startDate = Carbon::create($year, $month, 1)->startOfMonth();
        $endDate = Carbon::create($year, $month, 1)->endOfMonth();

        $sales = Sale::dateRange($startDate, $endDate);

        if ($userId) {
            $sales->forUser($userId);
        }

        $sales = $sales->get();

        return response()->json([
            'month' => $month,
            'year' => $year,
            'summary' => [
                'total_sales' => $sales->count(),
                'total_revenue' => $sales->sum('total_amount'),
                'total_profit' => $sales->sum(function ($sale) {
                    return $sale->profit;
                }),
                'average_sale' => $sales->count() > 0 ? $sales->sum('total_amount') / $sales->count() : 0,
            ],
            'sales' => $sales,
        ]);
    }

    /**
     * Store a Digit Ledger entry from a compact input string like 25*5000.
     */
    public function storeEntry(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'input_string' => ['required', 'string', 'regex:/^\s*(\d{2})\s*\*\s*(\d+(?:\.\d{1,2})?)\s*$/'],
        ]);

        if ($validator->fails()) {
            return response()->json([
                'errors' => $validator->errors(),
                'message' => 'Use the format 00*1000 through 99*1000.',
            ], 422);
        }

        preg_match('/^\s*(\d{2})\s*\*\s*(\d+(?:\.\d{1,2})?)\s*$/', $request->input_string, $matches);

        $record = DigitRecord::create([
            'input_string' => trim($request->input_string),
            'digit' => (int) $matches[1],
            'amount' => $matches[2],
            'recorded_at' => now(),
        ]);

        return response()->json([
            'message' => 'Digit record created successfully',
            'record' => $record,
        ], 201);
    }
}
