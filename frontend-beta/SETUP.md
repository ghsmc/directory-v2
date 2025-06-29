# 🚀 Yale Network Search - Beta Frontend Setup

## ✅ Complete Setup Instructions

### 1. Start the Backend API

```bash
# Navigate to backend
cd ../backend

# Start the AI-enhanced API server
python ai_enhanced_api_server.py
```

The API will run at **http://localhost:8000**

### 2. Start the Frontend

```bash
# Navigate to frontend (this folder)
cd /Users/georgemccain/Desktop/untitled\ folder\ 4/yale-network-search/frontend-beta

# Install dependencies (if not already done)
npm install

# Start the React app
npm start
```

The frontend will run at **http://localhost:3000**

### 3. Test the Integration

1. Open **http://localhost:3000** in your browser
2. You should see a ChatGPT-style interface
3. Try an example search like "computer science students"
4. Results should appear with Yale profiles

## 🎯 Features Included

### ChatGPT-Style Interface
- Dark theme matching ChatGPT
- Chat-like interaction flow
- Sidebar with examples and tips
- Smooth animations and loading states

### Search Capabilities
- **Natural language**: "students studying AI at Yale"
- **Field-specific**: "computer science", "medicine"
- **School-specific**: "Yale Law School", "SOM"
- **Combined queries**: "data science research"

### Result Display
- **Profile cards** with name, headline, school
- **Relevance scoring** (0-10 scale)
- **AI summaries** (when available) with ✨ icon
- **AI tags** for categorization
- **Meta information** (major, class year, etc.)

### Example Queries
Built-in examples:
- "computer science students"
- "data science at Yale"
- "medical researchers" 
- "Yale Law School alumni"
- "artificial intelligence"
- "student athletes"

## 🔧 Troubleshooting

### Backend Not Connected
If you see "Unable to connect to search server":
1. Check that backend is running on port 8000
2. Visit http://localhost:8000 to verify API is active
3. Check browser console for CORS issues

### No Search Results
If searches return no results:
1. Try simple terms: "student", "medicine", "computer"
2. Check backend logs for errors
3. Verify database has 14,412+ profiles

### Frontend Won't Start
If npm start fails:
1. Delete node_modules: `rm -rf node_modules`
2. Reinstall: `npm install`
3. Check Node.js version: `node --version` (needs v14+)

## 📱 Mobile Support

The interface is responsive and works on:
- Desktop browsers
- Mobile phones (sidebar hidden)
- Tablets

## 🎨 Customization

### Colors & Theme
Edit `src/App.css` to change:
- Background colors: `#343541`, `#202123`
- Accent color: `#10a37f`
- Text colors: `#d1d5db`, `#8e8ea0`

### Example Queries
Edit `src/App.tsx` line 25-32 to add more examples:
```javascript
const EXAMPLE_QUERIES = [
  "your custom query",
  // ... existing queries
];
```

### API Endpoint
To change backend URL, edit `src/App.tsx` line 79:
```javascript
const response = await fetch(`http://your-api-url:8000/search?q=${encodeURIComponent(query)}&limit=10`);
```

## 🚀 Production Deployment

### Build for Production
```bash
npm run build
```

### Deploy Options
- **Vercel**: Connect GitHub repo, auto-deploy
- **Netlify**: Drag & drop `build/` folder
- **AWS S3**: Upload `build/` contents
- **Any web server**: Serve `build/` folder

### Environment Variables
For production, set:
- `REACT_APP_API_URL` for backend endpoint
- Update CORS settings in backend for production domain

## ✨ Next Steps

1. **Test thoroughly** with various search terms
2. **Run AI enhancement** on more profiles for better results
3. **Collect user feedback** on search quality
4. **Monitor performance** with real usage
5. **Add analytics** to track popular searches

The ChatGPT-style interface is ready for beta testing with your Yale network data!