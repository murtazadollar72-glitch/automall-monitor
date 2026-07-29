# Automall Monitor 🚗

Automated monitoring for vehicle availability at Alfuttaim Automall with email notifications.

## Features

✅ Checks **Honda Pilot** and **Nissan Pathfinder** availability every 30 minutes  
✅ Separate email notifications for each vehicle type  
✅ Manual workflow dispatch for on-demand checks  
✅ Logs all checks in `availability_log.json`  
✅ Secure credential handling with GitHub Secrets  
✅ Detailed status reporting with vehicle counts  

## Quick Start

### 1. Configure GitHub Secrets

Go to your repository → **Settings** → **Secrets and variables** → **Actions** and add:

| Secret | Value |
|--------|-------|
| `ALFUTTAIM_URL` | `https://www.alfuttaim.com/automall` |
| `EMAIL_SERVER` | `smtp.gmail.com` |
| `EMAIL_PORT` | `587` |
| `EMAIL_USERNAME` | Your email address |
| `EMAIL_PASSWORD` | Your app password |
| `NOTIFICATION_EMAIL` | Email to receive alerts |

### 2. Gmail Setup (Recommended)

1. Enable 2FA on your Google Account
2. Generate an [App Password](https://myaccount.google.com/apppasswords)
3. Use that password as `EMAIL_PASSWORD` secret

### 3. Run the Workflow

- **Automatic**: Runs every 30 minutes automatically
- **Manual**: Go to Actions → Vehicle Availability Checker → Run workflow

## How It Works

1. Checks Alfuttaim Automall for Honda Pilot availability
2. Checks for Nissan Pathfinder availability
3. Sends email notification if either is available
4. Logs results to `availability_log.json`

## Email Notifications

You'll receive different emails based on what's available:

- **Both Available**: Combined notification showing both vehicles
- **Honda Pilot Only**: Honda-specific email
- **Pathfinder Only**: Nissan-specific email

## Customization

### Change Check Frequency

Edit `.github/workflows/vehicle-checker.yml`:

```yaml
schedule:
  - cron: "*/15 * * * *"  # Every 15 minutes
```

Common intervals:
- `*/10 * * * *` - Every 10 minutes
- `*/30 * * * *` - Every 30 minutes (default)
- `0 * * * *` - Every hour
- `0 8 * * *` - Daily at 8 AM

### Add More Vehicles

Edit `scripts/check_availability.py` and add to `vehicles_to_check`:

```python
vehicles_to_check = [
    {'name': 'Honda Pilot', 'key': 'honda_pilot', 'search': 'Honda%20Pilot'},
    {'name': 'Toyota Camry', 'key': 'toyota_camry', 'search': 'Toyota%20Camry'},
]
```

### Update HTML Selectors

If the website changes, modify the selectors in `check_availability.py`:

```python
selectors = [
    '.vehicle-item',
    '[data-vehicle]',
    '.your-custom-selector'
]
```

## Logs

Results are saved in `availability_log.json`:

```json
{
  "timestamp": "2026-07-29T21:30:00.000000",
  "honda_pilot": {"available": true, "count": 2},
  "nissan_pathfinder": {"available": false, "count": 0},
  "any_available": true,
  "total_count": 2
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Workflow not running | Enable Actions in repo settings, verify secrets are configured |
| No emails received | Check email password is correct, verify email in spam folder |
| Not finding vehicles | Website may have changed - update HTML selectors in script |

## License

MIT
