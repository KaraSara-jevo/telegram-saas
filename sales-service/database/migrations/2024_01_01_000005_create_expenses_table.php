<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('expenses', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('user_id');
            $table->string('category');
            $table->text('description');
            $table->decimal('amount', 10, 2);
            $table->timestamp('expense_date');
            $table->string('receipt_number')->nullable();
            $table->string('vendor')->nullable();
            $table->string('payment_method')->nullable();
            $table->text('notes')->nullable();
            $table->timestamps();
            
            $table->index(['user_id', 'expense_date']);
            $table->index('category');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('expenses');
    }
};
