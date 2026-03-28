# React + Next.js Migration Guide

## 📦 What Changed

The CRO Analyzer has been migrated from static HTML to a modern React + Next.js application. This provides:

- **Better component architecture**: Reusable React components for KPIs, charts, and recommendations
- **Enhanced performance**: Code splitting, image optimization, and client-side routing
- **Improved scalability**: Easier to add features and maintain codebase
- **Type safety**: TypeScript support for more robust code
- **Better state management**: Foundation for Redux/Zustand if needed

## 🚀 Quick Start

### Prerequisites

Before starting, install Node.js (v18 or higher):
- Download from: https://nodejs.org/
- Or use Homebrew: `brew install node`

### Installation & Development

1. **Navigate to the web directory:**
   ```bash
   cd web
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev:full
   ```
   
   This command runs both:
   - Next.js frontend on `http://localhost:3000`
   - Express API server on `http://localhost:3001`

4. **Open in browser:**
   - Frontend: http://localhost:3000
   - API docs: http://localhost:3001/api/health

### Build for Production

```bash
npm run build
```

This creates an optimized Next.js production build.

## 📁 Project Structure

```
web/
├── app/                          # Next.js App Directory
│   ├── components/              # React components
│   │   ├── DashboardLayout.tsx  # Main layout wrapper
│   │   ├── KPICard.tsx          # KPI display cards
│   │   ├── FunnelChart.tsx      # Funnel visualization
│   │   ├── RecommendationsList.tsx
│   │   └── HistoryTable.tsx
│   ├── dashboard/               # Dashboard page route
│   │   └── page.tsx
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Login/Register page (root route)
│   ├── globals.css              # Global styles
│   └── auth.css                 # Auth page styles
├── server/                      # Express API server
│   ├── server.js               # Main API routes
│   ├── scheduler.js            # Job scheduling
│   └── scripts/                # Database setup scripts
├── next.config.js              # Next.js configuration
├── tsconfig.json               # TypeScript configuration
└── package.json                # Dependencies and scripts
```

## 🔄 How It Works

### Frontend (Next.js + React)
- **Page Routes**: 
  - `/` - Login/Register page
  - `/dashboard` - Main CRO dashboard with KPIs, charts, and recommendations
  
- **Components**: Modular React components for better reusability
- **Styling**: CSS modules per component + global styles
- **API Integration**: Fetches data from Express backend at `http://localhost:3001`

### Backend (Express.js)
- **API Server**: Runs independently on port 3001
- **Routes**: 
  - `/api/auth/*` - Authentication endpoints
  - `/api/analysis/*` - CRO analysis endpoints
  - `/api/examples/*` - Example data
- **Database**: Connected to Supabase for data persistence
- **Scheduler**: Node.js job scheduler for automated analysis

### Development vs Production

**Development Mode** (`npm run dev:full`):
- Both Next.js and Express run simultaneously
- Frontend: http://localhost:3000
- API: http://localhost:3001
- Direct API calls without proxying

**Production Mode** (Deployed to Vercel):
- Next.js handles frontend and API proxying
- All requests routed through Next.js
- Express API can be deployed elsewhere or run as Vercel function

## 🛠️ Environment Variables

Create a `.env.local` file in the `web/` directory:

```env
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:3001
```

## 📊 Component Examples

### Using KPICard
```tsx
<KPICard
  title="Taxa de Conversão"
  value={3.45}
  unit="%"
  trend="up"
/>
```

### Using FunnelChart
```tsx
<FunnelChart
  data={[
    { stage: 'Visitantes', users: 10000 },
    { stage: 'Cliques', users: 5000 },
    { stage: 'Conversão', users: 500 }
  ]}
/>
```

## 🔌 API Integration

All components fetch data from the Express API:

```tsx
const response = await fetch(
  `${API_URL}/api/analysis/latest`,
  { headers: { Authorization: `Bearer ${token}` } }
);
```

## 🚢 Deployment to Vercel

1. **Ensure changes are committed:**
   ```bash
   git add .
   git commit -m "feat: Migrate to React + Next.js"
   git push origin main
   ```

2. **Go to Vercel Dashboard:**
   - https://vercel.com/dashboard

3. **Trigger deployment:**
   - Click "Redeploy" on cro-analyzer project

4. **Set environment variables:**
   - NEXT_PUBLIC_SUPABASE_URL
   - NEXT_PUBLIC_SUPABASE_ANON_KEY
   - SUPABASE_SERVICE_KEY

## 📝 Available Scripts

- `npm run dev` - Start Next.js dev server only
- `npm run dev:full` - Start Next.js + Express server
- `npm run build` - Build Next.js for production
- `npm start` - Start Next.js production server
- `npm run start:server` - Start Express server only
- `npm run schedule` - Run job scheduler
- `npm run setup-db` - Initialize Supabase schema
- `npm run seed` - Seed demo data

## 🎨 Styling & Customization

All styles are modular and organized:
- `app/globals.css` - Global reset and utilities
- `app/auth.css` - Authentication page styles
- `app/dashboard/dashboard.css` - Dashboard layout
- `app/components/*.css` - Component-specific styles

Colors used:
- Primary Green: `#4cc073`
- Background: Dark gradient `#1a1a2e` to `#16213e`
- Text: Light gray `#e0e0e0`
- Accent: Warning `#ffa500`, Danger `#ff6b6b`

## 🐛 Troubleshooting

### Port already in use
```bash
# Find process on port 3000
lsof -i :3000
# Kill it
kill -9 <PID>
```

### Build errors
```bash
# Clear Next.js cache
rm -rf .next/
npm run build
```

### API connection refused
- Ensure Express server is running: `npm run start:server`
- Check `NEXT_PUBLIC_API_URL` in `.env.local`

## 📚 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Express.js Guide](https://expressjs.com/)
- [Supabase Guide](https://supabase.com/docs)

## 🆚 Before vs After

### Before (Static HTML)
- Single HTML file for dashboard
- jQuery-based interactivity
- Manual API requests in inline JavaScript
- Limited reusability
- Harder to maintain

### After (React + Next.js)
- Component-based architecture
- TypeScript for type safety
- Modular state management
- Reusable components
- Better development experience
- Modern tooling and build process

## ✨ What's Next?

Future enhancements:
- Real-time WebSocket updates
- Advanced data visualization
- State management (Redux/Zustand)
- Testing suite (Jest + React Testing Library)
- Mobile app (React Native)
- Dark mode toggle (already designed for it)
