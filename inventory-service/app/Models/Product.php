<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Product extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'name',
        'description',
        'cost_price',
        'selling_price',
        'stock_quantity',
        'min_stock_level',
        'sku',
        'category',
        'is_active',
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'cost_price' => 'decimal:2',
        'selling_price' => 'decimal:2',
        'stock_quantity' => 'integer',
        'min_stock_level' => 'integer',
        'is_active' => 'boolean',
    ];

    /**
     * Get the profit margin for this product.
     */
    public function getProfitMarginAttribute(): float
    {
        if ($this->cost_price == 0) {
            return 0;
        }
        
        return (($this->selling_price - $this->cost_price) / $this->cost_price) * 100;
    }

    /**
     * Get the total value of current stock.
     */
    public function getStockValueAttribute(): float
    {
        return $this->cost_price * $this->stock_quantity;
    }

    /**
     * Check if stock is low.
     */
    public function isLowStock(): bool
    {
        return $this->stock_quantity <= $this->min_stock_level;
    }

    /**
     * Scope to get only active products.
     */
    public function scopeActive($query)
    {
        return $query->where('is_active', true);
    }

    /**
     * Scope to get products with low stock.
     */
    public function scopeLowStock($query)
    {
        return $query->whereRaw('stock_quantity <= min_stock_level');
    }
}
