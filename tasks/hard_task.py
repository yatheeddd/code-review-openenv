"""
Hard tasks: security — injection and unsafe handling of input or files.
"""

from __future__ import annotations

from typing import Any, Dict, List

HARD_TASKS: List[Dict[str, Any]] = [
    {
        "id": "hard-sql-injection",
        "code": "query = 'SELECT * FROM users WHERE id=' + user_input\n",
        "issue": "sql_injection",
    },
    {
        "id": "hard-command-injection",
        "code": (
            "import os\n\n"
            "def ping_host(hostname):\n"
            "    return os.system('ping -c 1 ' + hostname)\n"
        ),
        "issue": "command_injection",
    },
    {
        "id": "hard-unsafe-file",
        "code": (
            "def read_user_file(base_dir, user_path):\n"
            "    path = base_dir + '/' + user_path\n"
            "    return open(path, 'rb').read()\n"
        ),
        "issue": "unsafe_file_access",
    },
    {
        "id": "hard-hardcoded-auth",
        "code": (
            "def is_admin(token):\n"
            "    return token.lower() == 'admin'\n"
        ),
        "issue": "broken_authentication",
    },
]
