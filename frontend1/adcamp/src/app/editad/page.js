'use client';

import React, { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { adGenerationApi } from '../services/api';

const EditAdContent = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const id = searchParams.get('id');
  const [adData, setAdData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [editedData, setEditedData] = useState({
    product: '',
    targetAudience: '',
    adGoal: '',
    topFeature: '',
    callToAction: ''
  });

  useEffect(() => {
    const fetchData = async () => {
      if (id) {
        setIsLoading(true);
        setError(null);
        try {
          const adDetails = await fetchAdDetails(id);
          setAdData(adDetails);
          setEditedData(adDetails);
        } catch (error) {
          setError(error.response?.data?.message || 'Error fetching ad details');
          console.error('Error fetching ad details:', error);
        } finally {
          setIsLoading(false);
        }
      }
    };
    fetchData();
  }, [id]);

  const handleEditChange = (e) => {
    setEditedData({ ...editedData, [e.target.name]: e.target.value });
  };

  const handleSaveChanges = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      await adGenerationApi.saveAdChanges(id, editedData);
      router.push('/dashboard'); // or wherever you want to redirect after saving
    } catch (error) {
      setError(error.response?.data?.message || 'Error saving changes');
      console.error('Error saving ad changes:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (!id) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
        <p className="text-red-600">No ad ID provided.</p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      {adData ? (
        <>
          <h2 className="text-2xl font-bold mb-6">Edit Your Ad</h2>
          <form onSubmit={handleSaveChanges} className="space-y-6">
            {Object.entries(editedData).map(([key, value]) => (
              key !== 'id' && (
                <div key={key} className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">
                    {key.charAt(0).toUpperCase() + key.slice(1).replace(/([A-Z])/g, ' $1')}:
                  </label>
                  <input
                    type="text"
                    name={key}
                    value={value}
                    onChange={handleEditChange}
                    className="block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                    disabled={isLoading}
                  />
                </div>
              )
            ))}

            <div className="flex justify-end space-x-4">
              <button
                type="button"
                onClick={() => router.back()}
                className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                disabled={isLoading}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                disabled={isLoading}
              >
                {isLoading ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </form>
        </>
      ) : (
        <p className="text-gray-500">Loading ad details...</p>
      )}
    </div>
  );
};

const EditAd = () => {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    }>
      <EditAdContent />
    </Suspense>
  );
};

export default EditAd;