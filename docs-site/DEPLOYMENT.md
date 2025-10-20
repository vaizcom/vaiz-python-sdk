# Documentation Deployment Guide

The Vaiz SDK documentation can be deployed to various hosting platforms.

## Deployment Options

### Option 1: Vercel (Recommended)

Vercel provides the easiest deployment with automatic builds on every push.

#### Setup

1. **Install Vercel CLI** (optional):
   ```bash
   npm i -g vercel
   ```

2. **Deploy from Vercel Dashboard**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Set root directory to `docs-site`
   - Deploy!

3. **Or deploy from CLI**:
   ```bash
   cd docs-site
   vercel
   ```

#### Configuration

The `vercel.json` file is already configured:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "framework": "docusaurus"
}
```

### Option 2: GitHub Pages

Deploy to GitHub Pages using GitHub Actions.

#### Setup

1. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: GitHub Actions

2. **Push to main branch**:
   ```bash
   git push origin main
   ```

3. **Workflow runs automatically** when changes are pushed to `docs-site/`

4. **Access your site** at:
   ```
   https://[username].github.io/[repository-name]/
   ```

#### Update Configuration

If using a custom baseUrl, update `docusaurus.config.ts`:

```typescript
baseUrl: '/vaiz-python-sdk/',  // Change to your repo name
```

### Option 3: Netlify

1. **Connect repository** to Netlify

2. **Build settings**:
   - Base directory: `docs-site`
   - Build command: `npm run build`
   - Publish directory: `docs-site/build`

3. **Deploy**

### Option 4: Self-Hosted

#### Build Static Files

```bash
cd docs-site
npm run build
```

This creates a `build/` directory with static files.

#### Serve with nginx

```nginx
server {
    listen 80;
    server_name docs.example.com;
    
    root /path/to/docs-site/build;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

#### Serve with Apache

```apache
<VirtualHost *:80>
    ServerName docs.example.com
    DocumentRoot /path/to/docs-site/build
    
    <Directory /path/to/docs-site/build>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
        
        RewriteEngine On
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule ^ index.html [L]
    </Directory>
</VirtualHost>
```

#### Serve with Docker

```dockerfile
FROM node:20 as builder

WORKDIR /app
COPY docs-site/package*.json ./
RUN npm ci
COPY docs-site/ ./
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Continuous Deployment

### Automatic Deployment on Push

The GitHub Actions workflow (`.github/workflows/deploy-docs.yml`) automatically deploys when:

- Changes are pushed to `main` branch
- Files in `docs-site/` directory are modified

### Manual Deployment

Trigger deployment manually:

1. **GitHub Actions**:
   - Go to Actions tab
   - Select "Deploy Documentation" workflow
   - Click "Run workflow"

2. **Vercel CLI**:
   ```bash
   cd docs-site
   vercel --prod
   ```

## Custom Domain

### Vercel

1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

### GitHub Pages

1. Add `CNAME` file to `docs-site/static/`:
   ```
   docs.example.com
   ```

2. Update DNS:
   ```
   CNAME  docs.example.com -> username.github.io
   ```

3. Enable HTTPS in repository settings

### Netlify

1. Go to Domain Settings
2. Add custom domain
3. Update DNS records

## Environment Variables

For production builds, set these in your hosting platform:

```env
NODE_ENV=production
```

## Troubleshooting

### Build Fails

Check Node.js version:
```bash
node --version  # Should be 18+
```

Clear cache and rebuild:
```bash
cd docs-site
rm -rf node_modules .docusaurus
npm install
npm run build
```

### Links Not Working

Make sure `baseUrl` in `docusaurus.config.ts` matches your deployment path:

```typescript
// For root domain: docs.example.com
baseUrl: '/'

// For subdomain: example.com/docs
baseUrl: '/docs/'
```

### 404 on Refresh

Configure your server to always serve `index.html`:

**nginx**:
```nginx
try_files $uri $uri/ /index.html;
```

**Vercel/Netlify**: Already configured ✅

## Production Checklist

Before deploying to production:

- [ ] Test build locally: `npm run build`
- [ ] Check all internal links work
- [ ] Verify external links are correct
- [ ] Update `docusaurus.config.ts` URL and baseUrl
- [ ] Add Google Analytics (if needed)
- [ ] Set up custom domain (if needed)
- [ ] Enable HTTPS
- [ ] Test on mobile devices
- [ ] Set up monitoring/analytics

## Monitoring

### Vercel Analytics

Vercel provides built-in analytics. View them in your project dashboard.

### Google Analytics

Add to `docusaurus.config.ts`:

```typescript
presets: [
  [
    'classic',
    {
      gtag: {
        trackingID: 'G-XXXXXXXXXX',
      },
    },
  ],
],
```

## Support

For deployment issues:

- [Docusaurus Deployment Docs](https://docusaurus.io/docs/deployment)
- [Vercel Documentation](https://vercel.com/docs)
- [GitHub Pages Docs](https://docs.github.com/en/pages)

