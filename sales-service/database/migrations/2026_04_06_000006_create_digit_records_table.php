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
        if (Schema::hasTable('digit_records')) {
            return;
        }

        Schema::create('digit_records', function (Blueprint $table) {
            $table->id();
            $table->string('input_string');
            $table->unsignedTinyInteger('digit');
            $table->decimal('amount', 12, 2);
            $table->timestamp('recorded_at');
            $table->timestamps();

            $table->index(['digit', 'recorded_at']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('digit_records');
    }
};
