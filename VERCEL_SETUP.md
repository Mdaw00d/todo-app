# Vercel Deployment Setup

To properly deploy this Next.js application to Vercel:

1. Import your project into Vercel
2. In the project settings, set the following:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Development Command**: `npm run dev`

This is necessary because the Next.js application is located in the `frontend` subdirectory rather than the repository root.

Alternatively, you can configure this using the Vercel CLI:

```bash
vercel --local-config=frontend/vercel.json
```