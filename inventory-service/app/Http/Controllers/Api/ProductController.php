<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Product;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class ProductController extends Controller
{
    /**
     * Display a listing of products.
     */
    public function index(Request $request)
    {
        $query = Product::query();

        // Filter by active status
        if ($request->has('is_active')) {
            $query->where('is_active', $request->boolean('is_active'));
        }

        // Filter by category
        if ($request->has('category')) {
            $query->where('category', $request->category);
        }

        // Show low stock products
        if ($request->boolean('low_stock')) {
            $query->lowStock();
        }

        // Search by name or SKU
        if ($request->has('search')) {
            $search = $request->search;
            $query->where(function ($q) use ($search) {
                $q->where('name', 'like', "%{$search}%")
                  ->orWhere('sku', 'like', "%{$search}%");
            });
        }

        $products = $query->get();

        return response()->json([
            'products' => $products,
            'low_stock_count' => Product::lowStock()->count(),
        ]);
    }

    /**
     * Store a newly created product.
     */
    public function store(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'name' => 'required|string|max:255',
            'description' => 'nullable|string',
            'cost_price' => 'required|numeric|min:0',
            'selling_price' => 'required|numeric|min:0',
            'stock_quantity' => 'required|integer|min:0',
            'min_stock_level' => 'required|integer|min:0',
            'sku' => 'required|string|max:100|unique:products,sku',
            'category' => 'nullable|string|max:100',
            'is_active' => 'boolean',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $product = Product::create($request->all());

        return response()->json([
            'message' => 'Product created successfully',
            'product' => $product
        ], 201);
    }

    /**
     * Display the specified product.
     */
    public function show($id)
    {
        $product = Product::find($id);
        
        if (!$product) {
            return response()->json(['error' => 'Product not found'], 404);
        }

        return response()->json([
            'product' => $product,
            'profit_margin' => $product->profit_margin,
            'stock_value' => $product->stock_value,
            'is_low_stock' => $product->isLowStock(),
        ]);
    }

    /**
     * Update the specified product.
     */
    public function update(Request $request, $id)
    {
        $product = Product::find($id);
        
        if (!$product) {
            return response()->json(['error' => 'Product not found'], 404);
        }

        $validator = Validator::make($request->all(), [
            'name' => 'string|max:255',
            'description' => 'nullable|string',
            'cost_price' => 'numeric|min:0',
            'selling_price' => 'numeric|min:0',
            'stock_quantity' => 'integer|min:0',
            'min_stock_level' => 'integer|min:0',
            'sku' => 'string|max:100|unique:products,sku,'.$id,
            'category' => 'nullable|string|max:100',
            'is_active' => 'boolean',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $product->update($request->all());

        return response()->json([
            'message' => 'Product updated successfully',
            'product' => $product
        ]);
    }

    /**
     * Remove the specified product.
     */
    public function destroy($id)
    {
        $product = Product::find($id);
        
        if (!$product) {
            return response()->json(['error' => 'Product not found'], 404);
        }

        $product->delete();

        return response()->json([
            'message' => 'Product deleted successfully'
        ]);
    }

    /**
     * Update product stock.
     */
    public function updateStock(Request $request, $id)
    {
        $product = Product::find($id);
        
        if (!$product) {
            return response()->json(['error' => 'Product not found'], 404);
        }

        $validator = Validator::make($request->all(), [
            'quantity' => 'required|integer',
            'operation' => 'required|in:add,subtract,set',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $quantity = $request->quantity;
        $operation = $request->operation;

        switch ($operation) {
            case 'add':
                $product->stock_quantity += $quantity;
                break;
            case 'subtract':
                $newQuantity = $product->stock_quantity - $quantity;
                if ($newQuantity < 0) {
                    return response()->json(['error' => 'Insufficient stock'], 400);
                }
                $product->stock_quantity = $newQuantity;
                break;
            case 'set':
                if ($quantity < 0) {
                    return response()->json(['error' => 'Stock quantity cannot be negative'], 400);
                }
                $product->stock_quantity = $quantity;
                break;
        }

        $product->save();

        return response()->json([
            'message' => 'Stock updated successfully',
            'product' => $product,
            'is_low_stock' => $product->isLowStock(),
        ]);
    }
}
