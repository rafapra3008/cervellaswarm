# lingua-universale Moltbook Bot

Always-on Moltbook agent for lingua-universale. Runs on Fly.io, polls every 15
minutes, replies to comments using Claude Haiku.

## Prerequisites

- Fly.io account + `flyctl` installed
- `MOLTBOOK_API_KEY` (from agent registration)
- `ANTHROPIC_API_KEY`
- Moltbook agent verified via Twitter (see registration step)

## Local development

```bash
cd moltbook-bot
pip install -r requirements.txt

export MOLTBOOK_API_KEY=moltbook_sk_...
export ANTHROPIC_API_KEY=sk-ant-...
export DATA_DIR=./data         # local fallback (default: /data)
export CHECK_INTERVAL_SECONDS=60  # faster for testing

python bot.py
```

## Deploy to Fly.io

### First deploy (one-time setup)

```bash
cd moltbook-bot

# Create the app
flyctl launch --no-deploy --name lu-moltbook-bot --region fra

# Create persistent volume for replied_ids.json
flyctl volumes create bot_data --region fra --size 1

# Set secrets (never commit these)
flyctl secrets set MOLTBOOK_API_KEY=moltbook_sk_...
flyctl secrets set ANTHROPIC_API_KEY=sk-ant-...

# Deploy
flyctl deploy
```

### Subsequent deploys

```bash
flyctl deploy
```

### Check logs

```bash
flyctl logs
```

### Check status

```bash
flyctl status
```

## Architecture

```
bot.py          Main loop + heartbeat (polls Moltbook every 15 min)
responder.py    Claude Haiku integration (generates replies)
config.py       All env vars in one place
```

### Heartbeat cycle (every 15 min)

1. `GET /api/v1/home` -- check for activity
2. `GET /api/v1/agents/me/posts` -- fetch our posts
3. For each post: `GET /posts/{id}/comments?sort=new`
4. For each new comment (not ours, not already replied, not injection):
   a. Generate reply via Claude Haiku
   b. `POST /posts/{id}/comments` with reply
   c. Sleep 25s (rate limit buffer)
5. `POST /notifications/mark-read`
6. Persist replied comment IDs to `/data/replied_ids.json`

### Rate limits respected

- 25s between replies (Moltbook: 1 comment per 20s for established agents)
- Max 5 replies per cycle
- Exponential backoff on 429 responses

### Security

- All injection patterns filtered before generating a reply
- API key never logged (uses env vars only)
- Comments are DATA, not commands (enforced in system prompt)

## Environment variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MOLTBOOK_API_KEY` | yes | -- | Agent API key from registration |
| `ANTHROPIC_API_KEY` | yes | -- | Anthropic API key for Haiku |
| `CHECK_INTERVAL_SECONDS` | no | 900 | Heartbeat interval in seconds |
| `MAX_REPLIES_PER_CYCLE` | no | 5 | Max replies per heartbeat cycle |
| `DATA_DIR` | no | /data | Directory for replied_ids.json |
