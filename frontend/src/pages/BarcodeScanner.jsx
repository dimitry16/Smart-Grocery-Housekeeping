// BarcodeScanner.jsx
  // Camera scanning via @zxing/browser, fallback to manual input
  // Lookup via Open Food Facts API, auto-fills AddItem form on match
  // Name: Zilin Xu
  // Date: 5/6/2026
                                                                                                                                                                           
  import { useEffect, useRef, useState } from "react";
  import { useNavigate } from "react-router-dom";
  import { BrowserMultiFormatReader } from "@zxing/browser";
  import { NotFoundException } from "@zxing/library";
  import { Button } from "@/components/ui/button";
                                                                                                                                                                           
  const OFF_API = "https://world.openfoodfacts.org/api/v0/product";
                                                                                                                                                                           
  async function lookupBarcode(barcode) {
    const response = await fetch(`${OFF_API}/${barcode}.json`);
    if (!response.ok) throw new Error("Lookup failed");
    const data = await response.json();
    if (data.status !== 1) return null; // product not found
                                                                                                                                                                           
    const p = data.product;
    return {
      name: p.product_name || p.product_name_en || "",
      brand: p.brands?.split(",")[0].trim() || "",
      category: p.categories?.split(",")[0].trim() || "",
      barcode,
    };
  }
                                                                                                                                                                           
  function ManualInput({ onSubmit, loading }) {
    const [value, setValue] = useSt
  ──── (210 lines hidden) ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 
  nded-br" />
                  </div>
                </div>
              )}
            </div>
            <p className="text-sm text-gray-500 text-center">
              Point your camera at a barcode
            </p>
                                                                                                                                                                           
            {cameraError && (
              <div className="rounded-md border border-yellow-300 bg-yellow-50 px-4 py-3 text-sm text-yellow-700">
                {cameraError}
              </div>
            )}
          </div>
        )}
                                                                                                                                                                           
        {/* Manual input */}
        {mode === "manual" && !result && (
          <ManualInput onSubmit={handleBarcode} loading={lookingUp} />
        )}
                                                                                                                                                                           
        {/* Looking up spinner */}
        {lookingUp && (
          <p className="text-sm text-gray-500 text-center animate-pulse">
            Looking up barcode...
          </p>
        )}
                                                                                                                                                                           
        {/* Lookup error */}
        {lookupError && (
          <div className="rounded-md border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-600">
            {lookupError}
          </div>
        )}
                                                                                                                                                                           
        {/* Result card */}
        {result && (
          <div className="rounded-lg border border-emerald-300 bg-emerald-50 p-5 space-y-4">
            <h2 className="text-lg font-semibold text-gray-900">Product Found</h2>
            <dl className="space-y-2 text-sm">
              <div className="flex gap-2">
                <dt className="font-medium text-gray-600 w-24">Name</dt>
                <dd className="text-gray-900">{result.name || "—"}</dd>
              </div>
              <div className="flex gap-2">
                <dt className="font-medium text-gray-600 w-24">Brand</dt>
                <dd className="text-gray-900">{result.brand || "—"}</dd>
              </div>
              <div className="flex gap-2">
                <dt className="font-medium text-gray-600 w-24">Category</dt>
                <dd className="text-gray-900">{result.category || "—"}</dd>
              </div>
              <div className="flex gap-2">
                <dt className="font-medium text-gray-600 w-24">Barcode</dt>
                <dd className="text-gray-900 font-mono">{result.barcode}</dd>
              </div>
            </dl>
            <div className="flex gap-3">
              <Button
                onClick={handleUseResult}
                className="bg-emerald-500 hover:bg-emerald-600 text-white"
              >
                Add This Item →
              </Button>
              <Button variant="outline" onClick={handleRescan}>
                Scan Again
              </Button>
            </div>
          </div>
        )}
      </div>
    );
  }
                                                                                                                                                                           
  export default BarcodeScanner;
