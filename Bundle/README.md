# DAE-GOV Memory Bundle

## Structure

- `user0/`, `user1/`, etc. - Per-user memory compartments
  - `conversations/` - Conversation logs
  - `learning/` - Learning progression data
  - `r_matrix_snapshots/` - R-matrix state over time

- `../monitoring/` - System health monitoring

## Usage

Each user gets isolated memory. The system automatically:
1. Tracks R-matrix updates per user
2. Saves conversation history
3. Monitors learning progression
4. Creates periodic snapshots

## Monitoring

Run health checks:
```bash
python3 monitoring/health_check.py
```
