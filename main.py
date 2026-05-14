from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
from supabase import create_client, Client

# --- Environment Variables ---
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://xmoumwwedkkndwcofeec.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_9pM1RU0SuY0uyvmMna222Q_9-27Gs5j")

# Initialize Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Movie Review API")

# --- Data Model ---
class Review(BaseModel):
    id: int
    movie: str
    rating: float
    comment: str

# --- SERVE UI ---
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Movie Review Manager</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            header {
                text-align: center;
                color: white;
                margin-bottom: 40px;
            }
            
            header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            .main-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-bottom: 40px;
            }
            
            @media (max-width: 968px) {
                .main-grid {
                    grid-template-columns: 1fr;
                }
            }
            
            .card {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            
            .card h2 {
                color: #667eea;
                margin-bottom: 20px;
                font-size: 1.8em;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }
            
            .form-group {
                margin-bottom: 15px;
                display: flex;
                flex-direction: column;
            }
            
            label {
                font-weight: 600;
                color: #333;
                margin-bottom: 5px;
                font-size: 0.95em;
            }
            
            input, textarea {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 1em;
                font-family: inherit;
                transition: border-color 0.3s;
            }
            
            input:focus, textarea:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            textarea {
                resize: vertical;
                min-height: 100px;
            }
            
            .button-group {
                display: flex;
                gap: 10px;
                margin-top: 20px;
            }
            
            button {
                flex: 1;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .btn-primary {
                background: #667eea;
                color: white;
            }
            
            .btn-primary:hover {
                background: #5568d3;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            .btn-secondary {
                background: #f0f0f0;
                color: #333;
                border: 2px solid #667eea;
            }
            
            .btn-secondary:hover {
                background: #667eea;
                color: white;
            }
            
            .btn-danger {
                background: #ff6b6b;
                color: white;
                flex: 0.5;
            }
            
            .btn-danger:hover {
                background: #ff5252;
            }
            
            .reviews-section {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                grid-column: 1 / -1;
            }
            
            .reviews-section h2 {
                color: #667eea;
                margin-bottom: 20px;
                font-size: 1.8em;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }
            
            .review-list {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
            }
            
            .review-card {
                background: #f8f9fa;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 20px;
                transition: all 0.3s;
            }
            
            .review-card:hover {
                border-color: #667eea;
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
                transform: translateY(-3px);
            }
            
            .review-id {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 5px 10px;
                border-radius: 20px;
                font-size: 0.8em;
                font-weight: 600;
                margin-bottom: 10px;
            }
            
            .review-movie {
                font-size: 1.5em;
                font-weight: 700;
                color: #333;
                margin-bottom: 8px;
            }
            
            .review-rating {
                display: flex;
                align-items: center;
                margin-bottom: 10px;
                gap: 5px;
            }
            
            .stars {
                color: #ffc107;
                font-size: 1.2em;
            }
            
            .rating-value {
                background: #ffc107;
                color: white;
                padding: 2px 8px;
                border-radius: 5px;
                font-weight: 600;
                font-size: 0.9em;
            }
            
            .review-comment {
                color: #666;
                font-size: 0.95em;
                margin-bottom: 15px;
                line-height: 1.5;
            }
            
            .review-actions {
                display: flex;
                gap: 10px;
            }
            
            .btn-edit {
                flex: 1;
                background: #4ecdc4;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s;
            }
            
            .btn-edit:hover {
                background: #45b7b0;
            }
            
            .btn-delete {
                flex: 1;
                background: #ff6b6b;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s;
            }
            
            .btn-delete:hover {
                background: #ff5252;
            }
            
            .message {
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                font-weight: 600;
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 2000;
                animation: slideIn 0.3s ease-out;
            }
            
            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            .success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            
            .error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            
            .empty-state {
                text-align: center;
                padding: 40px;
                color: #999;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🎬 Movie Review Manager</h1>
                <p>Manage your movie reviews with ease</p>
            </header>
            
            <div class="main-grid">
                <!-- CREATE REVIEW -->
                <div class="card">
                    <h2>➕ Create Review</h2>
                    <form id="createForm">
                        <div class="form-group">
                            <label for="createId">Review ID:</label>
                            <input type="number" id="createId" placeholder="e.g., 1" required>
                        </div>
                        <div class="form-group">
                            <label for="createMovie">Movie Name:</label>
                            <input type="text" id="createMovie" placeholder="e.g., Inception" required>
                        </div>
                        <div class="form-group">
                            <label for="createRating">Rating (0-10):</label>
                            <input type="number" id="createRating" min="0" max="10" step="0.1" placeholder="e.g., 8.5" required>
                        </div>
                        <div class="form-group">
                            <label for="createComment">Comment:</label>
                            <textarea id="createComment" placeholder="Share your thoughts about the movie..."></textarea>
                        </div>
                        <div class="button-group">
                            <button type="submit" class="btn-primary">Add Review</button>
                            <button type="reset" class="btn-secondary">Clear</button>
                        </div>
                    </form>
                </div>
                
                <!-- READ REVIEW -->
                <div class="card">
                    <h2>🔍 Get Review</h2>
                    <form id="readForm">
                        <div class="form-group">
                            <label for="readId">Review ID:</label>
                            <input type="number" id="readId" placeholder="e.g., 1" required>
                        </div>
                        <button type="submit" class="btn-primary" style="margin-top: 20px;">Search Review</button>
                    </form>
                    <div id="readResult" style="margin-top: 20px;"></div>
                </div>
                
                <!-- UPDATE REVIEW -->
                <div class="card">
                    <h2>✏️ Update Review</h2>
                    <form id="updateForm">
                        <div class="form-group">
                            <label for="updateId">Review ID:</label>
                            <input type="number" id="updateId" placeholder="e.g., 1" required>
                        </div>
                        <div class="form-group">
                            <label for="updateMovie">Movie Name:</label>
                            <input type="text" id="updateMovie" placeholder="e.g., Inception" required>
                        </div>
                        <div class="form-group">
                            <label for="updateRating">Rating (0-10):</label>
                            <input type="number" id="updateRating" min="0" max="10" step="0.1" placeholder="e.g., 8.5" required>
                        </div>
                        <div class="form-group">
                            <label for="updateComment">Comment:</label>
                            <textarea id="updateComment" placeholder="Update your thoughts..."></textarea>
                        </div>
                        <div class="button-group">
                            <button type="submit" class="btn-primary">Update Review</button>
                            <button type="reset" class="btn-secondary">Clear</button>
                        </div>
                    </form>
                </div>
                
                <!-- DELETE REVIEW -->
                <div class="card">
                    <h2>🗑️ Delete Review</h2>
                    <form id="deleteForm">
                        <div class="form-group">
                            <label for="deleteId">Review ID:</label>
                            <input type="number" id="deleteId" placeholder="e.g., 1" required>
                        </div>
                        <button type="submit" class="btn-danger" style="margin-top: 20px; width: 100%;">Delete Review</button>
                    </form>
                </div>
            </div>
            
            <!-- ALL REVIEWS -->
            <div class="reviews-section">
                <h2>📋 All Reviews</h2>
                <button class="btn-primary" id="refreshBtn" style="margin-bottom: 20px; width: 150px;">🔄 Refresh</button>
                <div id="reviewsList" class="review-list"></div>
            </div>
        </div>
        
        <!-- MESSAGE CONTAINER -->
        <div id="messageContainer"></div>
        
        <script>
            // Show message
            function showMessage(text, type = 'info') {
                const container = document.getElementById('messageContainer');
                const msg = document.createElement('div');
                msg.className = `message ${type}`;
                msg.textContent = text;
                container.appendChild(msg);
                
                setTimeout(() => {
                    msg.remove();
                }, 4000);
            }
            
            // Format stars
            function formatStars(rating) {
                const fullStars = Math.floor(rating);
                const hasHalfStar = rating % 1 !== 0;
                let stars = '★'.repeat(fullStars);
                if (hasHalfStar) stars += '☆';
                return stars;
            }
            
            // Load all reviews
            async function loadAllReviews() {
                try {
                    const response = await fetch('/reviews');
                    if (!response.ok) throw new Error('Failed to load reviews');
                    
                    const reviews = await response.json();
                    const reviewsList = document.getElementById('reviewsList');
                    
                    if (!reviews || reviews.length === 0) {
                        reviewsList.innerHTML = '<div class="empty-state"><p>No reviews yet. Create one to get started!</p></div>';
                        return;
                    }
                    
                    reviewsList.innerHTML = reviews.map(review => `
                        <div class="review-card">
                            <div class="review-id">ID: ${review.id}</div>
                            <div class="review-movie">${review.movie}</div>
                            <div class="review-rating">
                                <span class="stars">${formatStars(review.rating)}</span>
                                <span class="rating-value">${review.rating}/10</span>
                            </div>
                            <div class="review-comment">"${review.comment}"</div>
                            <div class="review-actions">
                                <button class="btn-edit" onclick="editReview(${review.id})">Edit</button>
                                <button class="btn-delete" onclick="deleteReviewAction(${review.id})">Delete</button>
                            </div>
                        </div>
                    `).join('');
                } catch (error) {
                    showMessage('Error loading reviews: ' + error.message, 'error');
                }
            }
            
            // CREATE
            document.getElementById('createForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const data = {
                    id: parseInt(document.getElementById('createId').value),
                    movie: document.getElementById('createMovie').value,
                    rating: parseFloat(document.getElementById('createRating').value),
                    comment: document.getElementById('createComment').value
                };
                
                try {
                    const response = await fetch('/reviews', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.detail);
                    }
                    
                    showMessage('✅ Review created successfully!', 'success');
                    document.getElementById('createForm').reset();
                    loadAllReviews();
                } catch (error) {
                    showMessage('❌ Error: ' + error.message, 'error');
                }
            });
            
            // READ
            document.getElementById('readForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const reviewId = parseInt(document.getElementById('readId').value);
                
                try {
                    const response = await fetch(`/reviews/${reviewId}`);
                    
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.detail);
                    }
                    
                    const review = await response.json();
                    const readResult = document.getElementById('readResult');
                    readResult.innerHTML = `
                        <div class="review-card">
                            <div class="review-id">ID: ${review.id}</div>
                            <div class="review-movie">${review.movie}</div>
                            <div class="review-rating">
                                <span class="stars">${formatStars(review.rating)}</span>
                                <span class="rating-value">${review.rating}/10</span>
                            </div>
                            <div class="review-comment">"${review.comment}"</div>
                        </div>
                    `;
                    showMessage('✅ Review found!', 'success');
                } catch (error) {
                    document.getElementById('readResult').innerHTML = '';
                    showMessage('❌ Error: ' + error.message, 'error');
                }
            });
            
            // UPDATE
            document.getElementById('updateForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const reviewId = parseInt(document.getElementById('updateId').value);
                const data = {
                    id: reviewId,
                    movie: document.getElementById('updateMovie').value,
                    rating: parseFloat(document.getElementById('updateRating').value),
                    comment: document.getElementById('updateComment').value
                };
                
                try {
                    const response = await fetch(`/reviews/${reviewId}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.detail);
                    }
                    
                    showMessage('✅ Review updated successfully!', 'success');
                    document.getElementById('updateForm').reset();
                    loadAllReviews();
                } catch (error) {
                    showMessage('❌ Error: ' + error.message, 'error');
                }
            });
            
            // DELETE
            document.getElementById('deleteForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const reviewId = parseInt(document.getElementById('deleteId').value);
                
                if (!confirm('Are you sure you want to delete this review?')) return;
                
                try {
                    const response = await fetch(`/reviews/${reviewId}`, {
                        method: 'DELETE'
                    });
                    
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.detail);
                    }
                    
                    showMessage('✅ Review deleted successfully!', 'success');
                    document.getElementById('deleteForm').reset();
                    loadAllReviews();
                } catch (error) {
                    showMessage('❌ Error: ' + error.message, 'error');
                }
            });
            
            // Edit from review card
            function editReview(id) {
                const reviewCard = event.target.closest('.review-card');
                const movie = reviewCard.querySelector('.review-movie').textContent;
                const rating = parseFloat(reviewCard.querySelector('.rating-value').textContent);
                const comment = reviewCard.querySelector('.review-comment').textContent.slice(1, -1);
                
                document.getElementById('updateId').value = id;
                document.getElementById('updateMovie').value = movie;
                document.getElementById('updateRating').value = rating;
                document.getElementById('updateComment').value = comment;
                
                document.querySelector('header').scrollIntoView({ behavior: 'smooth' });
            }
            
            // Delete from review card
            async function deleteReviewAction(id) {
                if (!confirm('Are you sure you want to delete this review?')) return;
                
                try {
                    const response = await fetch(`/reviews/${id}`, {
                        method: 'DELETE'
                    });
                    
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.detail);
                    }
                    
                    showMessage('✅ Review deleted successfully!', 'success');
                    loadAllReviews();
                } catch (error) {
                    showMessage('❌ Error: ' + error.message, 'error');
                }
            }
            
            // Refresh button
            document.getElementById('refreshBtn').addEventListener('click', loadAllReviews);
            
            // Load reviews on page load
            loadAllReviews();
        </script>
    </body>
    </html>
    """

# --- CREATE (POST) ---
@app.post("/reviews")
def create_review(review: Review):
    try:
        response = supabase.table("reviews").insert(review.dict()).execute()
        return {"message": "Review added!", "review": review}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- READ (GET) ---
@app.get("/reviews/{review_id}")
def get_review(review_id: int):
    try:
        response = supabase.table("reviews").select("*").eq("id", review_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Review not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- READ ALL (GET) ---
@app.get("/reviews")
def get_all_reviews():
    try:
        response = supabase.table("reviews").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- UPDATE (PUT) ---
@app.put("/reviews/{review_id}")
def update_review(review_id: int, updated_review: Review):
    try:
        response = supabase.table("reviews").update(updated_review.dict()).eq("id", review_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Review not found")
        return {"message": "Review updated!", "review": updated_review}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- DELETE (DELETE) ---
@app.delete("/reviews/{review_id}")
def delete_review(review_id: int):
    try:
        response = supabase.table("reviews").delete().eq("id", review_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Review not found")
        return {"message": f"Review {review_id} deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
