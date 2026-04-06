<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Facades\Hash;

class AuthController extends Controller
{
    /**
     * Authenticate Telegram user and return JWT token
     */
    public function authenticateTelegram(Request $request)
    {
        // Try multiple ways to get JSON data
        $jsonData = $request->json()->all();
        if (empty($jsonData)) {
            $content = $request->getContent();
            if (!empty($content)) {
                $jsonData = json_decode($content, true);
            }
        }
        if (empty($jsonData)) {
            $jsonData = $request->all();
        }
        
        // Debug: Log what we received
        // \Log::info('Auth request data: ' . json_encode($jsonData));
        // \Log::info('Request content:', $request->getContent());
        
        $validator = Validator::make($jsonData, [
            'telegram_user_id' => 'required|integer',
            'username' => 'nullable|string|max:255',
            'first_name' => 'nullable|string|max:255',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $telegramUserId = $jsonData['telegram_user_id'];
        
        // Find or create user
        $user = User::find($telegramUserId);
        
        if (!$user) {
            // Create new user for Telegram
            $user = User::create([
                'id' => $telegramUserId,
                'username' => $jsonData['username'] ?? 'user_' . $telegramUserId,
                'shop_name' => $jsonData['first_name'] . "'s Shop",
                'is_active' => false, // Require subscription activation
                'subscription_end_date' => null,
            ]);
        }

        // Generate JWT token (simple implementation)
        $token = $this->generateJWT($user);

        return response()->json([
            'user' => [
                'id' => $user->id,
                'username' => $user->username,
                'shop_name' => $user->shop_name,
                'is_active' => $user->is_active,
                'subscription_end_date' => $user->subscription_end_date,
            ],
            'token' => $token,
            'expires_in' => 3600, // 1 hour
        ]);
    }

    /**
     * Simple JWT generation (for production, use jwt-auth package)
     */
    private function generateJWT($user)
    {
        $payload = [
            'sub' => $user->id,
            'iat' => time(),
            'exp' => time() + 3600, // 1 hour expiration
            'iss' => env('APP_NAME', 'telegram-saas'),
        ];

        // Simple base64 encoding (use proper JWT library in production)
        $header = json_encode(['typ' => 'JWT', 'alg' => 'HS256']);
        $header = base64_encode($header);
        
        $payload = base64_encode(json_encode($payload));
        $signature = hash_hmac('sha256', $header . "." . $payload, env('JWT_SECRET', 'your-secret-key'), true);
        $signature = base64_encode($signature);

        return implode('.', [$header, $payload, $signature]);
    }
}
