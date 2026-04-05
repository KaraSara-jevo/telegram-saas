<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Expense;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Carbon\Carbon;

class ExpenseController extends Controller
{
    /**
     * Display a listing of expenses.
     */
    public function index(Request $request)
    {
        $query = Expense::with('user');

        // Filter by user
        if ($request->has('user_id')) {
            $query->forUser($request->user_id);
        }

        // Filter by date range
        if ($request->has('start_date') && $request->has('end_date')) {
            $query->dateRange($request->start_date, $request->end_date);
        }

        // Filter by category
        if ($request->has('category')) {
            $query->category($request->category);
        }

        // Filter by payment method
        if ($request->has('payment_method')) {
            $query->where('payment_method', $request->payment_method);
        }

        // Order by latest
        $query->orderBy('expense_date', 'desc');

        $expenses = $query->paginate($request->get('per_page', 15));

        return response()->json($expenses);
    }

    /**
     * Store a newly created expense.
     */
    public function store(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'user_id' => 'required|integer',
            'category' => 'required|string|max:50',
            'description' => 'required|string',
            'amount' => 'required|numeric|min:0',
            'expense_date' => 'nullable|date',
            'receipt_number' => 'nullable|string|max:100',
            'vendor' => 'nullable|string|max:255',
            'payment_method' => 'nullable|string|max:50',
            'notes' => 'nullable|string',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $data = $request->all();
        $data['expense_date'] = $data['expense_date'] ?? now();

        $expense = Expense::create($data);

        return response()->json([
            'message' => 'Expense created successfully',
            'expense' => $expense->load('user')
        ], 201);
    }

    /**
     * Display the specified expense.
     */
    public function show($id)
    {
        $expense = Expense::with('user')->find($id);
        
        if (!$expense) {
            return response()->json(['error' => 'Expense not found'], 404);
        }

        return response()->json(['expense' => $expense]);
    }

    /**
     * Update the specified expense.
     */
    public function update(Request $request, $id)
    {
        $expense = Expense::find($id);
        
        if (!$expense) {
            return response()->json(['error' => 'Expense not found'], 404);
        }

        $validator = Validator::make($request->all(), [
            'category' => 'string|max:50',
            'description' => 'string',
            'amount' => 'numeric|min:0',
            'expense_date' => 'date',
            'receipt_number' => 'nullable|string|max:100',
            'vendor' => 'nullable|string|max:255',
            'payment_method' => 'nullable|string|max:50',
            'notes' => 'nullable|string',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $expense->update($request->all());

        return response()->json([
            'message' => 'Expense updated successfully',
            'expense' => $expense->load('user')
        ]);
    }

    /**
     * Remove the specified expense.
     */
    public function destroy($id)
    {
        $expense = Expense::find($id);
        
        if (!$expense) {
            return response()->json(['error' => 'Expense not found'], 404);
        }

        $expense->delete();

        return response()->json([
            'message' => 'Expense deleted successfully'
        ]);
    }

    /**
     * Get expense categories.
     */
    public function categories()
    {
        return response()->json([
            'categories' => Expense::getCategories()
        ]);
    }

    /**
     * Get expense summary by category.
     */
    public function summary(Request $request)
    {
        $startDate = $request->get('start_date', Carbon::now()->startOfMonth());
        $endDate = $request->get('end_date', Carbon::now()->endOfMonth());
        $userId = $request->get('user_id');

        $query = Expense::dateRange($startDate, $endDate);
        
        if ($userId) {
            $query->forUser($userId);
        }

        $expenses = $query->get();

        $summary = $expenses->groupBy('category')->map(function ($categoryExpenses) {
            return [
                'total' => $categoryExpenses->sum('amount'),
                'count' => $categoryExpenses->count(),
                'average' => $categoryExpenses->avg('amount'),
            ];
        });

        return response()->json([
            'period' => [
                'start_date' => $startDate,
                'end_date' => $endDate,
            ],
            'total_expenses' => $expenses->sum('amount'),
            'by_category' => $summary,
        ]);
    }
}
