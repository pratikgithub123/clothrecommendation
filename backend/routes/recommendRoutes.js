const express = require('express');
const router = express.Router();

// Import your recommendation controller
const { getRecommendations } = require('../controllers/recommendController');

// Define the POST route for recommendations
router.post('/', getRecommendations);

module.exports = router;
