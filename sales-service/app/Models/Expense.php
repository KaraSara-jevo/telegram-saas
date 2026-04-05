<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Expense extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'user_id', // Telegram user ID
        'category',
        'description',
        'amount',
        'expense_date',
        'receipt_number',
        'vendor',
        'payment_method',
        'notes',
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'user_id' => 'integer',
        'amount' => 'decimal:2',
        'expense_date' => 'datetime',
    ];

    /**
     * Get the user that incurred the expense.
     */
    public function user()
    {
        return $this->belongsTo(User::class, 'user_id', 'id');
    }

    /**
     * Scope to get expenses within a date range.
     */
    public function scopeDateRange($query, $startDate, $endDate)
    {
        return $query->whereBetween('expense_date', [$startDate, $endDate]);
    }

    /**
     * Scope to get expenses for a specific user.
     */
    public function scopeForUser($query, $userId)
    {
        return $query->where('user_id', $userId);
    }

    /**
     * Scope to get expenses by category.
     */
    public function scopeCategory($query, $category)
    {
        return $query->where('category', $category);
    }

    /**
     * Scope to get expenses for today.
     */
    public function scopeToday($query)
    {
        return $query->whereDate('expense_date', today());
    }

    /**
     * Scope to get expenses for this month.
     */
    public function scopeThisMonth($query)
    {
        return $query->whereMonth('expense_date', now()->month)
                    ->whereYear('expense_date', now()->year);
    }

    /**
     * Get common expense categories.
     */
    public static function getCategories(): array
    {
        return [
            'rent',
            'utilities',
            'salaries',
            'marketing',
            'supplies',
            'maintenance',
            'insurance',
            'taxes',
            'transportation',
            'other',
        ];
    }
}
