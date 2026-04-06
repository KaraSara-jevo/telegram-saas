<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class DigitRecord extends Model
{
    use HasFactory;

    protected $fillable = [
        'input_string',
        'digit',
        'amount',
        'recorded_at',
    ];

    protected $casts = [
        'digit' => 'integer',
        'amount' => 'decimal:2',
        'recorded_at' => 'datetime',
    ];
}
