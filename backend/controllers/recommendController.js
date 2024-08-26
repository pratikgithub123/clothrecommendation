const fs = require('fs');
const path = require('path');

let cosineSim, productIds;

// Load model data from JSON files
function loadModel() {
    try {
        cosineSim = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../model/cosine_sim.json'), 'utf8'));
        productIds = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../model/product_ids.json'), 'utf8'));
    } catch (error) {
        console.error('Error loading model:', error);
        throw error; // Re-throw error to be caught by your error handling middleware
    }
}

loadModel();

// Handle recommendation request
exports.getRecommendations = (req, res) => {
    try {
        const { purchase_history } = req.body;

        // Validate input
        if (!Array.isArray(purchase_history) || !purchase_history.every(id => typeof id === 'string')) {
            return res.status(400).json({ error: "Invalid input format. 'purchase_history' should be a list of strings." });
        }

        // Get indices of purchased products
        const indices = purchase_history.map(pid => productIds.indexOf(pid)).filter(idx => idx !== -1);

        if (indices.length === 0) {
            return res.json({ recommendations: [] });
        }

        // Calculate average similarity scores
        const avgSimScores = cosineSim.reduce((acc, scores, idx) => {
            if (indices.includes(idx)) {
                return acc.map((score, i) => score + scores[i]);
            }
            return acc;
        }, Array(cosineSim[0].length).fill(0)).map(score => score / indices.length);

        // Get top recommendations
        const recommendedIndices = avgSimScores
            .map((score, idx) => ({ idx, score }))
            .filter(({ idx }) => !indices.includes(idx)) // Exclude already purchased products
            .sort((a, b) => b.score - a.score) // Sort by score in descending order
            .slice(0, 5) // Get top 5 recommendations
            .map(({ idx }) => idx);

        const recommendations = recommendedIndices.map(idx => ({ product_id: productIds[idx] }));

        res.json({ recommendations });
    } catch (error) {
        console.error('Error in recommendation:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
};
