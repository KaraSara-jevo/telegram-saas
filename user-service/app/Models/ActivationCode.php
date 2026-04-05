<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ActivationCode extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'user_id',
        'code',
        'is_used',
        'expires_at',
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'user_id' => 'integer',
        'is_used' => 'boolean',
        'expires_at' => 'datetime',
    ];

    /**
     * Get the user that owns the activation code.
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    /**
     * Check if activation code is valid
     */
    public function isValid(): bool
    {
        return !$this->is_used && 
               (!$this->expires_at || $this->expires_at->isFuture());
    }
}
