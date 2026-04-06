<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class UserController extends Controller
{
    public function index()
    {
        return response()->json(User::orderBy('id')->get());
    }

    public function store(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'id' => 'required|integer|unique:users,id',
            'username' => 'required|string|max:255|unique:users,username',
            'shop_name' => 'required|string|max:255',
            'is_active' => 'boolean',
            'subscription_end_date' => 'nullable|date',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $user = User::create($request->only([
            'id',
            'username',
            'shop_name',
            'is_active',
            'subscription_end_date',
        ]));

        return response()->json([
            'message' => 'User created successfully',
            'user' => $user,
        ], 201);
    }

    public function show($id)
    {
        $user = User::with('activationCodes')->find($id);

        if (!$user) {
            return response()->json(['error' => 'User not found'], 404);
        }

        return response()->json($user);
    }

    public function update(Request $request, $id)
    {
        $user = User::find($id);

        if (!$user) {
            return response()->json(['error' => 'User not found'], 404);
        }

        $validator = Validator::make($request->all(), [
            'username' => 'sometimes|string|max:255|unique:users,username,'.$id,
            'shop_name' => 'sometimes|string|max:255',
            'is_active' => 'sometimes|boolean',
            'subscription_end_date' => 'nullable|date',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $user->update($request->only([
            'username',
            'shop_name',
            'is_active',
            'subscription_end_date',
        ]));

        return response()->json([
            'message' => 'User updated successfully',
            'user' => $user,
        ]);
    }

    public function destroy($id)
    {
        $user = User::find($id);

        if (!$user) {
            return response()->json(['error' => 'User not found'], 404);
        }

        $user->delete();

        return response()->json([
            'message' => 'User deleted successfully',
        ]);
    }
}
