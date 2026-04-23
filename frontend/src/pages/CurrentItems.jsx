// CurrentItems.jsx — fetch all, edit (PATCH), delete (DELETE)
// Name: Zilin Xu
// Date: 4/22/2026

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";

const BASE_URL = `${import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"}/v1/food-items`;

const CATEGORIES = [
  "Dairy", "Bakery", "Produce", "Seafood", "Meat",
  "Oils & Condiments", "Beverages", "Snacks", "Frozen", "Other",
];

function EditModal({ item, onClose, onSave }) {
  const [form, setForm] = useState({
    name: item.name ?? "",
    brand: item.brand ?? "",
    barcode: item.barcode ?? "",
    category: item.category ?? "",
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);

    const payload = {
      name: form.name || undefined,
      brand: form.brand || null,
      barcode: form.barcode || null,
      category: form.category || null,
    };

    try {
      const response = await fetch(`${BASE_URL}/${item.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data?.detail ?? `Error ${response.status}`);
      }

      const updated = await response.json();
      onSave(updated);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md p-6 space-y-4">
        <h2 className="text-xl font-semibold text-gray-900">Edit Item</h2>

        {error && (
          <div className="rounded-md border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-600">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1">
            <label className="text-sm font-medium text-gray-700" htmlFor="edit-name">
              Name <span className="text-red-500">*</span>
            </label>
            <input
              id="edit-name"
              name="name"
              type="text"
              required
              maxLength={50}
              value={form.name}
              onChange={handleChange}
              className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400"
            />
          </div>

          <div className="space-y-1">
            <label className="text-sm font-medium text-gray-700" htmlFor="edit-brand">
              Brand
            </label>
            <input
              id="edit-brand"
              name="brand"
              type="text"
              maxLength={30}
              value={form.brand}
              onChange={handleChange}
              className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400"
            />
          </div>

          <div className="space-y-1">
            <label className="text-sm font-medium text-gray-700" htmlFor="edit-barcode">
              Barcode
            </label>
            <input
              id="edit-barcode"
              name="barcode"
              type="text"
              maxLength={100}
              value={form.barcode}
              onChange={handleChange}
              className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400"
            />
          </div>

          <div className="space-y-1">
            <label className="text-sm font-medium text-gray-700" htmlFor="edit-category">
              Category
            </label>
            <select
              id="edit-category"
              name="category"
              value={form.category}
              onChange={handleChange}
              className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 bg-white"
            >
              <option value="">— Select a category —</option>
              {CATEGORIES.map((cat) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>

          <div className="flex gap-3 pt-2">
            <Button
              type="submit"
              disabled={submitting}
              className="bg-emerald-500 hover:bg-emerald-600 text-white"
            >
              {submitting ? "Saving..." : "Save Changes"}
            </Button>
            <Button type="button" variant="outline" onClick={onClose} disabled={submitting}>
              Cancel
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

function DeleteConfirmModal({ item, onClose, onConfirm, deleting }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-sm p-6 space-y-4">
        <h2 className="text-xl font-semibold text-gray-900">Delete Item</h2>
        <p className="text-sm text-gray-600">
          Are you sure you want to delete <span className="font-medium">{item.name}</span>? This cannot be undone.
        </p>
        <div className="flex gap-3">
          <Button
            onClick={onConfirm}
            disabled={deleting}
            className="bg-red-500 hover:bg-red-600 text-white"
          >
            {deleting ? "Deleting..." : "Delete"}
          </Button>
          <Button variant="outline" onClick={onClose} disabled={deleting}>
            Cancel
          </Button>
        </div>
      </div>
    </div>
  );
}

function CurrentItems() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingItem, setEditingItem] = useState(null);
  const [deletingItem, setDeletingItem] = useState(null);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    async function fetchItems() {
      try {
        const response = await fetch(BASE_URL);
        if (!response.ok) throw new Error(`Error ${response.status}`);
        const data = await response.json();
        setItems(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchItems();
  }, []);

  function handleSave(updated) {
    setItems((prev) => prev.map((i) => (i.id === updated.id ? updated : i)));
    setEditingItem(null);
  }

  async function handleDelete() {
    setDeleting(true);
    try {
      const response = await fetch(`${BASE_URL}/${deletingItem.id}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error(`Error ${response.status}`);
      setItems((prev) => prev.filter((i) => i.id !== deletingItem.id));
      setDeletingItem(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setDeleting(false);
    }
  }

  if (loading) {
    return <div className="p-6 text-center text-gray-500">Loading items...</div>;
  }

  if (error) {
    return <div className="p-6 text-center text-red-500">Failed to load items: {error}</div>;
  }

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <h1 className="text-3xl font-semibold text-gray-900">All Food Items</h1>

      <div className="rounded-lg border bg-white">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-gray-600 uppercase text-xs">
            <tr>
              <th className="px-4 py-3 text-left">Name</th>
              <th className="px-4 py-3 text-left">Brand</th>
              <th className="px-4 py-3 text-left">Category</th>
              <th className="px-4 py-3 text-left">Barcode</th>
              <th className="px-4 py-3 text-left">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {items.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-center text-gray-400">
                  No items found.
                </td>
              </tr>
            ) : (
              items.map((item) => (
                <tr key={item.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium">{item.name}</td>
                  <td className="px-4 py-3 text-gray-500">{item.brand ?? "—"}</td>
                  <td className="px-4 py-3">{item.category ?? "—"}</td>
                  <td className="px-4 py-3">{item.barcode ?? "—"}</td>
                  <td className="px-4 py-3">
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => setEditingItem(item)}
                      >
                        Edit
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        className="text-red-500 border-red-300 hover:bg-red-50"
                        onClick={() => setDeletingItem(item)}
                      >
                        Delete
                      </Button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {editingItem && (
        <EditModal
          item={editingItem}
          onClose={() => setEditingItem(null)}
          onSave={handleSave}
        />
      )}

      {deletingItem && (
        <DeleteConfirmModal
          item={deletingItem}
          onClose={() => setDeletingItem(null)}
          onConfirm={handleDelete}
          deleting={deleting}
        />
      )}
    </div>
  );
}

export default CurrentItems;
