from collections import defaultdict
from datetime import datetime
import os

def analyze_user_activity(log_file_path: str) -> dict:
    action_counts = defaultdict(int)
    user_total_time = defaultdict(float)
    all_users = set()
    session_durations = []

    if not os.path.exists(log_file_path):
        return {
            'total_users': 0,
            'action_counts': {},
            'most_active_user': None,
            'average_session_time': 0.0
        }

    with open(log_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            clean_line = line.strip()
            if not clean_line:
                continue

            parts = clean_line.replace(',', ' ').split()
            if len(parts) != 4:
                continue

            raw_time, user_id, action, raw_val = parts
            action = action.lower()

            try:
                datetime.fromisoformat(raw_time)
            except ValueError:
                continue

            try:
                val = float(raw_val)
            except ValueError:
                continue

            all_users.add(user_id)
            action_counts[action] += 1

            if action == 'login' and val > 0:
                session_durations.append(val)
                user_total_time[user_id] += val
            elif val > 0:
                user_total_time[user_id] += val

    avg_session = (
        round(sum(session_durations) / len(session_durations), 1)
        if session_durations else 0.0
    )

    most_active = None
    if user_total_time:
        most_active = max(
            user_total_time.keys(),
            key=lambda u: (user_total_time[u], u)
        )
    elif all_users:
        most_active = sorted(all_users)[0]

    return {
        'total_users': len(all_users),
        'action_counts': dict(action_counts),
        'most_active_user': most_active,
        'average_session_time': avg_session
    }

if __name__ == "__main__":
    result = analyze_user_activity("activity.log")
    from pprint import pprint
    pprint(result)