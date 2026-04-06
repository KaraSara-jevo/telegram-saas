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
        Schema::table('users', function (Blueprint $table) {
            $table->string('email')->unique()->after('username');
            $table->string('password')->after('email');
            $table->bigInteger('telegram_user_id')->nullable()->after('subscription_end_date');
            $table->string('phone')->nullable()->after('telegram_user_id');
            $table->string('address')->nullable()->after('phone');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->dropColumn(['email', 'password', 'telegram_user_id', 'phone', 'address']);
        });
    }
};
