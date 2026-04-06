<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Sale extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'user_id', // Telegram user ID
        'product_id',
        'quantity',
        'unit_price',
        'total_amount',
        'payment_method',
        'customer_name',
        'customer_phone',
        'notes',
        'sale_date',
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'user_id' => 'integer',
        'product_id' => 'integer',
        'quantity' => 'integer',
        'unit_price' => 'decimal:2',
        'total_amount' => 'decimal:2',
        'sale_date' => 'datetime',
    ];

    /**
     * Get the user that made the sale.
     */
    public function user()
    {
        return $this->belongsTo(User::class, 'user_id', 'id');
    }

    /**
     * Get the product that was sold.
     */
    public function product()
    {
        return $this->belongsTo(Product::class);
    }

    /**
     * Get the profit for this sale.
     */
    public function getProfitAttribute(): float
    {
        if (!$this->relationLoaded('product') && !$this->product_id) {
            return 0;
        }

        if (!$this->product) {
            return 0;
        }
        
        $costPerUnit = $this->product->cost_price;
        $totalCost = $costPerUnit * $this->quantity;
        
        return $this->total_amount - $totalCost;
    }

    /**
     * Scope to get sales within a date range.
     */
    public function scopeDateRange($query, $startDate, $endDate)
    {
        return $query->whereBetween('sale_date', [$startDate, $endDate]);
    }

    /**
     * Scope to get sales for a specific user.
     */
    public function scopeForUser($query, $userId)
    {
        return $query->where('user_id', $userId);
    }

    /**
     * Scope to get sales for today.
     */
    public function scopeToday($query)
    {
        return $query->whereDate('sale_date', today());
    }

    /**
     * Scope to get sales for this month.
     */
    public function scopeThisMonth($query)
    {
        return $query->whereMonth('sale_date', now()->month)
                    ->whereYear('sale_date', now()->year);
    }
}
