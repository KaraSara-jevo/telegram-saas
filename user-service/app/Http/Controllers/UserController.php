<?php

namespace App\Http\Controllers;

use App\Models\User;

class UserController extends Controller
{
    /**
     * Return a lightweight user profile response.
     */
    public function profile($id)
    {
        $user = User::find($id);

        if (!$user) {
            return response()->json(['error' => 'User not found'], 404);
        }

        return response()->json([
            'id' => $user->id,
            'username' => $user->username,
            'shop_name' => $user->shop_name,
            'is_active' => $user->is_active,
            'subscription_end_date' => $user->subscription_end_date,
        ]);
    }
}
