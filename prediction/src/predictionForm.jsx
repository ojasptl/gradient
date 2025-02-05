import React, { useState } from 'react';
import axios from 'axios';

const PredictionForm = () => {
  const [formData, setFormData] = useState({
    bedrooms: '',
    bathrooms: '',
    sqft_living: '',
    sqft_lot: '',
    floors: '',
    waterfront: '',
    condition: '',
  });

  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('https://react-theb.onrender.com/', {
        bedrooms: parseFloat(formData.bedrooms),
        bathrooms: parseFloat(formData.bathrooms),
        sqft_living: parseFloat(formData.sqft_living),
        sqft_lot: parseFloat(formData.sqft_lot),
        floors: parseFloat(formData.floors),
        waterfront: parseFloat(formData.waterfront),
        condition: parseFloat(formData.condition),
      });
      setPrediction(response.data);
      setError(null);
    } catch (err) {
      console.error('Prediction error details:', err.response || err.message);
      setError('An error occurred while fetching the prediction.');
      setPrediction(null);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        {Object.keys(formData).map((key) => (
          <div key={key}>
            <label>
              {key}:
              <input
                type="number"
                step="any"
                name={key}
                value={formData[key]}
                onChange={handleChange}
                required
              />
            </label>
          </div>
        ))}
        <button type="submit">Get Prediction</button>
      </form>
      {prediction && (
        <div>
          <h2>Prediction Result:</h2>
          <pre>{JSON.stringify(prediction, null, 2)}</pre>
        </div>
      )}
      {error && <p>{error}</p>}
    </div>
  );
};

export default PredictionForm;
