<?php

namespace App\Http\Controllers;

use App\Models\User;
use App\Models\ActivationCode;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Str;

class AuthController extends Controller
{
    /**
     * Login user with email and password
     */
    public function login(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'email' => 'required|email',
            'password' => 'required|string|min:6',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'message' => 'Validation failed',
                'errors' => $validator->errors()
            ], 422);
        }

        $user = User::where('email', $request->email)->first();

        if (!$user || !Hash::check($request->password, $user->password)) {
            return response()->json([
                'success' => false,
                'message' => 'Invalid credentials'
            ], 401);
        }

        if (!$user->hasActiveSubscription()) {
            return response()->json([
                'success' => false,
                'message' => 'Subscription expired or inactive',
                'requires_subscription' => true
            ], 403);
        }

        // Create token
        $token = $user->createToken('auth_token')->plainTextToken;

        return response()->json([
            'success' => true,
            'message' => 'Login successful',
            'data' => [
                'user' => $user,
                'token' => $token,
                'subscription' => [
                    'is_active' => $user->hasActiveSubscription(),
                    'end_date' => $user->subscription_end_date
                ]
            ]
        ]);
    }

    /**
     * Verify subscription code
     */
    public function verifySubscriptionCode(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'code' => 'required|string',
            'email' => 'required|email',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'message' => 'Validation failed',
                'errors' => $validator->errors()
            ], 422);
        }

        $activationCode = ActivationCode::where('code', $request->code)
            ->where('is_used', false)
            ->where('expires_at', '>', now())
            ->with('user')
            ->first();

        if (!$activationCode) {
            return response()->json([
                'success' => false,
                'message' => 'Invalid or expired activation code'
            ], 404);
        }

        $user = $activationCode->user;

        if ($user->email !== $request->email) {
            return response()->json([
                'success' => false,
                'message' => 'Activation code does not belong to this email'
            ], 403);
        }

        // Activate subscription
        $user->update([
            'is_active' => true,
            'subscription_end_date' => now()->addMonths(1) // Default 1 month
        ]);

        // Mark code as used
        $activationCode->update(['is_used' => true]);

        return response()->json([
            'success' => true,
            'message' => 'Subscription activated successfully',
            'data' => [
                'user' => $user,
                'subscription' => [
                    'is_active' => $user->hasActiveSubscription(),
                    'end_date' => $user->subscription_end_date
                ]
            ]
        ]);
    }

    /**
     * Telegram authentication
     */
    public function telegramAuth(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'telegram_user_id' => 'required|integer',
            'code' => 'required|string',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'message' => 'Validation failed',
                'errors' => $validator->errors()
            ], 422);
        }

        $user = User::where('telegram_user_id', $request->telegram_user_id)->first();

        if (!$user) {
            return response()->json([
                'success' => false,
                'message' => 'User not found'
            ], 404);
        }

        if (!$user->hasActiveSubscription()) {
            return response()->json([
                'success' => false,
                'message' => 'Subscription expired or inactive',
                'requires_subscription' => true
            ], 403);
        }

        // Create token
        $token = $user->createToken('telegram_auth')->plainTextToken;

        return response()->json([
            'success' => true,
            'message' => 'Telegram authentication successful',
            'data' => [
                'user' => $user,
                'token' => $token,
                'subscription' => [
                    'is_active' => $user->hasActiveSubscription(),
                    'end_date' => $user->subscription_end_date
                ]
            ]
        ]);
    }

    /**
     * Register new user
     */
    public function register(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'username' => 'required|string|max:255|unique:users',
            'email' => 'required|email|unique:users',
            'password' => 'required|string|min:6|confirmed',
            'shop_name' => 'required|string|max:255',
            'phone' => 'nullable|string|max:20',
            'address' => 'nullable|string|max:500',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'message' => 'Validation failed',
                'errors' => $validator->errors()
            ], 422);
        }

        $user = User::create([
            'username' => $request->username,
            'email' => $request->email,
            'password' => Hash::make($request->password),
            'shop_name' => $request->shop_name,
            'phone' => $request->phone,
            'address' => $request->address,
            'is_active' => false, // Inactive until subscription is activated
        ]);

        return response()->json([
            'success' => true,
            'message' => 'User registered successfully',
            'data' => [
                'user' => $user,
                'next_step' => 'Please activate your subscription with an activation code'
            ]
        ], 201);
    }

    /**
     * Logout user
     */
    public function logout(Request $request)
    {
        $request->user()->currentAccessToken()->delete();

        return response()->json([
            'success' => true,
            'message' => 'Logout successful'
        ]);
    }

    /**
     * Get user profile
     */
    public function profile(Request $request)
    {
        return response()->json([
            'success' => true,
            'data' => [
                'user' => $request->user(),
                'subscription' => [
                    'is_active' => $request->user()->hasActiveSubscription(),
                    'end_date' => $request->user()->subscription_end_date
                ]
            ]
        ]);
    }

    /**
     * Update user profile
     */
    public function updateProfile(Request $request)
    {
        $user = $request->user();

        $validator = Validator::make($request->all(), [
            'shop_name' => 'sometimes|string|max:255',
            'phone' => 'sometimes|string|max:20',
            'address' => 'sometimes|string|max:500',
            'telegram_user_id' => 'sometimes|integer|unique:users,telegram_user_id,' . $user->id,
        ]);

        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'message' => 'Validation failed',
                'errors' => $validator->errors()
            ], 422);
        }

        $user->update($request->only([
            'shop_name',
            'phone',
            'address',
            'telegram_user_id'
        ]));

        return response()->json([
            'success' => true,
            'message' => 'Profile updated successfully',
            'data' => ['user' => $user]
        ]);
    }
}
