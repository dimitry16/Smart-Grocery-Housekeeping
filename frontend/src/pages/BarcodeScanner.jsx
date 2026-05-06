// BarcodeScanner.jsx
// Name: Zilin Xu
// Date: 5/6/2026
// Camera scanning via @zxing/browser, fallback to manual input
// Lookup via Open Food Facts API, auto-fills AddItem form on match

import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { BrowserMultiFormatReader, NotFoundException } from "@zxing/browser";
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
  const [value, setValue] = useState("");

  function handleKey(e) {
    if (e.key === "Enter" && value.trim()) onSubmit(value.trim());
  }

  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-gray-700">Enter barcode manually</label>
      <div className="flex gap-2">
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKey}
          placeholder="e.g. 742365008412"
          className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400"
        />
        <Button
          onClick={() => value.trim() && onSubmit(value.trim())}
          disabled={loading || !value.trim()}
          className="bg-emerald-500 hover:bg-emerald-600 text-white"
        >
          {loading ? "Looking up..." : "Look Up"}
        </Button>
      </div>
    </div>
  );
}

function BarcodeScanner() {
  const navigate = useNavigate();
  const videoRef = useRef(null);
  const readerRef = useRef(null);

  const [mode, setMode] = useState("camera"); // "camera" | "manual"
  const [scanning, setScanning] = useState(false);
  const [lookingUp, setLookingUp] = useState(false);
  const [cameraError, setCameraError] = useState(null);
  const [lookupError, setLookupError] = useState(null);
  const [result, setResult] = useState(null); // found product

  // Start camera scanning
  useEffect(() => {
    if (mode !== "camera") return;

    const reader = new BrowserMultiFormatReader();
    readerRef.current = reader;
    setScanning(true);
    setCameraError(null);

    reader
      .decodeFromVideoDevice(undefined, videoRef.current, (res, err) => {
        if (res) {
          stopCamera();
          handleBarcode(res.getText());
        }
        if (err && !(err instanceof NotFoundException)) {
          // NotFoundException just means no barcode in frame yet — ignore
          console.error("Scanner error:", err);
        }
      })
      .catch((err) => {
        setCameraError(
          err?.message?.includes("Permission")
            ? "Camera permission denied. Please allow camera access or use manual input."
            : "Could not start camera. Try manual input instead."
        );
        setScanning(false);
        setMode("manual");
      });

    return () => stopCamera();
  }, [mode]);

  function stopCamera() {
    if (readerRef.current) {
      try { BrowserMultiFormatReader.releaseAllStreams(); } catch (_) {}
    }
    setScanning(false);
  }

  async function handleBarcode(barcode) {
    setLookupError(null);
    setLookingUp(true);
    try {
      const product = await lookupBarcode(barcode);
      if (product) {
        setResult(product);
      } else {
        // Not in Open Food Facts — go to AddItem pre-filled with just the barcode
        navigate("/additem", { state: { barcode } });
      }
    } catch {
      setLookupError("Could not reach Open Food Facts. You can still add the item manually.");
      setResult(null);
    } finally {
      setLookingUp(false);
    }
  }

  function handleUseResult() {
    navigate("/additem", { state: result });
  }

  function handleRescan() {
    setResult(null);
    setLookupError(null);
    if (mode === "camera") setMode(""); // force useEffect re-run
    setTimeout(() => setMode("camera"), 50);
  }

  return (
    <div className="p-6 max-w-lg mx-auto space-y-6">
      <div className="flex items-center gap-3">
        <button
          onClick={() => navigate(-1)}
          className="text-gray-400 hover:text-gray-700 transition-colors text-lg"
        >
          ←
        </button>
        <h1 className="text-3xl font-semibold text-gray-900">Scan Barcode</h1>
      </div>

      {/* Mode toggle */}
      <div className="flex gap-2">
        <button
          onClick={() => { setResult(null); setLookupError(null); setMode("camera"); }}
          className={`px-4 py-2 rounded-md text-sm font-medium border transition-colors ${
            mode === "camera"
              ? "bg-emerald-500 text-white border-emerald-500"
              : "bg-white text-gray-600 border-gray-300 hover:bg-gray-50"
          }`}
        >
          📷 Camera
        </button>
        <button
          onClick={() => { stopCamera(); setResult(null); setLookupError(null); setMode("manual"); }}
          className={`px-4 py-2 rounded-md text-sm font-medium border transition-colors ${
            mode === "manual"
              ? "bg-emerald-500 text-white border-emerald-500"
              : "bg-white text-gray-600 border-gray-300 hover:bg-gray-50"
          }`}
        >
          ⌨️ Manual
        </button>
      </div>

      {/* Camera view */}
      {mode === "camera" && !result && (
        <div className="space-y-3">
          <div className="relative rounded-lg overflow-hidden border border-gray-300 bg-black aspect-video">
            <video ref={videoRef} className="w-full h-full object-cover" />
            {scanning && (
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                {/* Scanning reticle */}
                <div className="w-56 h-36 border-2 border-emerald-400 rounded-md opacity-80">
                  <div className="absolute top-0 left-0 w-5 h-5 border-t-4 border-l-4 border-emerald-400 rounded-tl" />
                  <div className="absolute top-0 right-0 w-5 h-5 border-t-4 border-r-4 border-emerald-400 rounded-tr" />
                  <div className="absolute bottom-0 left-0 w-5 h-5 border-b-4 border-l-4 border-emerald-400 rounded-bl" />
                  <div className="absolute bottom-0 right-0 w-5 h-5 border-b-4 border-r-4 border-emerald-400 rounded-br" />
                </div>
              </div>
            )}
          </div>
          <p className="text-sm text-gray-500 text-center">Point your camera at a barcode</p>

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
        <p className="text-sm text-gray-500 text-center animate-pulse">Looking up barcode...</p>
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
