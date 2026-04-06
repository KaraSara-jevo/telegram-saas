<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\User;
use App\Models\ActivationCode;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Carbon\Carbon;

class SubscriptionController extends Controller
{
    /**
     * Display a listing of subscriptions.
     */
    public function index()
    {
        try {
            $users = User::with('activationCodes')->get();
            return response()->json($users);
        } catch (\Exception $e) {
            // Fallback to without relationship if there's an issue
            $users = User::get();
            return response()->json($users);
        }
    }

    /**
     * Store a new subscription or activation code.
     */
    public function store(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'user_id' => 'required|integer|exists:users,id',
            'subscription_days' => 'nullable|integer|min:1|max:365',
            'code' => 'nullable|string|unique:activation_codes,code',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $user = User::find($request->user_id);

        if ($request->has('subscription_days')) {
            // Extend subscription
            $currentEndDate = $user->subscription_end_date;
            $newEndDate = $currentEndDate ? 
                $currentEndDate->addDays($request->subscription_days) : 
                Carbon::now()->addDays($request->subscription_days);
                
            $user->subscription_end_date = $newEndDate;
            $user->is_active = true;
            $user->save();

            return response()->json([
                'message' => 'Subscription extended successfully',
                'user' => $user
            ]);
        } elseif ($request->has('code')) {
            // Create activation code
            $activationCode = ActivationCode::create([
                'user_id' => $user->id,
                'code' => $request->code,
                'expires_at' => Carbon::now()->addDays(30),
            ]);

            return response()->json([
                'message' => 'Activation code created successfully',
                'activation_code' => $activationCode
            ]);
        }

        return response()->json(['error' => 'No valid action provided'], 400);
    }

    /**
     * Display the specified subscription.
     */
    public function show($id)
    {
        $user = User::with('activationCodes')->find($id);
        
        if (!$user) {
            return response()->json(['error' => 'User not found'], 404);
        }

        return response()->json([
            'user' => $user,
            'has_active_subscription' => $user->hasActiveSubscription()
        ]);
    }

    /**
     * Update the subscription.
     */
    public function update(Request $request, $id)
    {
        $user = User::find($id);
        
        if (!$user) {
            return response()->json(['error' => 'User not found'], 404);
        }

        $validator = Validator::make($request->all(), [
            'is_active' => 'boolean',
            'subscription_end_date' => 'date|nullable',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $user->update($request->only(['is_active', 'subscription_end_date']));

        return response()->json([
            'message' => 'Subscription updated successfully',
            'user' => $user
        ]);
    }

    /**
     * Activate subscription using code.
     */
    public function activate(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'code' => 'required|string',
            'user_id' => 'required|integer|exists:users,id',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $activationCode = ActivationCode::where('code', $request->code)
            ->where('user_id', $request->user_id)
            ->first();

        if (!$activationCode || !$activationCode->isValid()) {
            return response()->json(['error' => 'Invalid or expired activation code'], 400);
        }

        $user = User::find($request->user_id);
        $user->is_active = true;
        $user->subscription_end_date = Carbon::now()->addDays(30);
        $user->save();

        $activationCode->is_used = true;
        $activationCode->save();

        return response()->json([
            'message' => 'Subscription activated successfully',
            'user' => $user
        ]);
    }
}
